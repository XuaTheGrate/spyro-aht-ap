import asyncio
import json
import os.path
import ssl
from dataclasses import dataclass
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

        self.set_tasks()
        
    def set_tasks(self):
        if self._ap_task != None:
            raise RuntimeError("Attempted to duplicate AP task")
        if self._pine_task != None:
            raise RuntimeError("Attempted to duplicate Pine task")
        
        self._ap_task = asyncio.create_task(self._ap_loop(), name="AP Loop")
        self._pine_task = asyncio.create_task(self._pine_loop(), name="Pine Loop")
    
    async def _send_locations(self):
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

    async def _process_packet(self, payload: dict[str, Any]) -> None:
        match payload['cmd']:
            case "Connected":
                for k in payload['players']:
                    k.pop('class')
                payload['players'] = [NetworkPlayer(**k) for k in payload['players']]
                await self._websocket_connected_packet(WebsocketConnected(**payload))
            case _ as c:
                print(f"WARNING: Unhandled packet command '{c}'")

    async def _ap_loop(self):
        while not self.exit.is_set():
            packets = decode(await self._socket.recv()) # type:ignore
            for packet in packets:
                await self._process_packet(packet)
        await self._socket.close()
    
    async def _pine_loop(self):
        await self.ready.wait()
        while not self.exit.is_set():
            for loc, addr, orv in consts.LOCATIONS:
                if loc in self.checked_locations:
                    continue

                data = await self.pine.read_int8(addr)
                if data | orv == data:
                    print(f"Dispatching item 0x{loc:x} ({addr:x})")
                    self.checked_locations.add(loc)
                    await self._send_locations()
            
            await asyncio.sleep(1)
        self.pine.disconnect()
    
    async def close(self):
        self.exit.set()
        await asyncio.wait([self._pine_task, self._ap_task]) # type: ignore


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
