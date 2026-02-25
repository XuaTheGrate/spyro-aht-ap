from __future__ import annotations

from BaseClasses import Item, ItemClassification

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import SpyroAHTWorld


ITEM_NAME_TO_ID = {
    "Double Jump": 0x0,
    # "Pole Spin": 0x1,
    # "Wing Shield": 0x2,
    # "Wall Kick": 0x3,
    # "Lightning Breath": 0x4,
    # "Water Breath": 0x5,
    # "Ice Breath": 0x6,
    "Dark Gem": 0x7,
    "Light Gem": 0x8,
    "Dragon Egg": 0x9
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    "Double Jump": ItemClassification.progression,
    # "Pole Spin": ItemClassification.progression,
    # "Wing Shield": ItemClassification.progression,
    # "Wall Kick": ItemClassification.progression,
    # "Lightning Breath": ItemClassification.progression,
    # "Water Breath": ItemClassification.progression,
    # "Ice Breath": ItemClassification.progression
    "Dark Gem": ItemClassification.progression,
    "Light Gem": ItemClassification.progression | ItemClassification.filler,
    "Dragon Egg": ItemClassification.filler
}

ITEM_COUNTS = {
    "Dark Gem": 3,
    "Light Gem": 6,
    "Dragon Egg": 6
}

class SpyroAHTItem(Item):
    game = "Spyro: A Hero's Tail"

FILLER_ITEM_NAME = "Dragon Egg"

def create_item_with_correct_classification(world: SpyroAHTWorld, name: str) -> SpyroAHTItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    return SpyroAHTItem(name, classification, ITEM_NAME_TO_ID[name], world.player)

def create_all_items(world: SpyroAHTWorld) -> None:
    itempool: list[Item] = []

    for item in ITEM_NAME_TO_ID.keys():
        for _ in range(ITEM_COUNTS.get(item, 1)):
            itempool.append(world.create_item(item))
    
    unfilled = len(world.multiworld.get_unfilled_locations(world.player))
    itempool.extend((world.create_filler() for _ in range(unfilled - len(itempool))))

    world.multiworld.itempool.extend(itempool)
    
