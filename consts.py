from enum import IntFlag

MD5 = '4a8320b24738334127b29de343c534ae'
IDN = 'SLUS_208.84'

# Items are stored at 0x503280
# the first tuple item is an offset from this address in multiples of 2
# the second item is the bit flag (0x1 - 0x80)
ITEM_STORAGE = 0x503280
ITEM_STORAGE_DOUBLE_JUMP = (0x0, 0x1)
ITEM_STORAGE_POLE_SPIN = (0x0, 0x2)
ITEM_STORAGE_ELECTRIC_BREATH = (0x0, 0x4)

DARK_GEM_COUNT = 0x502057
LIGHT_GEM_COUNT = 0x502056
DRAGON_EGG_COUNT = 0x502058

ACTIVE_BREATH = 0x502000
BREATH_FIRE = 0x1
BREATH_WATER = 0x2
BREATH_ICE = 0x4
BREATH_ELECTRIC = 0x8

DARK_GEM = 0x8
LIGHT_GEM = 0x9
DRAGON_EGG = 0xA

PLAYER_FLAGS = 0x502028


class PlayerFlags(IntFlag):
    DoubleJump = 0x1
    UNUSED_1 = 0x2
    SparxHealthUpgrade = 0x4
    UNDETERMINED_1 = 0x8
    PoleSpin = 0x10
    IceBreath = 0x20
    LightningBreath = 0x40
    WaterBreath = 0x80
    UNUSED_2 = 0x100
    DoubleGems = 0x200
    UNUSED_3 = 0x400
    UNUSED_4 = 0x800
    SuperchargeGadget = 0x1000
    InvincibilityGadget = 0x2000
    LOCKPICK_FLAG = 0x4000
    WingShield = 0x8000
    WallKick = 0x10000
    Shockwave = 0x20000
    ButterflyJar = 0x40000
    UNUSED_5 = 0x80000


NOP_ADDR = [
	(0x96de0, b'\x01\x00\x42\x34', b'\x00\x00\x00\x00') # disable double jump from elder tomas
]


LOCATIONS = {
	(0x1, 0x1, 0x5021b5, 0x80),         # Dragon Village: Double Jump/Horn Dive from Elder Tomas
	(0x2, DARK_GEM, 0x502775, 0x2),     # Dragon Village: Dark Gem by Elder Tomas
	(0x3, DARK_GEM, 0x502774, 0x80),    # Dragon Village: Dark Gem by Ember
	(0x4, DRAGON_EGG, 0x502782, 0x2),   # Dragon Village: Dragon Egg after Hunter
	(0x5, LIGHT_GEM, 0x5027c6, 0x80),   # Dragon Village: Light Gem in Nursery
	(0x6, DRAGON_EGG, 0x5027c9, 0x18),  # Dragon Village: Locked Chest near Ball Gadget
	(0x7, LIGHT_GEM, 0x5027cf, 0x6),    # Dragon Village: Locked Chest on cliff
	(0x8, DRAGON_EGG, 0x502792, 0x8),   # Dragon Village: Dragon Egg behind breakable wall
	(0x9, LIGHT_GEM, 0x502791, 0x80),   # Dragon Village: Light Gem above Lab Secret Entrance
	(0xA, LIGHT_GEM, 0x502777, 0x4),    # Dragon Village: Light Gem across timed platforms
	(0xB, DARK_GEM, 0x502775, 0x40),    # Dragon Village: Dark Gem by Sgt. Byrd
	(0xC, DRAGON_EGG, 0x502776, 0x40),  # Dragon Village: Dragon Egg behind Dark Gem by Sgt. Byrd
	(0xD, DRAGON_EGG, 0x000000, 0x0),   # Dragon Village: Dragon Egg from Sgt. Byrd
	(0xE, LIGHT_GEM, 0x000000, 0x0),    # Dragon Village: Light Gem from Sgt. Byrd
	(0xF, LIGHT_GEM, 0x5027d0, 0x6),    # Dragon Village: Locked Chest before Crocoville Swamp
    (0x10, DRAGON_EGG, 0x5027ce, 0x80), # Dragon Village: Dragon Egg in Gnastys Lair
    (0x11, 0x5, 0x502175, 0x8),         # Dragon Village: Lightning Breath from Gnasty Gnorc

    (0x12, DARK_GEM, 0x5027ed, 0x2),    # Crocoville Swamp: Dark Gem by Moneybags platform
    (0x13, LIGHT_GEM, 0x502841, 0x1),   # Crocoville Swamp: Locked Chest behind breakable wall
    (0x14, DRAGON_EGG, 0x502820, 0x8),  # Crocoville Swamp: Dragon Egg across platforms in mud
    (0x15, LIGHT_GEM, 0x50281F, 0x4),   # Crocoville Swamp: Light Gem behind reinforced door
    (0x16, LIGHT_GEM, 0x502840, 0x20),  # Crocoville Swamp: Light Gem on top of pyramid
    (0x17, DRAGON_EGG, 0x502833, 0x2),  # Crocoville Swamp: Locked Chest near Dogs
    (0x18, DRAGON_EGG, 0x502847, 0x2),  # Crocoville Swamp: Locked Chest in Temple
    (0x19, LIGHT_GEM, 0x50281a, 0x4),   # Crocoville Swamp: Light Gem in Temple
    (0x1A, LIGHT_GEM, 0x50280f, 0x8),   # Crocoville Swamp: Light Gem in secret room
    (0x1B, DRAGON_EGG, 0x5027ed, 0x8),  # Crocoville Swamp: Dragon Egg from thief in temple
    (0x1C, LIGHT_GEM, 0x502819, 0x4),   # Crocoville Swamp: Light Gem after platforming
    (0x1D, DRAGON_EGG, 0x502848, 0x2),  # Crocoville Swamp: Dragon Egg after pole spin left
    (0x1E, DRAGON_EGG, 0x000000, 0x0),  # Crocoville Swamp: Dragon Egg from Blink
    (0x1F, LIGHT_GEM, 0x000000, 0x0),   # Crocoville Swamp: Light Gem from Blink
    (0x20, DARK_GEM, 0x502820, 0x20),   # Crocoville Swamp: Dark Gem before Elder Magnus
    (0x21, 0x2, 0x5021e9, 0x1),         # Crocoville Swamp: Pole Spin from Elder Magnus
    (0x22, DRAGON_EGG, 0x502816, 0x2),  # Crocoville Swamp: Dragon Egg in Elder Magnus' house
    (0x23, LIGHT_GEM, 0x502848, 0x8),   # Crocoville Swamp: Light Gem in Elder Magnus' house
    (0x24, DARK_GEM, 0x50280e, 0x80),   # Crocoville Swamp: Dark Gem above Blink
    (0x25, DRAGON_EGG, 0x000000, 0x0),  # Crocoville Swamp: Dragon Egg from Fredneck
    (0x26, LIGHT_GEM, 0x000000, 0x0),   # Crocoville Swamp: Light Gem from Fredneck
    (0x27, LIGHT_GEM, 0x502819, 0x10),  # Crocoville Swamp: Light Gem across the lilypads

    (0x28, LIGHT_GEM, 0x502961, 0x4),   # Dragonfly Falls: Locked Chest near Ball Gadget
    (0x29, DARK_GEM, 0x50288a, 0x80),   # Dragonfly Falls: Dark Gem behind breakable wall
    (0x2A, DRAGON_EGG, 0x50288a, 0x2),  # Dragonfly Falls: Dragon Egg after Dark Gem behind breakable wall
    (0x2B, LIGHT_GEM, 0x502888, 0x8),   # Dragonfly Falls: Light Gem behind reinforced wall
    (0x2C, DARK_GEM, 0x50288a, 0x8),    # Dragonfly Falls: Dark Gem near vultures
    (0x2D, DRAGON_EGG, 0x50288b, 0x2),  # Dragonfly Falls: Dragon Egg in vultures nest
    (0x2E, DARK_GEM, 0x50288b, 0x80),   # Dragonfly Falls: Dark Gem before large pool
    (0x2F, LIGHT_GEM, 0x5028bb, 0x4),   # Dragonfly Falls: Light Gem behind breakable wall in large pool
    (0x30, DRAGON_EGG, 0x000000, 0x0),  # Dragonfly Falls: Dragon Egg from Sparx
    (0x31, LIGHT_GEM, 0x000000, 0x0),   # Dragonfly Falls: Light Gem from Sparx
    (0x32, DRAGON_EGG, 0x50288c, 0x40), # Dragonfly Falls: Dragon Egg behind breakable wall above wall kick
    (0x33, LIGHT_GEM, 0x502962, 0x20),  # Dragonfly Falls: Light Gem beyond Piranha Pool
    (0x34, LIGHT_GEM, 0x502962, 0x4),   # Dragonfly Falls: Locked Chest in Piranha Pool
    (0x35, DRAGON_EGG, 0x5028b8, 0x40), # Dragonfly Falls: Dragon Egg in vultures nest (Hunter)
    (0x36, LIGHT_GEM, 0x5028b8, 0x10),  # Dragonfly Falls: Complete Hunters trial
    (0x37, DARK_GEM, 0x50288f, 0x1),    # Dragonfly Falls: Dark Gem at end of zone
    (0x38, LIGHT_GEM, 0x000000, 0x0),   # Dragonfly Falls: Light Gem behind breakable wall beyond 70 Light Gem door
    (0x39, DRAGON_EGG, 0x000000, 0x0),  # Dragonfly Falls: Dragon Egg from thief beyond 70 Light Gem door
    (0x3A, LIGHT_GEM, 0x000000, 0x0),   # Dragonfly Falls: Light Gem glide from wall kick
}
"""
    "Crocoville Swamp: Dark Gem by Moneybags platform",
    "Crocoville Swamp: Locked Chest behind breakable wall",
    "Crocoville Swamp: Dragon Egg across platforms in mud",
   #"Crocoville Swamp: Light Gem behind reinforced door",
    "Crocoville Swamp: Light Gem on top of pyramid",
    "Crocoville Swamp: Locked Chest near Dogs",
    "Crocoville Swamp: Locked Chest in Temple",
    "Crocoville Swamp: Light Gem in Temple",
    "Crocoville Swamp: Light Gem in secret room",
    "Crocoville Swamp: Dragon Egg from thief in temple",
    "Crocoville Swamp: Light Gem after platforming",
    "Crocoville Swamp: Dragon Egg after pole spin left",
   #"Crocoville Swamp: Dragon Egg from Blink",
   #"Crocoville Swamp: Light Gem from Blink",
    "Crocoville Swamp: Dark Gem before Elder Magnus",
    "Crocoville Swamp: Pole Spin from Elder Magnus",
    "Crocoville Swamp: Dragon Egg in Elder Magnus' house",
    "Crocoville Swamp: Light Gem in Elder Magnus' house",
    "Crocoville Swamp: Dark Gem above Blink",
   #"Crocoville Swamp: Dragon Egg from Fredneck",
   #"Crocoville Swamp: Light Gem from Fredneck",
    "Crocoville Swamp: Light Gem across the lilypads",
"""