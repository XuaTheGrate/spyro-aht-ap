from __future__ import annotations

from BaseClasses import ItemClassification, Location

from . import items
from .regions import REGION_LOCATIONS

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import SpyroAHTWorld


#LOCATION_NAME_TO_ID = {
#    "Double Jump from Elder Tomas": 0x1,
#    "Dark Gem next to Elder Tomas": 0x2,
#    "Dark Gem next to Ember": 0x3,
#    "Dragon Egg past Hunter": 0x4,
#    "Light Gem inside Nursery": 0x5,
#    "Dragon Egg in Locked Chest before Ball Gadget": 0x6,
#    "Light Gem in Locked Chest after Double Jump Cliff": 0x7,
#    "Dragon Egg behind Breakable Wall near Sgt. Byrd": 0x8,
#    "Light Gem above Professor Mole": 0x9,
#    "Light Gem after platforming near Sgt. Byrd": 0xA,
#    "Dark Gem after platforming near Sgt. Byrd": 0xB,
#    "Dragon Egg after Dark Gem near Sgt. Byrd": 0xC,
#    #"Dragon Egg from Sgt. Byrd Minigame": 0xD,
#    #"Light Gem from Sgt. Byrd Minigame": 0xE,
#    "Light Gem in Locked Chest before Crocoville Swamp": 0xF,
#    "Dragon Egg in Gnasty's Lair after Flame": 0x10,
#    "Lightning Breath from Gnasty Gnorc": 0x11
#}

LOCATION_NAME_TO_ID = {}

#LOCATION_NAME_TO_ID = {k: i for i, k in enumerate(LOCATION_NAMES, 1)}
_i = 0
for region in REGION_LOCATIONS:
    for location in REGION_LOCATIONS[region]:
        _i += 1
        assert location not in LOCATION_NAME_TO_ID
        LOCATION_NAME_TO_ID[location] = _i


class SpyroAHTLocation(Location):
    game = "Spyro: A Hero's Tail"

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {name: LOCATION_NAME_TO_ID[name] for name in location_names}

def create_all_locations(world: SpyroAHTWorld) -> None:
    create_regular_locations(world)
    create_events(world)

def create_regular_locations(world: SpyroAHTWorld):
    for region in REGION_LOCATIONS:
        r = world.get_region(region)
        r.add_locations(get_location_names_with_ids(REGION_LOCATIONS[region]))
    
    #dragon_village = world.get_region("Dragon Village")
    #dragon_village_tomas = world.get_region("Dragon Village - After Elder Tomas")
    #dragon_village_gnasty = world.get_region("Dragon Village - Gnasty Gnorc's Lair")

    #dragon_village.add_locations(get_location_names_with_ids(["Double Jump from Elder Tomas", "Dark Gem next to Ember"]), SpyroAHTLocation)
    #dragon_village_tomas.add_locations((), SpyroAHTLocation)

    #dragon_village_gnasty.add_locations(get_location_names_with_ids(["Dragon Egg in Gnasty's Lair after Flame", "Lightning Breath from Gnasty Gnorc"]), SpyroAHTLocation)

def create_events(world: SpyroAHTWorld) -> None:
    # TEMPORARY
    dragon_village_gnasty = world.get_region("Dragon Village - Gnasty Gnorcs Lair")
    dragon_village_gnasty.add_event("Defeat Gnasty Gnorc", "Victory", location_type=SpyroAHTLocation,item_type=items.SpyroAHTItem)
