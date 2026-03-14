from __future__ import annotations

from BaseClasses import Location
from rule_builder.rules import True_, HasAny, Has, HasAll

from . import items
from .regions import REGIONS, DataLocation

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import SpyroAHTWorld

LOCATION_NAME_TO_ID: dict[str, int] = {}

SHOP_ITEMS = [
    DataLocation("Moneybags: Shop item 1", 1001, True_()), # Extra Health Unit
    DataLocation("Moneybags: Shop Item 2", 1002, True_()), # Keychain
    DataLocation("Moneybags: Shop Item 3", 1003, True_()), # Butterfly Jar
    DataLocation("Moneybags: Shop Item 4", 1004, True_()), # Double Gems
    DataLocation("Moneybags: Shop Item 5", 1005, True_()), # Shockwave
]

SHOP_ITEMS.extend(DataLocation(f"Moneybags: Shop Item {6+i}", 1006+i, True_()) for i in range(52))


for region in REGIONS.values():
    for location in region.locations:
        assert location.id not in LOCATION_NAME_TO_ID.values()
        LOCATION_NAME_TO_ID[location.name] = location.id


for s in SHOP_ITEMS:
    LOCATION_NAME_TO_ID[s.name] = s.id


class SpyroAHTLocation(Location):
    game = "Spyro: A Hero's Tail"


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {name: LOCATION_NAME_TO_ID[name] for name in location_names}


def create_all_locations(world: SpyroAHTWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: SpyroAHTWorld):
    for region in REGIONS.values():
        r = world.get_region(region.name)
        r.add_locations(get_location_names_with_ids([l.name for l in region.locations]))
    
    if world.options.randomize_shop_items:
        r = world.get_region("Dragon Village")
        r.add_locations({l.name: l.id for l in SHOP_ITEMS})


def create_events(world: SpyroAHTWorld) -> None:
    match world.options.misc_goal:
        case 0: # Gnasty Gnorc
            world.get_region("Dragon Village - Gnasty Gnorcs Lair").add_event(
                "Dragon Village: Defeat Gnasty Gnorc (Goal)", "Victory", location_type=SpyroAHTLocation, item_type=items.SpyroAHTItem,
                rule=HasAny("Fire Breath", "Charge")
            )
        case 1: # Ineptune
            world.get_region("Coastal Remains - Ineptunes Lair").add_event(
                "Coastal Remains: Defeat Ineptune (Goal)", "Victory", location_type=SpyroAHTLocation, item_type=items.SpyroAHTItem,
                rule=True_()
            )
        case 2: # Red
            world.get_region("Frostbite Village - Reds Lair").add_event(
                "Frostbite Village - Defeat Red (Goal)", "Victory", location_type=SpyroAHTLocation, item_type=items.SpyroAHTItem,
                rule=True_()
            )
        case 3: # Mecha-Red
            reds_lab = world.get_region("Red's Laboratory")
            reds_lab.add_event("Red's Laboratory: Defeat Mecha-Red", "Victory", location_type=SpyroAHTLocation,item_type=items.SpyroAHTItem,rule=Has("Dark Gem", 40) & HasAll("Lightning Breath", "Fire Breath"))
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
