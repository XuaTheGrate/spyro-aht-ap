import struct
from dataclasses import dataclass
from enum import IntEnum, IntFlag
from typing import Literal

BREATH_FIRE = 0x1
BREATH_WATER = 0x2
BREATH_ICE = 0x4
BREATH_ELECTRIC = 0x8

DARK_GEM = 0x8
LIGHT_GEM = 0x9
DRAGON_EGG = 0xA

# https://discord.com/channels/619694339777495056/692182418429575260/1477821351879507998

# (AP location ID, bitfield offset)
LOCATIONS_BITFIELD: dict[int, int] = {
    2: 65, 3: 66, 4: 70, 5: 73, 6: 74, 7: 76,
    8: 72, 9: 71, 10: 69, 11: 67, 12: 68,
    13: 181, 14: 182, 15: 77, 16: 75, 18: 48,
    19: 61, 20: 57, 21: 56, 22: 60, 23: 59,
    24: 62, 25: 55, 26: 51, 27: 49, 28: 53,
    29: 63, 30: 185, 31: 186, 32: 58, 34: 52,
    35: 64, 36: 50, 37: 183, 38: 184, 39: 54,
    40: 45, 41: 34, 42: 32, 43: 31, 44: 33,
    45: 35, 46: 36, 47: 44, 48: 187, 49: 188,
    50: 38, 51: 46, 52: 47, 53: 43, 54: 42,
    55: 40, 56: 37, 57: 41, 58: 39, 59: 155,
    60: 153, 61: 156, 62: 157, 63: 191, 64: 192,
    65: 146, 66: 147, 67: 148, 68: 145, 69: 158,
    70: 150, 71: 193, 72: 189, 73: 190, 74: 152,
    75: 151, 76: 154, 77: 159, 78: 149, 80: 19,
    81: 15, 82: 23, 84: 21, 85: 20, 86: 22,
    87: 27, 88: 26, 89: 25, 90: 24, 91: 28,
    92: 18, 93: 196, 94: 197, 95: 17, 96: 16,
    97: 30, 98: 29, 99: 7, 100: 3, 101: 5, 102: 8,
    103: 9, 104: 0, 105: 194, 106: 195, 107: 2,
    108: 10, 109: 1, 110: 13, 111: 4, 112: 11,
    113: 6, 114: 14, 115: 12, 116: 89, 117: 200,
    118: 201, 119: 101, 120: 94, 121: 102, 122: 95,
    123: 98, 124: 198, 125: 199, 172: 99, 126: 90,
    127: 91, 128: 105, 129: 92, 130: 96, 131: 97,
    132: 93, 133: 104, 134: 100, 135: 103, 137: 130,
    138: 204, 139: 121, 140: 129, 141: 120, 142: 122,
    143: 126, 144: 127, 145: 124, 146: 202, 147: 203,
    148: 128, 149: 125, 150: 123, 151: 209, 152: 106,
    153: 119, 154: 107, 156: 117, 157: 108, 158: 109,
    159: 111, 160: 205, 161: 206, 162: 207, 163: 113,
    164: 116, 165: 115, 166: 112, 167: 114, 168: 208,
    169: 210, 170: 110, 171: 118, 173: 143, 174: 144,
    175: 211, 176: 212, 177: 142, 178: 167, 179: 215,
    180: 162, 181: 213, 182: 214, 183: 168, 184: 160,
    185: 161, 186: 163, 187: 164, 188: 170, 189: 166,
    190: 169, 191: 165, 192: 172, 193: 171, 194: 173,
    195: 175, 196: 174, 197: 176, 198: 177, 199: 180,
    200: 179, 201: 178, 202: 216, 203: 217, 204: 79,
    205: 83, 206: 86, 207: 87, 208: 80, 209: 78, 210: 218,
    211: 219, 212: 88, 213: 82, 214: 84, 215: 81, 216: 85,
    217: 140, 218: 136, 219: 134, 220: 138, 221: 137,
    222: 135, 223: 139, 224: 141, 225: 132, 226: 131, 227: 133,
    234: 221, 235: 220, 236: 223, 237: 222, 238: 225, 239: 226,
    240: 230, 241: 227, 242: 228, 243: 229, 244: 224, 245: 234,
    246: 233, 247: 232, 248: 235, 249: 231, 250: 236, 251: 237,
    252: 238, 253: 239, 254: 240
}

LOCATIONS_OBJECTIVE: dict[int, int] = {
    0x44000001: 1,   # Dragon Village: Double Jump from Elder Tomas
    0x44000081: 17,  # Dragon Village: Lightning Breath from Gnasty Gnorc
    0x44000003: 33,  # Crocovile Swamp: Pole Spin from Elder Magnus
    0x44000082: 79,  # Coastal Remains: Water Breath from Ineptune
    0x4400009d: 83,  # Cloudy Domain: Wing Shield from Elder Titan
    0x44000083: 136, # Frostbite Village: Ice Breath from Red
    0x4400009c: 155, # Ice Citadel: Wall Kick from Elder Astor
    0x44000084: 228, # Red's Laboratory: Defeat Mecha-Red
}


SCOUT_OBJECTIVES: dict[int, tuple[int, int]] = {
    0x44000017: (13, 14),
    0x44000013: (30, 31),
    0x4400000c: (37, 38),
    0x4400007b: (48, 49),

    0x4400001a: (63, 64),
    0x4400004b: (72, 73),
    0x440000a7: (93, 94),
    0x440000a5: (105, 106),

    0x4400008a: (117, 118),
    0x4400008f: (124, 125),
    0x440000aa: (146, 147),
    0x44000094: (160, 161),

    0x44000097: (175, 176),
    0x440000d1: (181, 182),
    0x440000bb: (202, 203),
    0x440000b6: (210, 211),
}


GOALS = [
    0x44000081, # Defeat Gnasty Gnorc
    0x44000082, # Defeat Ineptune
    0x44000083, # Defeat Red
    0x44000084  # Defeat Mecha-Red
]

#class GameState:
#    location_bitfield = 0x0
#    starting_breath = 0x30
#    starting_abilities = 0x34
#    skip_realm_intro_cutscene = 0x38
#    skip_cutscene_button = 0x39
#    allow_teleport_to_hub = 0x3A
#    allow_immediate_realm_access = 0x3B
#
#    init = 0x3C
#
#    xls_shop_sheetcount_ALWAYS_1 = 0x40
#    xls_shop_sheet_offset_ALWAYS_4 = 0x44
#    xls_shop_rowcount = 0x48


class AddressList:
    p_LOCATION_BITFIELD: int
    p_NUM_GEM_PACKS_RECEIVED: int
    p_NUM_LOCK_PICKS_RECEIVED: int
    p_INFINITE_BUTTERFLY_JAR: int
    p_SKIP_CUTSCENE_BUTTON: int
    p_ALLOW_TELEPORT_TO_HUB: int
    p_ALLOW_IMMEDIATE_REALM_ACCESS: int
    p_DISABLE_POPUPS: int
    p_PATCH_BEEN_WRITTEN_TO: int
    p_MW_SEED: int
    p_INIT: int
    p_BOSS_COSTS: int
    p_LG_DOOR_COSTS: int
    p_XLS_SHOP_SHEETCOUNT_ALWAYS_1: int
    p_XLS_SHOP_SHEET_OFFSET_ALWAYS_4: int
    p_XLS_SHOP_ROWCOUNT: int
    p_XLS_SHOP_ITEMS: int
    p_SHOP_TEXT: int

    g_LOCATION_BITFIELD: int
    g_NUM_GEM_PACKS_RECEIVED: int
    g_NUM_LOCKPICKS_RECEIVED: int
    g_INFINITE_BUTTERFLY_JAR: int
    g_DEATHLINK_RECV: int
    g_DEATHLINK_SEND: int
    g_SKIP_CUTSCENE_BUTTON: int
    g_ALLOW_TELEPORT_TO_HUB: int
    g_ALLOW_IMMEDIATE_REALM_ACCESS: int
    g_DISABLE_POPUPS: int
    g_PATCH_BEEN_WRITTEN_TO: int
    g_MW_SEED: int
    g_INIT: int
    g_BOSS_COSTS: int
    g_LG_DOOR_COSTS: int
    g_XLS_SHOP_SHEETCOUNT_ALWAYS_1: int
    g_XLS_SHOP_SHEET_OFFSET_ALWAYS_4: int
    g_XLS_SHOP_ROWCOUNT: int
    g_XLS_SHOP_ITEMS: int
    g_XLS_SHOP_TEXT: int

    n_AP_NOTIFICATION_COLOR: int
    n_AP_NOTIFICATION_TIMER: int
    n_AP_NOTIFICATION_TEXT_BUFFER: int

    OBJECTIVES: int
    DARK_GEM_COUNT: int
    LIGHT_GEM_COUNT: int
    DRAGON_EGG_COUNT: int

    GEMS: int
    TOTAL_GEMS: int

    LOCKPICKS: int

    ACTIVE_BREATH: int
    ABILITY_FLAGS: int
    IN_GAME: int
    PAUSE: int
    LOADING: int


class SLUS_20884(AddressList):
    pass


class SLES_52569(AddressList):
    pass


class G5SE7D(AddressList):
    p_LOCATION_BITFIELD = 0x803d8fa8
    p_NUM_GEM_PACKS_RECEIVED = 0x803d8fd8
    p_NUM_LOCK_PICKS_RECEIVED = 0x803d8fd9
    p_INFINITE_BUTTERFLY_JAR = 0x803d8fda
    p_SKIP_CUTSCENE_BUTTON = 0x803d8fdb
    p_ALLOW_TELEPORT_TO_HUB = 0x803d8fdc
    p_ALLOW_IMMEDIATE_REALM_ACCESS = 0x803d8fdd
    p_DISABLE_POPUPS = 0x803d8fde
    p_PATCH_BEEN_WRITTEN_TO = 0x803d8fdf
    p_MW_SEED = 0x803d8fe0
    p_INIT = 0x803d8fe4
    p_BOSS_COSTS = 0x803d8fe8
    p_LG_DOOR_COSTS = 0x803d8fec
    p_XLS_SHOP_SHEETCOUNT_ALWAYS_1 = 0x803d8ff0
    p_XLS_SHOP_SHEET_OFFSET_ALWAYS_4 = 0x803d8ff4
    p_XLS_SHOP_ROWCOUNT = 0x803d8ff8
    p_XLS_SHOP_ITEMS = 0x803d8ffc
    p_SHOP_TEXT = 0x803d99fc

    g_LOCATION_BITFIELD = 0x80467ce4
    g_NUM_GEM_PACKS_RECEIVED = 0x80467d14
    g_NUM_LOCKPICKS_RECEIVED = 0x80467d15
    g_INFINITE_BUTTERFLY_JAR = 0x80467d16
    g_DEATHLINK_RECV = NotImplemented
    g_DEATHLINK_SEND = NotImplemented
    g_SKIP_CUTSCENE_BUTTON = 0x80467d17
    g_ALLOW_TELEPORT_TO_HUB = 0x80467d18
    g_ALLOW_IMMEDIATE_REALM_ACCESS = 0x80467d19
    g_DISABLE_POPUPS = 0x80467d1a
    g_PATCH_BEEN_WRITTEN_TO = 0x80467d1b
    g_MW_SEED = 0x80467d1c
    g_INIT = 0x80467d20
    g_BOSS_COSTS = 0x80467d24
    g_LG_DOOR_COSTS = 0x80467d28
    g_XLS_SHOP_SHEETCOUNT_ALWAYS_1 = 0x80467d2c
    g_XLS_SHOP_SHEET_OFFSET_ALWAYS_4 = 0x80467d30
    g_XLS_SHOP_ROWCOUNT = 0x80467d34
    g_XLS_SHOP_ITEMS = 0x80467d38
    g_XLS_SHOP_TEXT = 0x80468738

    n_AP_NOTIFICATION_COLOR = 0x8029dbcc
    n_AP_NOTIFICATION_TIMER = 0x8029dbd0
    n_AP_NOTIFICATION_TEXT_BUFFER = 0x8029dbd4

    OBJECTIVES = 0x80465C88
    DARK_GEM_COUNT = 0x80465BB7
    LIGHT_GEM_COUNT = 0x80465BB6
    DRAGON_EGG_COUNT = 0x80465BB8

    GEMS = 0x80465B68
    TOTAL_GEMS = 0x80465B6C

    LOCKPICKS = 0x80465b70

    ACTIVE_BREATH = 0x80465B60
    ABILITY_FLAGS = 0x80465B88
    IN_GAME = 0x8046F344 
    PAUSE = 0x8046F378
    LOADING = 0x0


class AbilityFlags(IntFlag):
    DoubleJump = 0x1
    SparxHealthUpgrade = 0x4
    PoleSpin = 0x10
    IceBreath = 0x20
    LightningBreath = 0x40
    WaterBreath = 0x80
    DoubleGems = 0x200
    SuperchargeGadget = 0x1000
    InvincibilityGadget = 0x2000
    PurchasedLockpick = 0x4000
    WingShield = 0x8000
    WallKick = 0x10000
    Shockwave = 0x20000
    ButterflyJar = 0x40000
    FireBreath = 0x80000
    Glide = 0x100000
    Charge = 0x200000
    Swim = 0x400000


class ShopItemModel(IntEnum):
    Lockpick = 0x0200014c
    HealthUpgrade = 0x0200014b
    FireBomb = 0x02000077
    ElectricBomb = 0x020000a7
    WaterBomb = 0x02000114
    IceBomb = 0x020000a1
    FireMag = 0x0200023f
    ElectricMag = 0x0200023e
    WaterMag = 0x02000241
    IceMag = 0x02000240
    Keychain = 0x02000242
    ButterflyJar = 0x020001b1
    DoubleGems = 0x0200023a
    Shockwave = 0x0200023b
    TeleportTicket = 0x0200023c
    TeleportTicketMain = 0x0200023d


class TextEntry:
    base = 0x28010000

    def __init__(self, index: int, text: str):
        self.index = index
        self._text = text
        self.been_bought = False
    
    @property
    def address(self):
        return self.base + self.index

    @property
    def text(self):
        if len(self._text) >= 48:
            return self._text[:44] + "..."
        return self._text
    
    def to_bytes(self, byteorder: Literal['big', 'little'] = 'big'):
        return struct.pack(('<' if byteorder == 'little' else '>') + '?B48s', self.been_bought, 0, self.text.encode('ascii'))


@dataclass
class XLSShoppingItem:
    entity: ShopItemModel
    text: TextEntry
    cost: tuple[int, int] # [u16, u16] (base, remote)

    @property
    def structure(self) -> str:
        return "IIIIHHhhII"

    def to_bytes(self, byteorder: Literal['big', 'little'] = 'big'):
        return struct.pack(('<' if byteorder == 'little' else '>') + self.structure, 
                           self.entity, 0x01000028, self.text.address, self.text.address,
                           self.cost[0], self.cost[1], 1, 0, 0, 0)


