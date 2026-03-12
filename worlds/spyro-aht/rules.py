from __future__ import annotations

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

from .regions import REGIONS

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import SpyroAHTWorld


def set_all_rules(world: SpyroAHTWorld) -> None:
    set_all_location_rules(world)
    

def set_all_location_rules(world: SpyroAHTWorld) -> None:
    for r in REGIONS.values():
        for location in r.locations:
            l = world.get_location(location.name)
            world.set_rule(l, location.access_rule)
