MD5 = '4a8320b24738334127b29de343c534ae'
IDN = 'SLUS_208.84'

NOP_ADDR = [
	(0x96de0, b'\x01\x00\x42\x34', b'\x00\x00\x00\x00') # disable double jump from elder tomas
]

LOCATIONS = {
	# Dragon Village
	(0x0, 0x5021b5, 0x80), # Double Jump from Elder Tomas
	(0x1, 0x502775, 0x2),  # Dark Gem next to Elder Tomas
	(0x2, 0x502774, 0x80), # Dark Gem next to Ember
	(0x3, 0x502782, 0x2),  # Dragon Egg past Hunter
	(0x4, 0x5027c6, 0x80), # Light Gem inside Nursery
    # TODO: make this check more strict
	(0x5, 0x5027c9, 0x18), # Dragon Egg in Locked Chest before Ball Gadget
    # TODO: make this check more strict
	(0x6, 0x5027cf, 0x6),  # Light Gem in Locked Chest after Double Jump Cliff
	(0x7, 0x502792, 0x8),  # Dragon Egg behind Breakable Wall near Sgt. Byrd
	(0x8, 0x502791, 0x40), # Light Gem above Professor Mole
	(0x9, 0x502777, 0x4),  # Light Gem after Platforming near Sgt. Byrd
	(0xA, 0x502775, 0x40), # Dark Gem after Platforming near Sgt. Byrd
	(0xB, 0x502776, 0x40), # Dragon Egg after Dark Gem near Sgt. Byrd
    # TODO: resolve mini games
	# (0xC, 0x000000, 0x0),  # Dragon Egg from Sgt. Byrd
	# (0xD, 0x000000, 0x0),  # Light Gem from Sgt. Byrd
    # TODO: make this check more strict
	(0xE, 0x5027D0, 0x6),  # Light Gem in Locked Chest before Swamp
    # TODO
    # (0xF, 0x000000, 0x0),  # Dragon Egg in Gnasty's Lair after Flame
    # (0x10, 0x00000, 0x0),  # Lightning Breath from Gnasty Gnorc
}