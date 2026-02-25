from __future__ import annotations

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import SpyroAHTWorld


def set_all_rules(world: SpyroAHTWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: SpyroAHTWorld) -> None:
    village_to_tomas = world.get_entrance("EntranceElderTomas")
    tomas_to_gnasty = world.get_entrance("EntranceGnastysLair")

    set_rule(village_to_tomas, lambda state: state.has("Double Jump", world.player))
    set_rule(tomas_to_gnasty, lambda state: state.has("Dark Gem", world.player, 3))

def set_all_location_rules(world: SpyroAHTWorld) -> None:
    set_rule(world.get_location("Dark Gem next to Ember"), lambda state: state.has("Double Jump", world.player))

def set_completion_condition(world: SpyroAHTWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
