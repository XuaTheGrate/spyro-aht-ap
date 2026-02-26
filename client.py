import asyncio
import json
import os.path
import ssl
from collections import Counter
from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Literal

import websockets

import consts
from pcsx2_interface import Pine

encode = json.JSONEncoder(ensure_ascii=False,check_circular=False,separators=(',',':')).encode
decode = json.JSONDecoder().decode


def get_uuid() -> str: # https://github.com/ArchipelagoMW/Archipelago/blob/main/Utils.py#L423
    import platformdirs
    cache_dir = platformdirs.user_cache_dir("Archipelago", False)
    cache_file = os.path.join(cache_dir, "common.json")

    try:
        with open(cache_file) as f:
            common_file = json.load(f)
            uuid = common_file.get("uuid", None)
    except FileNotFoundError:
        common_file = {}
        uuid = None

    if uuid:
        return uuid

    from uuid import uuid4
    uuid = str(uuid4())
    common_file["uuid"] = uuid

    cache_folder = os.path.dirname(cache_file)
    os.makedirs(cache_folder, exist_ok=True)
    with open(cache_file, "w") as f:
        json.dump(common_file, f, separators=(",", ":"))
    return uuid


def get_ssl_context() -> ssl.SSLContext:
    import certifi
    return ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=certifi.where())


@dataclass
class NetworkPlayer:
    team: int
    slot: int
    alias: str
    name: str


@dataclass
class NetworkItem:
    item: int
    location: int
    player: int
    flags: int


@dataclass
class WebsocketConnected:
    cmd: Literal["Connected"]
    team: int
    slot: int
    players: list[NetworkPlayer]
    missing_locations: list[int]
    checked_locations: list[int]
    slot_info: dict[str, Any]
    hint_points: int
    slot_data: dict[str, Any]


class ClientStatus(IntEnum):
    UNKNOWN = 0
    CONNECTED = 5
    READY = 10
    PLAYING = 20
    GOAL = 30


# TODO: compression support
class APClient:
    def __init__(self, *,
                 loop: asyncio.AbstractEventLoop,
                 address: str = "archipelago.gg",
                 port: int = 38281,
                 slot: str,
                 password: str | None = None,
                 secure: bool = True,
                 pine: Pine | None = None):
        self.loop = loop
        self.address = address
        self.port = port
        self.slot = slot
        self.password = password
        self._socket: websockets.WebSocketClientProtocol
        self._use_secure_connection = secure

        self.pine = pine or Pine(loop)

        self.ready = asyncio.Event()
        self.exit = asyncio.Event()

        self.checked_locations: set[int] = set()
        
        self._pine_task: asyncio.Task | None = None
        self._ap_task: asyncio.Task | None = None

        # TODO: not the ideal way to re-sync items i think, but that is for future me to fix
        self.synced_items = Counter()
    
    def _connect_payload(self) -> str:
        return encode([{
            "cmd": "Connect",
            "password": self.password,
            "game": "Spyro: A Hero's Tail",
            "name": self.slot,
            "uuid": get_uuid(),
            "tags": ["AP"],
            "version": {"major":0,"minor":6,"build":6,"class":"Version"},
            "items_handling": 0b111
        }])
    
    async def connect(self) -> None:
        if not self.pine.is_connected():
            print("Connecting to PCSX2")
            await self.pine.connect()

        addr = f"ws{'s' if self._use_secure_connection else ''}://{self.slot}:{self.password}@{self.address}:{self.port}"

        print(f"Connecting to {self.address}:{self.port}")
        self._socket = await websockets.connect(addr, loop=self.loop, ping_timeout=None, ping_interval=None, ssl=get_ssl_context() if self._use_secure_connection else None, max_size=16*1024*1024)
        _roominfo = await self._socket.recv()
        print(f"Connecting to slot '{self.slot}'")
        await self._socket.send(self._connect_payload())
        #await self._socket.send("""[{"cmd":"GetDataPackage","games":["Spyro: A Hero's Tail"]}]""")

        self.set_tasks()
        
    def set_tasks(self):
        if self._ap_task != None:
            raise RuntimeError("Attempted to duplicate AP task")
        if self._pine_task != None:
            raise RuntimeError("Attempted to duplicate Pine task")
        
        self._ap_task = asyncio.create_task(self._ap_loop(), name="AP Loop")
        self._pine_task = asyncio.create_task(self._pine_loop(), name="Pine Loop")
    
    async def _send_locations(self):
        if len(self.checked_locations) == 0: return

        print(f"Sending {len(self.checked_locations)} locations")
        payload = encode([{
            "cmd": "LocationChecks",
            "locations": list(self.checked_locations)
        }])
        await self._socket.send(payload)
    
    async def _websocket_connected_packet(self, packet: WebsocketConnected):
        self.checked_locations |= set(packet.checked_locations)
        await self._send_locations()
        print(f"Synced {len(self.checked_locations)} locations")
        self.ready.set()
        await self.send_status_update(ClientStatus.PLAYING)
    
    async def _received_item(self, item: NetworkItem) -> None:
        # TODO: add prompt to in game via Trina
        print(f"Received item {item.item:x}")
        match item.item:
            case 0x1: # Double Jump
                await self.set_store_item(consts.ITEM_STORAGE_DOUBLE_JUMP)
                await self.set_player_flag(consts.PlayerFlags.DoubleJump, True)
            case 0x2: # Pole Spin:
                await self.set_store_item(consts.ITEM_STORAGE_POLE_SPIN)
                await self.set_player_flag(consts.PlayerFlags.PoleSpin, True)
            case 0x5: # Lightning Breath
                await self.set_store_item(consts.ITEM_STORAGE_ELECTRIC_BREATH)
                await self.set_player_flag(consts.PlayerFlags.LightningBreath, True)
                await self.force_set_breath(consts.BREATH_ELECTRIC)
            case 0x8: # Dark Gem
                count = await self.get_item_count(consts.DARK_GEM_COUNT)
                if count < self.synced_items[0x8]:
                    await self.add_dark_gem()
            case 0x9: # Light Gem
                count = await self.get_item_count(consts.LIGHT_GEM_COUNT)
                if count < self.synced_items[0x9]:
                    await self.add_light_gem()
            case 0xA: # Dragon Egg
                count = await self.get_item_count(consts.DRAGON_EGG_COUNT)
                if count < self.synced_items[0xA]:
                    await self.add_dragon_egg()

    async def _process_packet(self, payload: dict[str, Any]) -> None:
        match payload['cmd']:
            case "Connected":
                for k in payload['players']:
                    k.pop('class')
                payload['players'] = [NetworkPlayer(**k) for k in payload['players']]
                await self._websocket_connected_packet(WebsocketConnected(**payload))
            case "PrintJSON":
                print(f"Archipelago: {payload['data']}")
            case "ReceivedItems":
                for i in payload['items']:
                    self.synced_items[i['item']] += 1
                    i.pop("class")
                    ni = NetworkItem(**i)
                    await self._received_item(ni)
            case _ as c:
                print(f"WARNING: Unhandled packet command '{c}'")

    async def _ap_loop(self):
        while not self.exit.is_set():
            packets = decode(await self._socket.recv()) # type:ignore
            for packet in packets:
                await self._process_packet(packet)
        await asyncio.wait_for(self._socket.close(), 3.0)
    
    async def _pine_loop(self):
        await self.ready.wait()
        while not self.exit.is_set():
            for loc, item_type, addr, orv in consts.LOCATIONS:
                if loc in self.checked_locations:
                    continue

                if addr == 0x0:
                    print(f"Dispatching location 0x{loc:x} as address is blank")
                    self.checked_locations.add(loc)
                    await self._send_locations()
                    continue

                data = await self.pine.read_int8(addr)
                if data | orv == data:
                    print(f"Dispatching item 0x{loc:x} ({addr:x})")
                    self.checked_locations.add(loc)
                    await self.remove_item(item_type)
                    await self._send_locations()

                    if loc == 0x11: # TODO: remove temporary victory condition
                        print(f"Dispatching victory")
                        await self.send_status_update(ClientStatus.GOAL)
            
            await asyncio.sleep(1)
        self.pine.disconnect()
    
    async def close(self):
        self.exit.set()
        await asyncio.wait([self._pine_task, self._ap_task]) # type: ignore
    
    async def send_status_update(self, status: ClientStatus) -> None:
        print(f"Sending status: {status!r}")
        await self._socket.send(encode([{"cmd": "StatusUpdate", "status": int(status)}]))
    
    async def set_player_flag(self, flag: consts.PlayerFlags, to: bool):
        flags = consts.PlayerFlags(await self.pine.read_int32(consts.PLAYER_FLAGS))
        if to:
            await self.pine.write_int32(consts.PLAYER_FLAGS, flags | flag)
        else:
            await self.pine.write_int32(consts.PLAYER_FLAGS, flags & ~flag)
    
    async def remove_item(self, item: int):
        print(f"Early removing {item:x}")
        match item:
            case 0x1: # Double Jump
                if not await self.should_have_item(consts.ITEM_STORAGE_DOUBLE_JUMP):
                    await self.set_player_flag(consts.PlayerFlags.DoubleJump, False)
            case 0x2: # Pole Spin
                if not await self.should_have_item(consts.ITEM_STORAGE_POLE_SPIN):
                    await self.set_player_flag(consts.PlayerFlags.PoleSpin, False)
            case 0x5: # Lightning Breath
                # TODO: add temporary electric breath support for leaving boss dungeons
                # or alternatively a key combo to tp out
                if not await self.should_have_item(consts.ITEM_STORAGE_ELECTRIC_BREATH):
                    await self.set_player_flag(consts.PlayerFlags.LightningBreath, False)
                    await self.force_set_breath(consts.BREATH_FIRE)
            case 0x8: # Dark Gem
                await self.add_dark_gem(-1)
            case 0x9: # Light Gem
                await self.add_light_gem(-1)
            case 0xA: # Dragon Egg
                await self.add_dragon_egg(-1)
    
    async def set_store_item(self, key: tuple[int, int]):
        flag = await self.pine.read_int8(consts.ITEM_STORAGE + key[0])
        await self.pine.write_int8(consts.ITEM_STORAGE + key[0], flag | key[1])
    
    async def should_have_item(self, key: tuple[int, int]) -> bool:
        flag = await self.pine.read_int8(consts.ITEM_STORAGE + key[0])
        return flag & key[1] == key[1]

    async def get_item_count(self, addr: int):
        return await self.pine.read_int8(addr)
    
    async def add_dark_gem(self, amount: int = 1):
        count = await self.get_item_count(consts.DARK_GEM_COUNT)
        await self.pine.write_int8(consts.DARK_GEM_COUNT, count + amount)
    
    async def add_light_gem(self, amount: int = 1):
        count = await self.get_item_count(consts.LIGHT_GEM_COUNT)
        await self.pine.write_int8(consts.LIGHT_GEM_COUNT, count + amount)
    
    async def add_dragon_egg(self, amount: int = 1):
        count = await self.get_item_count(consts.DRAGON_EGG_COUNT)
        await self.pine.write_int8(consts.DRAGON_EGG_COUNT, count + amount)
    
    async def force_set_breath(self, breath_id: int):
        await self.pine.write_int8(consts.ACTIVE_BREATH, breath_id)


async def main():
    loop = asyncio.get_running_loop()
    client = APClient(loop=loop, address="localhost", slot="MayaXTG", secure=False)
    await client.connect()
    try:
        while True:
            await asyncio.sleep(1)
    finally:
        await client.close()


if __name__ == '__main__':
    asyncio.run(main())
