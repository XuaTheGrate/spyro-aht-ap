from __future__ import annotations

from BaseClasses import Entrance, Region

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import SpyroAHTWorld

def create_and_connect_regions(world: SpyroAHTWorld) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: SpyroAHTWorld) -> None:
    dragon_village = Region("Dragon Village", world.player, world.multiworld)
    dragon_village_tomas = Region("Dragon Village - After Elder Tomas", world.player, world.multiworld)
    dragon_village_gnasty = Region("Dragon Village - Gnasty Gnorc's Lair", world.player, world.multiworld)

    world.multiworld.regions += [dragon_village, dragon_village_tomas, dragon_village_gnasty]

def connect_regions(world: SpyroAHTWorld) -> None:
    dragon_village = world.get_region("Dragon Village")
    dragon_village_tomas = world.get_region("Dragon Village - After Elder Tomas")
    dragon_village_gnasty = world.get_region("Dragon Village - Gnasty Gnorc's Lair")

    dragon_village.connect(dragon_village_tomas, "EntranceElderTomas")
    dragon_village_tomas.connect(dragon_village_gnasty, "EntranceGnastysLair")
