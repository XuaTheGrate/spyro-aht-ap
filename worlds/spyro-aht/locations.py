from __future__ import annotations

from BaseClasses import Location

from . import items
from .regions import REGIONS, DataLocation, _DEFAULT_RULE

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import SpyroAHTWorld

LOCATION_NAME_TO_ID: dict[str, int] = {}

for region in REGIONS.values():
    for location in region.locations:
        assert location.id not in LOCATION_NAME_TO_ID.values()
        LOCATION_NAME_TO_ID[location.name] = location.id


SHOP_ITEMS = [
    DataLocation("Moneybags: Shop item 1", 1001, _DEFAULT_RULE), # Extra Health Unit
    DataLocation("Moneybags: Shop Item 2", 1002, _DEFAULT_RULE), # Keychain
    DataLocation("Moneybags: Shop Item 3", 1003, _DEFAULT_RULE), # Butterfly Jar
    DataLocation("Moneybags: Shop Item 4", 1004, _DEFAULT_RULE), # Double Gems
    DataLocation("Moneybags: Shop Item 5", 1005, _DEFAULT_RULE), # Shockwave
]

SHOP_ITEMS.extend(DataLocation(f"Moneybags: Shop Item {6+i}", 1006+i, _DEFAULT_RULE) for i in range(54))


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
    reds_lab = world.get_region("Red's Laboratory")
    reds_lab.add_event("Red's Laboratory: Defeat Mecha-Red", "Victory", location_type=SpyroAHTLocation,item_type=items.SpyroAHTItem,rule=lambda state: state.has("Dark Gem", world.player, 40))
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
