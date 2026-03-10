from enum import IntFlag

BREATH_FIRE = 0x1
BREATH_WATER = 0x2
BREATH_ICE = 0x4
BREATH_ELECTRIC = 0x8

DARK_GEM = 0x8
LIGHT_GEM = 0x9
DRAGON_EGG = 0xA

ITEM_STORAGE_DOUBLE_JUMP = (0x0, 0x1)
ITEM_STORAGE_POLE_SPIN = (0x0, 0x2)
ITEM_STORAGE_ELECTRIC_BREATH = (0x0, 0x4)

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
    222: 135, 223: 139, 224: 141, 225: 132, 226: 131, 227: 133
}

LOCATIONS_OBJECTIVE: dict[int, int] = {
    0x44000001: 1,   # Dragon Village: Double Jump from Elder Tomas
    0x44000081: 17,  # Dragon Village: Lightning Breath from Gnasty Gnorc
    0x44000003: 33,  # Crocoville Swamp: Pole Spin from Elder Magnus
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
    0x44000084 # Defeat Mecha-Red
]


class AddressList:
    BITFIELD: int
    OBJECTIVES: int
    DARK_GEM_COUNT: int
    LIGHT_GEM_COUNT: int
    DRAGON_EGG_COUNT: int
    ACTIVE_BREATH: int
    ABILITY_FLAGS: int
    IN_GAME: int
    PAUSE: int
    LOADING: int


class SLUS_20884(AddressList):
    BITFIELD = 0x503280
    OBJECTIVES = NotImplemented
    DARK_GEM_COUNT = 0x502057
    LIGHT_GEM_COUNT = 0x502056
    DRAGON_EGG_COUNT = 0x502058
    ACTIVE_BREATH = 0x502000
    ABILITY_FLAGS = 0x502028
    IN_GAME = 0x50f790
    PAUSE = 0x590764
    LOADING = 0x598690


class G5SE7D(AddressList):
    BITFIELD = 0x80467CE4
    OBJECTIVES = 0x80465C88
    DARK_GEM_COUNT = 0x80465BB7
    LIGHT_GEM_COUNT = 0x80465BB6
    DRAGON_EGG_COUNT = 0x80465BB8
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
