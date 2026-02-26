from __future__ import annotations

from BaseClasses import Region

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import SpyroAHTWorld

REGIONS: dict[str, list[str]] = {
    "Dragon Village": ["Dragon Village - After Elder Tomas"],
    "Dragon Village - After Elder Tomas": ["Dragon Village - Gnasty Gnorcs Lair", "Crocoville Swamp", "Dragonfly Falls"],
    "Dragon Village - Gnasty Gnorcs Lair": [],

    "Crocoville Swamp": ["Crocoville Swamp - After Elder Magnus"],
    "Crocoville Swamp - After Elder Magnus": [],
    "Dragonfly Falls": []
}

REGION_LOCATIONS: dict[str, list[str]] = {
    "Dragon Village": ["Dragon Village: Double Jump/Horn Dive from Elder Tomas"],
    "Dragon Village - After Elder Tomas": [
        "Dragon Village: Dark Gem by Elder Tomas",
        "Dragon Village: Dark Gem by Ember",
        "Dragon Village: Dragon Egg after Hunter",
        "Dragon Village: Light Gem in Nursery",
        "Dragon Village: Locked Chest near Ball Gadget",
        "Dragon Village: Locked Chest on cliff",
        "Dragon Village: Dragon Egg behind breakable wall",
        "Dragon Village: Light Gem above Lab Secret Entrance",
        "Dragon Village: Light Gem across timed platforms",
        "Dragon Village: Dark Gem by Sgt. Byrd",
        "Dragon Village: Dragon Egg behind Dark Gem by Sgt. Byrd",
        "Dragon Village: Dragon Egg from Sgt. Byrd",
        "Dragon Village: Light Gem from Sgt. Byrd",
        "Dragon Village: Locked Chest before Crocoville Swamp"
    ],
    "Dragon Village - Gnasty Gnorcs Lair": ["Dragon Village: Dragon Egg in Gnastys Lair", "Dragon Village: Lightning Breath from Gnasty Gnorc"],
    "Crocoville Swamp": [    
        "Crocoville Swamp: Dark Gem by Moneybags platform",
        "Crocoville Swamp: Locked Chest behind breakable wall",
        "Crocoville Swamp: Dragon Egg across platforms in mud",
        "Crocoville Swamp: Light Gem behind reinforced door",
        "Crocoville Swamp: Light Gem on top of pyramid",
        "Crocoville Swamp: Locked Chest near Dogs",
        "Crocoville Swamp: Locked Chest in Temple",
        "Crocoville Swamp: Light Gem in Temple",
        "Crocoville Swamp: Light Gem in secret room",
        "Crocoville Swamp: Dragon Egg from thief in temple",
        "Crocoville Swamp: Light Gem after platforming",
        "Crocoville Swamp: Dragon Egg after pole spin left",
        "Crocoville Swamp: Dragon Egg from Blink",
        "Crocoville Swamp: Light Gem from Blink",
        "Crocoville Swamp: Dark Gem before Elder Magnus",
        "Crocoville Swamp: Pole Spin from Elder Magnus"
    ],
    "Crocoville Swamp - After Elder Magnus": [
        "Crocoville Swamp: Dragon Egg in Elder Magnus' house",
        "Crocoville Swamp: Light Gem in Elder Magnus' house",
        "Crocoville Swamp: Dark Gem above Blink",
        "Crocoville Swamp: Dragon Egg from Fredneck",
        "Crocoville Swamp: Light Gem from Fredneck",
        "Crocoville Swamp: Light Gem across the lilypads",
    ],
    "Dragonfly Falls": [
        "Dragonfly Falls: Locked Chest near Ball Gadget",
        "Dragonfly Falls: Dark Gem behind breakable wall",
        "Dragonfly Falls: Dragon Egg after Dark Gem behind breakable wall",
        "Dragonfly Falls: Light Gem behind reinforced wall",
        "Dragonfly Falls: Dark Gem near vultures",
        "Dragonfly Falls: Dragon Egg in vultures nest",
        "Dragonfly Falls: Dark Gem before large pool",
        "Dragonfly Falls: Light Gem behind breakable wall in large pool",
        "Dragonfly Falls: Dragon Egg from Sparx",
        "Dragonfly Falls: Light Gem from Sparx",
        "Dragonfly Falls: Dragon Egg behind breakable wall above wall kick",
        "Dragonfly Falls: Light Gem beyond Piranha Pool",
        "Dragonfly Falls: Locked Chest in Piranha Pool",
        "Dragonfly Falls: Dragon Egg in vultures nest (Hunter)",
        "Dragonfly Falls: Complete Hunters trial",
        "Dragonfly Falls: Dark Gem at end of zone",
        "Dragonfly Falls: Light Gem behind breakable wall beyond 70 Light Gem door",
        "Dragonfly Falls: Dragon Egg from thief beyond 70 Light Gem door",
        "Dragonfly Falls: Light Gem glide from wall kick"
    ]
}

def create_and_connect_regions(world: SpyroAHTWorld) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: SpyroAHTWorld) -> None:
    for region in REGIONS.keys():
        r = Region(region, world.player, world.multiworld)
        world.multiworld.regions.append(r)

    #dragon_village = Region("Dragon Village", world.player, world.multiworld)
    #dragon_village_tomas = Region("Dragon Village - After Elder Tomas", world.player, world.multiworld)
    #dragon_village_gnasty = Region("Dragon Village - Gnasty Gnorc's Lair", world.player, world.multiworld)

    #world.multiworld.regions += [dragon_village, dragon_village_tomas, dragon_village_gnasty]

def connect_regions(world: SpyroAHTWorld) -> None:
    regions = {world.get_region(r): [world.get_region(k) for k in v] for r, v in REGIONS.items()}

    for region, connects in regions.items():
        for con in connects:
            entrance = region.name.replace(' ', '') + '->' + con.name.replace(' ', '')
            print(f"Connecting {region.name} to {con.name}: {entrance!r}")
            region.connect(con, entrance)

    #dragon_village = world.get_region("Dragon Village")
    #dragon_village_tomas = world.get_region("Dragon Village - After Elder Tomas")
    #dragon_village_gnasty = world.get_region("Dragon Village - Gnasty Gnorc's Lair")

    #dragon_village.connect(dragon_village_tomas, "EntranceElderTomas")
    #dragon_village_tomas.connect(dragon_village_gnasty, "EntranceGnastysLair")
