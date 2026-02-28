from __future__ import annotations

import asyncio
from collections import Counter, defaultdict

import Utils
from CommonClient import ClientCommandProcessor, CommonContext, logger, server_loop, gui_enabled, get_base_parser
from NetUtils import ClientStatus, NetworkItem

import consts
import kvui
from pcsx2_interface import Pine


class GenericClient:
    ready: asyncio.Event
    @property
    def is_connected(self) -> bool: ...
    async def connect(self): ...
    async def disconnect(self): ...
    async def is_in_game(self) -> bool: ...
    async def is_paused(self) -> bool: ...
    async def is_loading(self) -> bool: ...
    async def scan_locations(self, ctx: SpyroAHTContext) -> set[int]: ...
    async def _remove_item(self, item: int): ...
    async def store_item(self, tag: tuple[int, int]): ...
    async def should_have_item(self, tag: tuple[int, int]) -> bool: ...
    async def set_player_flag(self, flag: int, to: bool): ...
    async def get_item_count(self, addr: int) -> int: ...
    async def add_item(self, addr: int, count: int): ...
    async def force_set_breath(self, breath_id: int): ...


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
        self.ready.set()
        logger.info("PCSX2 connection established")
    
    async def disconnect(self):
        if self.pine.is_connected():
            self.ready.clear()
            self.pine.disconnect()

    async def is_in_game(self) -> bool:
        return await self.pine.read_int32(consts.IN_GAME) == 1
    
    async def is_paused(self) -> bool:
        return await self.pine.read_int32(consts.PAUSE) == 1
    
    async def is_loading(self) -> bool:
        return await self.pine.read_int32(consts.LOADING) == 1
    
    async def scan_locations(self, ctx: SpyroAHTContext) -> set[int]:
        result: set[int] = set()
        for location, item_type, address, or_value in consts.LOCATIONS:
            if location in ctx.checked_locations:
                continue

            if address == 0x0:
                result.add(location)
            
            data = await self.pine.read_int8(address)
            if data | or_value == data:
                result.add(location)
                # TODO: remove this as the function that adds items should be patched in release
                await self._remove_item(item_type)
                if location == 0x11:
                    if not ctx.finished_game:
                        await ctx.send_msgs([{"cmd":"StatusUpdate","status":ClientStatus.CLIENT_GOAL}])
                        ctx.finished_game = True
        return result
    
    async def _remove_item(self, item: int):
        match item:
            case 0x1:
                if not await self.should_have_item(consts.ITEM_STORAGE_DOUBLE_JUMP):
                    await self.set_player_flag(consts.PlayerFlags.DoubleJump, False)
            case 0x2:
                if not await self.should_have_item(consts.ITEM_STORAGE_POLE_SPIN):
                    await self.set_player_flag(consts.PlayerFlags.PoleSpin, False)
            case 0x5:
                if not await self.should_have_item(consts.ITEM_STORAGE_ELECTRIC_BREATH):
                    await self.set_player_flag(consts.PlayerFlags.LightningBreath, False)
            case 0x8:
                await self.add_item(consts.DARK_GEM_COUNT, -1)
            case 0x9:
                await self.add_item(consts.LIGHT_GEM_COUNT, -1)
            case 0xA:
                await self.add_item(consts.DRAGON_EGG_COUNT, -1)
    
    async def store_item(self, tag: tuple[int, int]):
        flag = await self.pine.read_int8(consts.ITEM_STORAGE + tag[0])
        await self.pine.write_int8(consts.ITEM_STORAGE + tag[0], flag | tag[1])
    
    async def should_have_item(self, tag: tuple[int, int]) -> bool:
        return await self.pine.read_int8(consts.ITEM_STORAGE + tag[0]) & tag[1] == tag[1]
    
    async def set_player_flag(self, flag: int, to: bool):
        flags = await self.pine.read_int32(consts.PLAYER_FLAGS)
        if to:
            await self.pine.write_int32(consts.PLAYER_FLAGS, flags | flag)
        else:
            await self.pine.write_int32(consts.PLAYER_FLAGS, flags & ~flag)
    
    async def get_item_count(self, addr: int) -> int:
        return await self.pine.read_int8(addr)
    
    async def add_item(self, addr: int, count: int):
        c = await self.get_item_count(addr)
        if c == 0 and count < 0:
            logger.warning(f"Attempted to set negative value for 0x00{addr:x}")
            return
        await self.pine.write_int8(addr, count + c)
    
    async def force_set_breath(self, breath_id: int):
        await self.pine.write_int8(consts.ACTIVE_BREATH, breath_id)


class DolphinClient(GenericClient):
    pass


class SpyroAHTCommandProcessor(ClientCommandProcessor):
    ctx: SpyroAHTContext

    def _cmd_client(self, client: str = "") -> bool:
        """
        Assign the used emulator client. Should be one of 'pcsx2' or 'dolphin'.
        """
        if not client or client.lower() not in ('pcsx2', 'dolphin'):
            self.output("Please specify 'pcsx2' or 'dolphin' as your client.")
            return False

        if client.lower() == 'pcsx2':
            self.ctx.emu_client = PCSX2Client()
        elif client.lower() == 'dolphin':
            raise NotImplementedError
        
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
            case 0x1: # Double Jump
                await ctx.emu_client.store_item(consts.ITEM_STORAGE_DOUBLE_JUMP)
                await ctx.emu_client.set_player_flag(consts.PlayerFlags.DoubleJump, True)
            case 0x2: # Pole Spin
                await ctx.emu_client.store_item(consts.ITEM_STORAGE_POLE_SPIN)
                await ctx.emu_client.set_player_flag(consts.PlayerFlags.PoleSpin, True)
            case 0x5: # Lightning Breath
                await ctx.emu_client.store_item(consts.ITEM_STORAGE_ELECTRIC_BREATH)
                await ctx.emu_client.set_player_flag(consts.PlayerFlags.LightningBreath, True)
                await ctx.emu_client.force_set_breath(consts.BREATH_ELECTRIC)
            case 0x8: # Dark Gem
                count = await ctx.emu_client.get_item_count(consts.DARK_GEM_COUNT)
                if count < ctx.item_counts[0x8]:
                    await ctx.emu_client.add_item(consts.DARK_GEM_COUNT, 1)
            case 0x9:
                count = await ctx.emu_client.get_item_count(consts.LIGHT_GEM_COUNT)
                if count < ctx.item_counts[0x9]:
                    await ctx.emu_client.add_item(consts.LIGHT_GEM_COUNT, 1)
            case 0xA:
                count = await ctx.emu_client.get_item_count(consts.DRAGON_EGG_COUNT)
                if count < ctx.item_counts[0xA]:
                    await ctx.emu_client.add_item(consts.DRAGON_EGG_COUNT, 1)


async def dispatch_locations(ctx: SpyroAHTContext):
    locations = await ctx.emu_client.scan_locations(ctx)
    locations = locations.difference(ctx.checked_locations)
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
