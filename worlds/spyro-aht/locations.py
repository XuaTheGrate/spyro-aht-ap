from __future__ import annotations

from BaseClasses import ItemClassification, Location

from . import items

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import SpyroAHTWorld


LOCATION_NAME_TO_ID = {
    "Double Jump from Elder Tomas": 0x0,
    "Dark Gem next to Elder Tomas": 0x1,
    "Dark Gem next to Ember": 0x2,
    "Dragon Egg past Hunter": 0x3,
    "Light Gem inside Nursery": 0x4,
    "Dragon Egg in Locked Chest before Ball Gadget": 0x5,
    "Light Gem in Locked Chest after Double Jump Cliff": 0x6,
    "Dragon Egg behind Breakable Wall near Sgt. Byrd": 0x7,
    "Light Gem above Professor Mole": 0x8,
    "Light Gem after platforming near Sgt. Byrd": 0x9,
    "Dark Gem after platforming near Sgt. Byrd": 0xA,
    "Dragon Egg after Dark Gem near Sgt. Byrd": 0xB,
    #"Dragon Egg from Sgt. Byrd Minigame": 0xC,
    #"Light Gem from Sgt. Byrd Minigame": 0xD,
    "Light Gem in Locked Chest before Crocoville Swamp": 0xE,
    "Dragon Egg in Gnasty's Lair after Flame": 0xF,
    "Lightning Breath from Gnasty Gnorc": 0x10
}

class SpyroAHTLocation(Location):
    game = "Spyro: A Hero's Tail"

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {name: LOCATION_NAME_TO_ID[name] for name in location_names}

def create_all_locations(world: SpyroAHTWorld) -> None:
    create_regular_locations(world)
    create_events(world)

def create_regular_locations(world: SpyroAHTWorld):
    dragon_village = world.get_region("Dragon Village")
    dragon_village_tomas = world.get_region("Dragon Village - After Elder Tomas")
    dragon_village_gnasty = world.get_region("Dragon Village - Gnasty Gnorc's Lair")

    dragon_village.add_locations(get_location_names_with_ids(["Double Jump from Elder Tomas", "Dark Gem next to Ember"]), SpyroAHTLocation)
    dragon_village_tomas.add_locations(get_location_names_with_ids([
        "Dark Gem next to Elder Tomas",
        "Dragon Egg past Hunter",
        "Light Gem inside Nursery",
        "Dragon Egg in Locked Chest before Ball Gadget",
        "Light Gem in Locked Chest after Double Jump Cliff",
        "Dragon Egg behind Breakable Wall near Sgt. Byrd",
        "Light Gem above Professor Mole",
        "Light Gem after platforming near Sgt. Byrd",
        "Dark Gem after platforming near Sgt. Byrd",
        "Dragon Egg after Dark Gem near Sgt. Byrd",
        #"Dragon Egg from Sgt. Byrd Minigame",
        #"Light Gem from Sgt. Byrd Minigame",
        "Light Gem in Locked Chest before Crocoville Swamp",
    ]), SpyroAHTLocation)

    dragon_village_gnasty.add_locations(get_location_names_with_ids(["Dragon Egg in Gnasty's Lair after Flame", "Lightning Breath from Gnasty Gnorc"]), SpyroAHTLocation)

def create_events(world: SpyroAHTWorld) -> None:
    # utilise this as a way to defeat gnasty gnorc perhaps
    dragon_village_gnasty = world.get_region("Dragon Village - Gnasty Gnorc's Lair")
    dragon_village_gnasty.add_event("Defeat Mecha-Red", "Victory", location_type=SpyroAHTLocation,item_type=items.SpyroAHTItem)