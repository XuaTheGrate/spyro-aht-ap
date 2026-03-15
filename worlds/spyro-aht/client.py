from __future__ import annotations

import asyncio
import random
from abc import ABC, abstractmethod
from collections import Counter
from math import floor
import struct

import kvui
import dolphin_memory_engine

import Utils
from CommonClient import ClientCommandProcessor, CommonContext, logger, server_loop, gui_enabled, get_base_parser
from NetUtils import ClientStatus, NetworkItem

from . import consts
from .pcsx2_interface import Pine


class GenericClient(ABC):
    addresses: consts.AddressList
    ready: asyncio.Event
    msg_queue: asyncio.Queue[str]

    @property
    @abstractmethod
    def is_connected(self) -> bool: raise NotImplementedError
    @abstractmethod
    async def connect(self): raise NotImplementedError
    @abstractmethod
    async def disconnect(self): raise NotImplementedError
    @abstractmethod
    async def is_in_game(self) -> bool: raise NotImplementedError
    @abstractmethod
    async def is_paused(self) -> bool: raise NotImplementedError
    @abstractmethod
    async def is_loading(self) -> bool: raise NotImplementedError
    @abstractmethod
    async def scan_locations(self, ctx: SpyroAHTContext) -> set[int]: raise NotImplementedError
    @abstractmethod
    async def set_ability_flag(self, flag: int, to: bool): raise NotImplementedError
    @abstractmethod
    async def get_item_count(self, addr: int) -> int: raise NotImplementedError
    @abstractmethod
    async def add_item(self, addr: int, count: int): raise NotImplementedError
    @abstractmethod
    async def force_set_breath(self, breath_id: int): raise NotImplementedError
    @abstractmethod
    async def check_goal(self, ctx: SpyroAHTContext): raise NotImplementedError
    @abstractmethod
    async def scout_location(self, ctx: SpyroAHTContext): raise NotImplementedError
    @abstractmethod
    async def has_any_breath(self) -> bool: raise NotImplementedError
    @abstractmethod
    async def add_gem_pack(self): raise NotImplementedError
    @abstractmethod
    async def apply_patch(self, ctx: SpyroAHTContext): raise NotImplementedError
    @abstractmethod
    async def prepare_shop_items(self, ctx: SpyroAHTContext, *locations): raise NotImplementedError
    @abstractmethod
    async def enable_butterfly_jar(self): raise NotImplementedError
    @abstractmethod
    async def notification_task(self): raise NotImplementedError


class PCSX2Client(GenericClient):
    def __init__(self, pine: Pine | None = None, *, slot: int = 28011, loop: asyncio.AbstractEventLoop | None = None):
        self.pine: Pine = pine or Pine(loop or asyncio.get_running_loop(), slot=slot)
        self._slot = slot
        self.ready = asyncio.Event()
    
    @property
    def is_connected(self) -> bool:
        return self.pine.is_connected()
    
    async def connect(self):
        await self.disconnect()
        await self.pine.connect()
        logger.info("PCSX2 connection established")
        game_id = await self.pine.get_game_id()
        # TODO: support for PAL version
        match game_id:
            case 'SLUS-20884':
                self.addresses = consts.SLUS_20884()
            case _:
                logger.error(f"Unsupported game ID {game_id}")
                self.pine.disconnect()
                return
        self.ready.set()
    
    async def disconnect(self):
        if self.pine.is_connected():
            self.ready.clear()
            self.pine.disconnect()

    async def is_in_game(self) -> bool:
        return await self.pine.read_int32(self.addresses.IN_GAME) == 1
    
    async def is_paused(self) -> bool:
        return await self.pine.read_int32(self.addresses.PAUSE) == 1
    
    async def is_loading(self) -> bool:
        return await self.pine.read_int32(self.addresses.LOADING) == 1
    
    async def scan_locations(self, ctx: SpyroAHTContext) -> set[int]:
        result: set[int] = set()
        for aploc, index in consts.LOCATIONS_BITFIELD.items():
            if aploc in ctx.checked_locations:
                continue

            addr = self.addresses.g_LOCATION_BITFIELD + floor(index / 8)
            data = await self.pine.read_int8(addr)
            flag = data & (1 << (index % 8))
            if flag:
                result.add(aploc)
        
        for obj, aploc in consts.LOCATIONS_OBJECTIVE.items():
            if aploc in ctx.checked_locations:
                continue
            
            index = (obj & 0xFFFF) - 1
            uint = floor(index / 32)
            bit = index % 32
            data = await self.pine.read_int32(self.addresses.OBJECTIVES + (uint * 4))
            flag = data & (1 << bit)
            if flag:
                result.add(aploc)

        return result        
    
    async def set_ability_flag(self, flag: int, to: bool):
        flags = await self.pine.read_int32(self.addresses.ABILITY_FLAGS)
        if to:
            await self.pine.write_int32(self.addresses.ABILITY_FLAGS, flags | flag)
        else:
            await self.pine.write_int32(self.addresses.ABILITY_FLAGS, flags & ~flag)
    
    async def get_item_count(self, addr: int) -> int:
        return await self.pine.read_int8(addr)
    
    async def add_item(self, addr: int, count: int):
        c = await self.get_item_count(addr)
        if c == 0 and count < 0:
            logger.warning(f"Attempted to set negative value for 0x00{addr:x}")
            return
        await self.pine.write_int8(addr, count + c)
    
    async def force_set_breath(self, breath_id: int):
        await self.pine.write_int8(self.addresses.ACTIVE_BREATH, breath_id)


class DolphinClient(GenericClient):
    def __init__(self) -> None:
        self.ready = asyncio.Event()
        self.addresses = consts.G5SE7D()
        self._scouted_locations: set[int] = set()
        self.msg_queue = asyncio.Queue()
        self._notification_task = asyncio.create_task(self.notification_task())
    
    async def connect(self):
        if not dolphin_memory_engine.is_hooked():
            dolphin_memory_engine.hook()
            game_id: bytes = dolphin_memory_engine.read_bytes(0x80000000, 6)
            if game_id != b'G5SE7D':
                dolphin_memory_engine.un_hook()
                logger.error(f"Unsupported game ID {game_id.decode()}")
                return
        logger.info("Successfully hooked into Dolphin")
        self.ready.set()
    
    async def disconnect(self):
        self._notification_task.cancel()
        if dolphin_memory_engine.is_hooked():
            dolphin_memory_engine.un_hook()
    
    @property
    def is_connected(self) -> bool:
        return dolphin_memory_engine.is_hooked()
    
    async def is_in_game(self) -> bool:
        m_state = int.from_bytes(dolphin_memory_engine.read_bytes(self.addresses.IN_GAME, 4), 'big')
        m_pause = dolphin_memory_engine.read_byte(self.addresses.PAUSE)
        return m_state == 3 and (m_pause & 0x80 == 0)
    
    async def is_paused(self) -> bool:
        # unsure if separate handling is necessary
        return not await self.is_in_game()
    
    async def is_loading(self) -> bool:
        # unsure if separate handling is necessary
        return await self.is_paused()
    
    async def scan_locations(self, ctx: SpyroAHTContext) -> set[int]:
        result: set[int] = set()
        for aploc, index in consts.LOCATIONS_BITFIELD.items():
            await asyncio.sleep(0)  # a 0 second sleep is used to yield back to the event loop, bandaid fix for blocking

            if aploc in ctx.checked_locations:
                continue
            
            addr = self.addresses.g_LOCATION_BITFIELD + floor(index / 8)
            data = dolphin_memory_engine.read_byte(addr)
            flag = data & (1 << (index % 8))
            if flag:
                result.add(aploc)
        
        for obj, aploc in consts.LOCATIONS_OBJECTIVE.items():
            await asyncio.sleep(0)

            if aploc in ctx.checked_locations:
                continue
            
            index = (obj & 0xFFFF) - 1
            uint = floor(index / 32)
            bit = index % 32
            data = int.from_bytes(dolphin_memory_engine.read_bytes(self.addresses.OBJECTIVES + (uint * 4), 4), 'big')
            flag = data & (1 << bit)
            if flag:
                result.add(aploc)
        
        if ctx._slot_data['randomize_shop_items'] == 1:
            for i in range(57):
                await asyncio.sleep(0)

                purchase_flag = dolphin_memory_engine.read_byte(self.addresses.g_XLS_SHOP_TEXT + (0x32 * i))
                if purchase_flag:
                    result.add(1001 + i)

        return result
    
    async def set_ability_flag(self, flag: int, to: bool):
        flags = int.from_bytes(dolphin_memory_engine.read_bytes(self.addresses.ABILITY_FLAGS, 4), 'big')
        if to:
            flags |= flag
        else:
            flags &= ~flag
        dolphin_memory_engine.write_bytes(self.addresses.ABILITY_FLAGS, flags.to_bytes(4))
    
    async def get_item_count(self, addr: int) -> int:
        return dolphin_memory_engine.read_byte(addr)
    
    async def add_item(self, addr: int, count: int):
        c = await self.get_item_count(addr)
        if c == 0 and count < 0:
            logger.warning(f"Attempted to set negative value for 0x{addr:x}")
            return
        dolphin_memory_engine.write_byte(addr, c + count)
    
    async def add_item_4(self, addr: int, count: int):
        c = int.from_bytes(dolphin_memory_engine.read_bytes(addr, 4), 'big')
        if c == 0 and count < 0:
            logger.warning(f"Attempted to set negative value for 0x{addr:x}")
            return
        dolphin_memory_engine.write_bytes(addr, (c + count).to_bytes(4))
    
    async def force_set_breath(self, breath_id: int):
        dolphin_memory_engine.write_bytes(self.addresses.ACTIVE_BREATH, breath_id.to_bytes(4))
    
    async def check_goal(self, ctx: SpyroAHTContext):
        obj = consts.GOALS[ctx._slot_data['misc_goal']]

        index = (obj & 0xFFFF) - 1
        uint = floor(index / 32)
        bit = index % 32
        data = int.from_bytes(dolphin_memory_engine.read_bytes(self.addresses.OBJECTIVES + (uint * 4), 4), 'big')
        flag = data & (1 << bit)
        if flag:
            await ctx.send_msgs([{"cmd":"StatusUpdate","status":ClientStatus.CLIENT_GOAL}])
    
    async def scout_location(self, ctx: SpyroAHTContext):
        if not ctx._slot_data['misc_hint_minigame_rewards']:
            return
        
        locations: set[int] = set()
        for obj, loc in consts.SCOUT_OBJECTIVES.items():
            index = (obj & 0xFFFF) - 1
            uint = floor(index / 32)
            bit = index % 32
            data = int.from_bytes(dolphin_memory_engine.read_bytes(self.addresses.OBJECTIVES + (uint * 4), 4), 'big')
            flag = data & (1 << bit)
            if flag:
                locations.update(loc)
        locations.difference_update(self._scouted_locations)
        
        if locations:
            self._scouted_locations.update(locations)
            await ctx.send_msgs([{"cmd":"LocationScouts","locations":locations,"create_as_hint":2}])
    
    async def has_any_breath(self) -> bool:
        b = int.from_bytes(dolphin_memory_engine.read_bytes(self.addresses.ABILITY_FLAGS, 4), 'big')
        return b & 0x800e0 > 0

    async def add_gem_pack(self):
        await self.add_item(self.addresses.g_NUM_GEM_PACKS_RECEIVED, 1)
        await self.add_item_4(self.addresses.GEMS, 500)
        await self.add_item_4(self.addresses.TOTAL_GEMS, 500)
    
    async def enable_butterfly_jar(self):
        flag = dolphin_memory_engine.read_byte(self.addresses.g_BUTTERFLY_JAR)
        if not flag:
            dolphin_memory_engine.write_byte(self.addresses.g_BUTTERFLY_JAR, 1)
            await self.set_ability_flag(consts.AbilityFlags.ButterflyJar, True)
    
    async def apply_patch(self, ctx: SpyroAHTContext):
        dolphin_memory_engine.write_byte(self.addresses.p_SKIP_CUTSCENE_BUTTON, ctx._slot_data['misc_skip_cutscenes'])
        dolphin_memory_engine.write_byte(self.addresses.p_ALLOW_TELEPORT_TO_HUB, 1)
        dolphin_memory_engine.write_byte(self.addresses.p_ALLOW_IMMEDIATE_REALM_ACCESS, ctx._slot_data['misc_allow_immediate_realm_access'])

        dolphin_memory_engine.write_bytes(self.addresses.p_MW_SEED, (int(ctx._seed) & 0xffffffff).to_bytes(4, 'big'))

        if ctx._slot_data['randomize_shop_items']:
            await ctx.send_msgs([{"cmd":"LocationScouts","locations":list(range(1001, 1058)),"create_as_hint":0}])
            await ctx._shop_items_received.wait()
            await self.prepare_shop_items(ctx, *ctx._shop_items)

        dolphin_memory_engine.write_byte(self.addresses.p_PATCH_BEEN_WRITTEN_TO, 1)
    
    async def prepare_shop_items(self, ctx: SpyroAHTContext, *items: NetworkItem):
        dolphin_memory_engine.write_bytes(self.addresses.p_XLS_SHOP_ROWCOUNT, (57).to_bytes(4, 'big'))

        for idx, item in enumerate(items):
            player = ctx.player_names[item.player]
            name = ctx.item_names.lookup_in_slot(item.item, item.player)

            n = ctx._slot_data['shop_prices_min']
            x = ctx._slot_data['shop_prices_max']
            rng = ctx._slot_data['randomize_shop_prices']
            match rng:
                case 0 | 1: # normal dist
                    price = random.randint(n, x)
                case 2: # lower bound dist
                    s = list(range(n, x+1))
                    w = list(range(x, n+1, -1))
                    price = random.choices(s, w, k=1)[0]
                case 3: # upper bound dist
                    s = list(range(n, x+1))
                    price = random.choices(s, s, k=1)[0]
                case _:
                    raise RuntimeError
            
            model = consts.ShopItemModel.Lockpick

            if item.player == ctx.slot: # self
                match item.item:
                    case 0x1A | 0x1D: # double gems or gem pack
                        price = 1
                    case 0x1 | 0xE | 0x5 | 0x6 | 0x7 | 0xD: # double jump or breaths or charge
                        price = min(price, random.randint(400, 500))
                
                match item.item:
                    case 0xE:
                        model = consts.ShopItemModel.FireBomb
                    case 0x5:
                        model = consts.ShopItemModel.ElectricBomb
                    case 0x6:
                        model = consts.ShopItemModel.WaterBomb
                    case 0x7:
                        model = consts.ShopItemModel.IceBomb
                    case 0xF:
                        model = consts.ShopItemModel.HealthUpgrade
                    case 0x18:
                        model = consts.ShopItemModel.Keychain
                    case 0x19:
                        model = consts.ShopItemModel.ButterflyJar
                    case 0x1B:
                        model = consts.ShopItemModel.Shockwave
            
            i = consts.XLSShoppingItem(model, consts.TextEntry(idx, f"{player}'s {name}"), (price, floor(price + (price * 0.25))))

            offset = 0x20 * (idx + 1)
            dolphin_memory_engine.write_bytes(self.addresses.p_XLS_SHOP_ITEMS + offset, i.to_bytes('big'))
            dolphin_memory_engine.write_bytes(self.addresses.p_XLS_SHOP_TEXT + (0x32 * idx), i.text.to_bytes('big'))

            await asyncio.sleep(0)
    
    async def notification_task(self):
        try:
            while True:
                await asyncio.sleep(3.5)
                if await self.is_in_game() and not await self.is_paused() and not await self.is_loading():
                    message = await self.msg_queue.get()

                    if len(message) > 255:
                        message = message[:255]

                    colour = struct.pack(">BBBB", 0x80, 0x80, 0x80, 0x80)
                    dolphin_memory_engine.write_bytes(self.addresses.n_AP_NOTIFICATION_COLOR, colour)
                    dolphin_memory_engine.write_bytes(self.addresses.n_AP_NOTIFICATION_TIMER, (3*60).to_bytes(4))
                    dolphin_memory_engine.write_bytes(self.addresses.n_AP_NOTIFICATION_TEXT_BUFFER, (message + "\0").encode('ascii'))
        except Exception:
            logger.error("ERROR IN NOTIFICATION_TASK", exc_info=True)


class SpyroAHTCommandProcessor(ClientCommandProcessor):
    ctx: SpyroAHTContext

    def _cmd_debug_send(self, location: str) -> bool:
        """
        DEBUG COMMAND ONLY USE IF NECESSARY. Manually send a location.
        """
        from .locations import LOCATION_NAME_TO_ID
        id = LOCATION_NAME_TO_ID.get(location, None)
        if not id:
            self.output("Invalid location.")
            return False
        Utils.async_start(self.ctx.send_msgs([{"cmd":"LocationChecks","locations":[id]}]))
        return True

    def _cmd_client(self, client: str = "") -> bool:
        """
        Assign the used emulator client. Should be one of 'pcsx2' or 'dolphin'.
        """
        match client.lower():
            case 'pcsx2':
                #self.ctx.emu_client = PCSX2Client()
                raise NotImplementedError
            case 'dolphin':
                self.ctx.emu_client = DolphinClient()
            case _:
                self.output("Please specify 'pcsx2' or 'dolphin' as your client.")
                return False

        self.ctx.emu_loop = asyncio.create_task(emu_loop(self.ctx), name="EmuLoop")
        Utils.async_start(self.ctx.emu_client.connect())
        return True


class SpyroAHTContext(CommonContext):
    command_processor = SpyroAHTCommandProcessor
    game = "Spyro: A Hero's Tail"
    items_handling = 0b111

    def __init__(self, server_address: str | None = None, password: str | None = None) -> None:
        super().__init__(server_address, password)

        self.emu_client: GenericClient
        self.emu_loop: asyncio.Task | None = None
        self.synced_items: set[NetworkItem] = set()
        self.auth_ready = asyncio.Event()
        self.item_counts = Counter()

        self._seed = ""
        self._shop_items_received = asyncio.Event()
        self._shop_items: list[NetworkItem] = []

    def make_gui(self) -> type[kvui.GameManager]:
        ui = super().make_gui()
        ui.base_title = "Spyro: A Hero's Tail Archipelago Client"
        return ui
    
    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect(game=self.game)
    
    async def send_connect(self, **kwargs) -> None:
        await super().send_connect(**kwargs)
    
    def on_package(self, cmd: str, args: dict):
        match cmd:
            case 'Connected':
                self._slot_data = args['slot_data']
                self.auth_ready.set()
            case 'RoomInfo':
                self._seed = args['seed_name']
            case 'LocationInfo':
                self._shop_items = [NetworkItem(*item) for item in args['locations']]
                self._shop_items_received.set()


async def dispatch_items(ctx: SpyroAHTContext):
    ctx.item_counts = Counter(i.item for i in ctx.items_received)
    for item in ctx.items_received:
        match item.item:
            case 0xB: # Swim
                await ctx.emu_client.set_ability_flag(consts.AbilityFlags.Swim, True)
            case 0xC: # Glide
                await ctx.emu_client.set_ability_flag(consts.AbilityFlags.Glide, True)
            case 0xD: # Charge
                await ctx.emu_client.set_ability_flag(consts.AbilityFlags.Charge, True)
            case 0x1: # Double Jump
                await ctx.emu_client.set_ability_flag(consts.AbilityFlags.DoubleJump, True)
            case 0x2: # Pole Spin
                await ctx.emu_client.set_ability_flag(consts.AbilityFlags.PoleSpin, True)
            case 0x3: # Wing Shield
                await ctx.emu_client.set_ability_flag(consts.AbilityFlags.WingShield, True)
            case 0x4:
                await ctx.emu_client.set_ability_flag(consts.AbilityFlags.WallKick, True)
            case 0xE: # Fire Breath
                if not await ctx.emu_client.has_any_breath():
                    await ctx.emu_client.force_set_breath(consts.BREATH_FIRE)
                await ctx.emu_client.set_ability_flag(consts.AbilityFlags.FireBreath, True)
            case 0x5: # Lightning Breath
                if not await ctx.emu_client.has_any_breath():
                    await ctx.emu_client.force_set_breath(consts.BREATH_ELECTRIC)
                await ctx.emu_client.set_ability_flag(consts.AbilityFlags.LightningBreath, True)
            case 0x6: # Water Breath
                if not await ctx.emu_client.has_any_breath():
                    await ctx.emu_client.force_set_breath(consts.BREATH_WATER)
                await ctx.emu_client.set_ability_flag(consts.AbilityFlags.WaterBreath, True)
            case 0x7: # Ice Breath
                if not await ctx.emu_client.has_any_breath():
                    await ctx.emu_client.force_set_breath(consts.BREATH_ICE)
                await ctx.emu_client.set_ability_flag(consts.AbilityFlags.IceBreath, True)
            case 0x8: # Dark Gem
                count = await ctx.emu_client.get_item_count(ctx.emu_client.addresses.DARK_GEM_COUNT)
                if count < ctx.item_counts[0x8]:
                    await ctx.emu_client.add_item(ctx.emu_client.addresses.DARK_GEM_COUNT, 1)
            case 0x9: # Light Gem
                count = await ctx.emu_client.get_item_count(ctx.emu_client.addresses.LIGHT_GEM_COUNT)
                if count < ctx.item_counts[0x9]:
                    await ctx.emu_client.add_item(ctx.emu_client.addresses.LIGHT_GEM_COUNT, 1)
            case 0xA: # Dragon Egg
                count = await ctx.emu_client.get_item_count(ctx.emu_client.addresses.DRAGON_EGG_COUNT)
                if count < ctx.item_counts[0xA]:
                    await ctx.emu_client.add_item(ctx.emu_client.addresses.DRAGON_EGG_COUNT, 1)
            case 0x1C: # Lockpick
                count = await ctx.emu_client.get_item_count(ctx.emu_client.addresses.g_NUM_LOCKPICKS)
                if count < ctx.item_counts[0x1C]:
                    await ctx.emu_client.add_item(ctx.emu_client.addresses.g_NUM_LOCKPICKS, 1)
                    await ctx.emu_client.add_item(ctx.emu_client.addresses.LOCKPICKS, 1)
            case 0xF: # Extra Health Unit
                await ctx.emu_client.set_ability_flag(consts.AbilityFlags.SparxHealthUpgrade, True)
            case 0x19: # Butterfly Jar
                await ctx.emu_client.enable_butterfly_jar()
            case 0x1A: # Double Gems
                await ctx.emu_client.set_ability_flag(consts.AbilityFlags.DoubleGems, True)
            case 0x1B: # Shockwave
                await ctx.emu_client.set_ability_flag(consts.AbilityFlags.Shockwave, True)
            case 0x1D: # Gem Pack
                count = await ctx.emu_client.get_item_count(ctx.emu_client.addresses.g_NUM_GEM_PACKS_RECEIVED)
                if count < ctx.item_counts[0x1D]:
                    await ctx.emu_client.add_gem_pack()


starter_checks = {229, 230, 231, 232}


async def dispatch_locations(ctx: SpyroAHTContext):
    locations = await ctx.emu_client.scan_locations(ctx)

    for c in starter_checks:
        if c not in ctx.checked_locations:
            locations.add(c)

    if locations:
        await ctx.send_msgs([{"cmd":"LocationChecks","locations":locations}])


async def emu_loop(ctx: SpyroAHTContext):
    try:
        await ctx.emu_client.ready.wait()
        await ctx.auth_ready.wait()

        await ctx.emu_client.apply_patch(ctx)

        while not ctx.exit_event.is_set():
            try:
                await asyncio.wait_for(ctx.watcher_event.wait(), 1.0)
            except asyncio.TimeoutError:
                pass
            ctx.watcher_event.clear()

            if await ctx.emu_client.is_in_game() and not await ctx.emu_client.is_paused() and not await ctx.emu_client.is_loading():
                await ctx.emu_client.set_ability_flag(consts.AbilityFlags.PurchasedLockpick, True)

                await dispatch_items(ctx)
                await ctx.emu_client.scout_location(ctx)
                await dispatch_locations(ctx)
                await ctx.emu_client.check_goal(ctx)
    except Exception:
        logger.error("ERROR IN EMULATOR LOOP, PLEASE REPORT IN THREAD", exc_info=True)
    finally:
        await ctx.emu_client.disconnect()


def main(*args: str):
    Utils.init_logging("Spyro: A Hero's Tail Client")

    async def _main(connect: str | None, password: str | None):
        ctx = SpyroAHTContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        await ctx.exit_event.wait()
        ctx.watcher_event.set()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.emu_loop:
            await ctx.emu_loop
    
    parser = get_base_parser()
    parsed_args = parser.parse_args(args)
    import colorama
    colorama.init()
    asyncio.run(_main(parsed_args.connect, parsed_args.password))
    colorama.deinit()


if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
