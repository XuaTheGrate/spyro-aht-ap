from enum import IntFlag

MD5 = '4a8320b24738334127b29de343c534ae'
IDN = 'SLUS_208.84'

ITEM_STORAGE = 0x503280

# Items are stored at 0x503280
# the first tuple item is an offset from this address in multiples of 2
# the second item is the bit flag (0x1 - 0x80)
ITEM_STORAGE_DOUBLE_JUMP = (0x0, 0x1)

DARK_GEM_COUNT = 0x502057
LIGHT_GEM_COUNT = 0x502056
DRAGON_EGG_COUNT = 0x502058

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
	# Dragon Village
	(0x1, 0x1, 0x5021b5, 0x80), # Double Jump from Elder Tomas
	(0x2, 0x8, 0x502775, 0x2),  # Dark Gem next to Elder Tomas
	(0x3, 0x8, 0x502774, 0x80), # Dark Gem next to Ember
	(0x4, 0xA, 0x502782, 0x2),  # Dragon Egg past Hunter
	(0x5, 0x9, 0x5027c6, 0x80), # Light Gem inside Nursery
    # TODO: make this check more strict
	(0x6, 0xA, 0x5027c9, 0x18), # Dragon Egg in Locked Chest before Ball Gadget
    # TODO: make this check more strict
	(0x7, 0x9, 0x5027cf, 0x6),  # Light Gem in Locked Chest after Double Jump Cliff
	(0x8, 0xA, 0x502792, 0x8),  # Dragon Egg behind Breakable Wall near Sgt. Byrd
	(0x9, 0x9, 0x502791, 0x80), # Light Gem above Professor Mole
	(0xA, 0x9, 0x502777, 0x4),  # Light Gem after Platforming near Sgt. Byrd
	(0xB, 0x8, 0x502775, 0x40), # Dark Gem after Platforming near Sgt. Byrd
	(0xC, 0xA, 0x502776, 0x40), # Dragon Egg after Dark Gem near Sgt. Byrd
    # TODO: resolve mini games
	# (0xD, 0xA, 0x000000, 0x0),  # Dragon Egg from Sgt. Byrd
	# (0xE, 0x9, 0x000000, 0x0),  # Light Gem from Sgt. Byrd
    # TODO: make this check more strict
	(0xF, 0x9, 0x5027D0, 0x6),  # Light Gem in Locked Chest before Swamp
    # TODO
    # (0x10, 0xA, 0x000000, 0x0),  # Dragon Egg in Gnasty's Lair after Flame
    # (0x11, 0x5, 0x00000, 0x0),  # Lightning Breath from Gnasty Gnorc
}