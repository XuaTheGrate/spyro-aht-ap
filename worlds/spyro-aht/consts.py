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
    # 1: 0,   # Dragon Village: Double Jump from Elder Tomas
    2: 65,    # Dragon Village: Dark Gem by Ember
    3: 66,    # Dragon Village: Dark Gem by Elder Tomas
    4: 70,    # Dragon Village: Dragon Egg after Hunter
    5: 73,    # Dragon Village: Light Gem in Nursery
    6: 74,    # Dragon Village: Locked Chest near Ball Gadget
    7: 76,    # Dragon Village: Locked Chest on cliff
    8: 72,    # Dragon Village: Dragon Egg behind breakable wall
    9: 71,    # Dragon Village: Light Gem above Lab Secret Entrance
    10: 69,   # Dragon Village: Light Gem across timed platforms
    11: 67,   # Dragon Village: Dark Gem by Sgt. Byrd
    12: 68,   # Dragon Village: Dragon Egg behind Dark Gem by Sgt. Byrd
    13: 181,  # Dragon Village: Dragon Egg from Sgt. Byrd
    14: 182,  # Dragon Village: Light Gem from Sgt. Byrd
    15: 77,   # Dragon Village: Locked Chest before Crocoville Swamp
    16: 75,   # Dragon Village: Dragon Egg in Gnastys Lair
    # 17: 0,  # Dragon Village: Lightning Breath from Gnasty Gnorc

    18: 48,   # Crocoville Swamp: Dark Gem by Moneybags platform
    19: 61,   # Crocoville Swamp: Locked Chest behind breakable wall
    20: 57,   # Crocoville Swamp: Dragon Egg across platforms in mud
    21: 56,   # Crocoville Swamp: Light Gem behind reinforced door
    22: 60,   # Crocoville Swamp: Light Gem on top of pyramid
    23: 59,   # Crocoville Swamp: Locked Chest near Dogs
    24: 62,   # Crocoville Swamp: Locked Chest in Temple
    25: 55,   # Crocoville Swamp: Light Gem in Temple
    26: 51,   # Crocoville Swamp: Light Gem in secret room
    27: 49,   # Crocoville Swamp: Dragon Egg from thief in temple
    28: 53,   # Crocoville Swamp: Light Gem after platforming
    29: 63,   # Crocoville Swamp: Dragon Egg after pole spin left
    30: 185,  # Crocoville Swamp: Dragon Egg from Blink
    31: 186,  # Crocoville Swamp: Light Gem from Blink
    32: 58,   # Crocoville Swamp: Dark Gem before Elder Magnus
    # 33: 0,  # Crocoville Swamp: Pole Spin from Elder Magnus
    34: 52,   # Crocoville Swamp: Dragon Egg in Elder Magnus' house
    35: 64,   # Crocoville Swamp: Light Gem in Elder Magnus' house
    36: 50,   # Crocoville Swamp: Dark Gem above Blink
    37: 183,  # Crocoville Swamp: Dragon Egg from Fredneck
    38: 184,  # Crocoville Swamp: Light Gem from Fredneck
    39: 54,   # Crocoville Swamp: Light Gem across the lilypads

    40: 45,   # Dragonfly Falls: Locked Chest near Ball Gadget
    41: 34,   # Dragonfly Falls: Dark Gem behind breakable wall
    42: 32,   # Dragonfly Falls: Dragon Egg after Dark Gem behind breakable wall
    43: 31,   # Dragonfly Falls: Light Gem behind reinforced wall
    44: 33,   # Dragonfly Falls: Dark Gem near vultures
    45: 35,   # Dragonfly Falls: Dragon Egg in vultures nest
    46: 36,   # Dragonfly Falls: Dark Gem before large pool
    47: 44,   # Dragonfly Falls: Light Gem behind breakable wall in large pool
    48: 187,  # Dragonfly Falls: Dragon Egg from Sparx
    49: 188,  # Dragonfly Falls: Light Gem from Sparx
    50: 38,   # Dragonfly Falls: Dragon Egg behind breakable wall above wall kick
    51: 46,   # Dragonfly Falls: Light Gem beyond Piranha Pool
    52: 47,   # Dragonfly Falls: Locked Chest in Piranha Pool
    53: 43,   # Dragonfly Falls: Dragon Egg in vultures nest (Hunter)
    54: 42,   # Dragonfly Falls: Complete Hunters trial
    55: 40,   # Dragonfly Falls: Dark Gem at end of zone
    56: 37,   # Dragonfly Falls: Light Gem behind breakable wall beyond 70 Light Gem door
    57: 41,   # Dragonfly Falls: Dragon Egg from thief beyond 70 Light Gem door
    58: 39    # Dragonfly Falls: Light Gem glide from wall kick
}

LOCATIONS_OBJECTIVE: dict[int, int] = {
    0x44000001: 1,   # Dragon Village: Double Jump from Elder Tomas
    0x44000081: 17,  # Dragon Village: Lightning Breath from Gnasty Gnorc
    0x44000003: 33   # Crocoville Swamp: Pole Spin from Elder Magnus
}


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
    LOADING = 0x0 # unnecessary


class PlayerFlags(IntFlag):
    DoubleJump = 0x1
    #UNUSED = 0x2
    SparxHealthUpgrade = 0x4
    #UNUSED = 0x8
    PoleSpin = 0x10
    IceBreath = 0x20
    LightningBreath = 0x40
    WaterBreath = 0x80
    #UNUSED = 0x100
    DoubleGems = 0x200
    #UNUSED = 0x400
    #UNUSED = 0x800
    SuperchargeGadget = 0x1000
    InvincibilityGadget = 0x2000
    PurchasedLockpick = 0x4000
    WingShield = 0x8000
    WallKick = 0x10000
    Shockwave = 0x20000
    ButterflyJar = 0x40000
    #UNUSED = 0x80000
