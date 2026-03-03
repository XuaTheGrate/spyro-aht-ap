from __future__ import annotations

from BaseClasses import Location

from . import items
from .regions import REGIONS

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import SpyroAHTWorld

LOCATION_NAME_TO_ID: dict[str, int] = {}

for region in REGIONS.values():
    for location in region.locations:
        assert location.id not in LOCATION_NAME_TO_ID.values()
        LOCATION_NAME_TO_ID[location.name] = location.id


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


def create_events(world: SpyroAHTWorld) -> None:
    reds_lab = world.get_region("Red's Laboratory")
    reds_lab.add_event("Red's Laboratory: Defeat Mecha-Red", "Victory", location_type=SpyroAHTLocation,item_type=items.SpyroAHTItem,rule=lambda state: state.has("Dark Gem", world.player, 40))
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
