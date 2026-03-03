from __future__ import annotations

import asyncio
from collections import Counter
from math import floor

import kvui
import dolphin_memory_engine

import Utils
from CommonClient import ClientCommandProcessor, CommonContext, logger, server_loop, gui_enabled, get_base_parser
from NetUtils import NetworkItem

from . import consts
from .pcsx2_interface import Pine


class GenericClient:
    addresses: consts.AddressList
    ready: asyncio.Event
    @property
    def is_connected(self) -> bool: raise NotImplementedError
    async def connect(self): raise NotImplementedError
    async def disconnect(self): raise NotImplementedError
    async def is_in_game(self) -> bool: raise NotImplementedError
    async def is_paused(self) -> bool: raise NotImplementedError
    async def is_loading(self) -> bool: raise NotImplementedError
    async def scan_locations(self, ctx: SpyroAHTContext) -> set[int]: raise NotImplementedError
    async def set_ability_flag(self, flag: int, to: bool): raise NotImplementedError
    async def get_item_count(self, addr: int) -> int: raise NotImplementedError
    async def add_item(self, addr: int, count: int): raise NotImplementedError
    async def force_set_breath(self, breath_id: int): raise NotImplementedError


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
        #self.ready.set()
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

            addr = self.addresses.BITFIELD + floor(index / 8)
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
        await self._temp_check_ability_flags(ctx)
        result: set[int] = set()
        for aploc, index in consts.LOCATIONS_BITFIELD.items():
            await asyncio.sleep(0)  # a 0 second sleep is used to yield back to the event loop, bandaid fix for blocking

            if aploc in ctx.checked_locations:
                continue
            
            addr = self.addresses.BITFIELD + floor(index / 8)
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

        return result

    async def _temp_check_ability_flags(self, ctx: SpyroAHTContext):
        # temporary function for testing, remove on release
        if 1 not in ctx.checked_locations:
            await self.set_ability_flag(consts.PlayerFlags.DoubleJump, False)
        if 17 not in ctx.checked_locations:
            breath = int.from_bytes(dolphin_memory_engine.read_bytes(self.addresses.ACTIVE_BREATH), 'big')
            if breath == consts.BREATH_ELECTRIC:
                await self.force_set_breath(consts.BREATH_FIRE)
            await self.set_ability_flag(consts.PlayerFlags.LightningBreath, False)
        if 33 not in ctx.checked_locations:
            await self.set_ability_flag(consts.PlayerFlags.PoleSpin, False)
        if 79 not in ctx.checked_locations:
            breath = int.from_bytes(dolphin_memory_engine.read_bytes(self.addresses.ACTIVE_BREATH), 'big')
            if breath == consts.BREATH_WATER:
                await self.force_set_breath(consts.BREATH_FIRE)
            await self.set_ability_flag(consts.PlayerFlags.WaterBreath, False)
        if 83 not in ctx.checked_locations:
            await self.set_ability_flag(consts.PlayerFlags.WingShield, False)
        if 136 not in ctx.checked_locations:
            breath = int.from_bytes(dolphin_memory_engine.read_bytes(self.addresses.ACTIVE_BREATH), 'big')
            if breath == consts.BREATH_ICE:
                await self.force_set_breath(consts.BREATH_FIRE)
            await self.set_ability_flag(consts.PlayerFlags.IceBreath, False)
        if 155 not in ctx.checked_locations:
            await self.set_ability_flag(consts.PlayerFlags.WallKick, False)
    
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
    
    async def force_set_breath(self, breath_id: int):
        dolphin_memory_engine.write_bytes(self.addresses.ACTIVE_BREATH, breath_id.to_bytes(4))


class SpyroAHTCommandProcessor(ClientCommandProcessor):
    ctx: SpyroAHTContext

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

    def make_gui(self) -> type[kvui.GameManager]:
        ui = super().make_gui()
        ui.base_title = "Spyro: A Hero's Tail Archipelago Client"
        return ui
    
    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect(game=self.game)
        self.auth_ready.set()
    
    async def send_connect(self, **kwargs) -> None:
        await super().send_connect(**kwargs)


async def dispatch_items(ctx: SpyroAHTContext):
    ctx.item_counts = Counter(i.item for i in ctx.items_received)
    for item in ctx.items_received:
        if item in ctx.synced_items:
            continue
        ctx.synced_items.add(item)
        match item.item:
            # case 0xB: # Swim
            # case 0xC: # Glide
            # case 0xD: # Charge
            case 0x1: # Double Jump
                await ctx.emu_client.set_ability_flag(consts.PlayerFlags.DoubleJump, True)
            case 0x2: # Pole Spin
                await ctx.emu_client.set_ability_flag(consts.PlayerFlags.PoleSpin, True)
            case 0x3: # Wing Shield
                await ctx.emu_client.set_ability_flag(consts.PlayerFlags.WingShield, True)
            case 0x4:
                await ctx.emu_client.set_ability_flag(consts.PlayerFlags.WallKick, True)
            # case 0xE: # Fire Breath
            case 0x5: # Lightning Breath
                await ctx.emu_client.set_ability_flag(consts.PlayerFlags.LightningBreath, True)
                await ctx.emu_client.force_set_breath(consts.BREATH_ELECTRIC)
            case 0x6: # Water Breath
                await ctx.emu_client.set_ability_flag(consts.PlayerFlags.WaterBreath, True)
                await ctx.emu_client.force_set_breath(consts.BREATH_WATER)
            case 0x7: # Ice Breath
                await ctx.emu_client.set_ability_flag(consts.PlayerFlags.IceBreath, True)
                await ctx.emu_client.force_set_breath(consts.BREATH_ICE)
            case 0x8: # Dark Gem
                count = await ctx.emu_client.get_item_count(ctx.emu_client.addresses.DARK_GEM_COUNT)
                if count < ctx.item_counts[0x8]:
                    await ctx.emu_client.add_item(ctx.emu_client.addresses.DARK_GEM_COUNT, 1)
            case 0x9:
                count = await ctx.emu_client.get_item_count(ctx.emu_client.addresses.LIGHT_GEM_COUNT)
                if count < ctx.item_counts[0x9]:
                    await ctx.emu_client.add_item(ctx.emu_client.addresses.LIGHT_GEM_COUNT, 1)
            case 0xA:
                count = await ctx.emu_client.get_item_count(ctx.emu_client.addresses.DRAGON_EGG_COUNT)
                if count < ctx.item_counts[0xA]:
                    await ctx.emu_client.add_item(ctx.emu_client.addresses.DRAGON_EGG_COUNT, 1)
            case _:
                logger.error(f"Unhandled item {item!r}")


starter_checks = {229, 230, 231, 232}


async def dispatch_locations(ctx: SpyroAHTContext):
    locations = await ctx.emu_client.scan_locations(ctx)

    for c in starter_checks:
        if c not in ctx.checked_locations:
            locations.add(c)

    if locations:
        await ctx.send_msgs([{"cmd":"LocationChecks","locations":locations}])


async def emu_loop(ctx: SpyroAHTContext):
    await ctx.emu_client.ready.wait()
    await ctx.auth_ready.wait()
    while not ctx.exit_event.is_set():
        try:
            await asyncio.wait_for(ctx.watcher_event.wait(), 1.0)
        except asyncio.TimeoutError:
            pass
        ctx.watcher_event.clear()

        if await ctx.emu_client.is_in_game() and not await ctx.emu_client.is_paused() and not await ctx.emu_client.is_loading():
            await dispatch_items(ctx)
            await dispatch_locations(ctx)
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

        #ctx.emu_loop = asyncio.create_task(emu_loop(ctx), name="EmuLoop")
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
