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
    village_to_tomas = world.get_entrance("DragonVillage->DragonVillage-AfterElderTomas")
    tomas_to_gnasty = world.get_entrance("DragonVillage-AfterElderTomas->DragonVillage-GnastyGnorcsLair")
    crocoville_to_magnus = world.get_entrance("CrocovilleSwamp->CrocovilleSwamp-AfterElderMagnus")
    tomas_to_dragonfly = world.get_entrance("DragonVillage-AfterElderTomas->DragonflyFalls")

    set_rule(village_to_tomas, lambda state: state.has("Double Jump", world.player))
    set_rule(tomas_to_gnasty, lambda state: state.has("Dark Gem", world.player, 10))
    set_rule(crocoville_to_magnus, lambda state: state.has("Pole Spin", world.player))
    set_rule(tomas_to_dragonfly, lambda state: state.has("Light Gem", world.player, 8))
    

def set_all_location_rules(world: SpyroAHTWorld) -> None:
    #set_rule(world.get_location("Crocoville Swamp: Light Gem behind reinforced door"), lambda state: state.has("Light Gem", world.player, 40))
    set_rule(world.get_location("Crocoville Swamp: Dragon Egg from thief in temple"), lambda state: state.has("Lightning Breath", world.player))
    set_rule(world.get_location("Crocoville Swamp: Dragon Egg after pole spin left"), lambda state: state.has("Pole Spin", world.player))

    #set_rule(world.get_location("Dragon Egg behind breakable wall above wall kick"), lambda state: state.has("Wall Kick", world.player))
    #set_rule(world.get_location("Dragonfly Falls: Light Gem behind breakable wall beyond 70 Light Gem door"), lambda state: state.has("Light Gem", world.player, 70))
    #set_rule(world.get_location("Dragonfly Falls: Dragon Egg from thief beyond 70 Light Gem door"), lambda state: state.has("Light Gem", world.player, 70))
    #set_rule(world.get_location("Dragonfly Falls: Light Gem glide from wall kick"), lambda state: state.has("Wall Kick", world.player))


def set_completion_condition(world: SpyroAHTWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
