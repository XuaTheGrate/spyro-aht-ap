from __future__ import annotations

from BaseClasses import Item, ItemClassification

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import SpyroAHTWorld


ITEM_NAME_TO_ID = {
    "Double Jump": 0x1,
    "Pole Spin": 0x2,
    "Wing Shield": 0x3,
    "Wall Kick": 0x4,

    "Dark Gem": 0x8,
    "Light Gem": 0x9,
    "Dragon Egg": 0xA,

    "Fire Breath": 0xE,
    "Lightning Breath": 0x5,
    "Water Breath": 0x6,
    "Ice Breath": 0x7,

    "Swim": 0xB,
    "Glide": 0xC,
    "Charge": 0xD,
}

DEFAULT_ITEMS = [
    "Double Jump",
    "Pole Spin",
    "Wing Shield",
    "Wall Kick",
    "Dark Gem",
    "Light Gem",
    "Dragon Egg"
]

DEFAULT_ITEM_CLASSIFICATIONS = {
    "Double Jump": ItemClassification.progression,
    "Pole Spin": ItemClassification.progression,
    "Wing Shield": ItemClassification.progression,
    "Wall Kick": ItemClassification.progression,
    "Fire Breath": ItemClassification.progression,
    "Lightning Breath": ItemClassification.progression,
    "Water Breath": ItemClassification.progression,
    "Ice Breath": ItemClassification.progression,
    "Swim": ItemClassification.progression,
    "Glide": ItemClassification.progression,
    "Charge": ItemClassification.progression,
    "Dark Gem": ItemClassification.progression,
    "Light Gem": ItemClassification.progression | ItemClassification.filler,
    "Dragon Egg": ItemClassification.filler
}

ITEM_COUNTS = {
    "Dark Gem": 40,
    "Light Gem": 100,
    "Dragon Egg": 80  
}

FILLER_ITEM_NAME = "Dragon Egg"


class SpyroAHTItem(Item):
    game = "Spyro: A Hero's Tail"


def create_item_with_correct_classification(world: SpyroAHTWorld, name: str) -> SpyroAHTItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    return SpyroAHTItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: SpyroAHTWorld) -> None:
    itempool: list[Item] = []

    for item in DEFAULT_ITEMS:
        for _ in range(ITEM_COUNTS.get(item, 1)):
            itempool.append(world.create_item(item))
    
    match world.options.randomize_breath:
        case 0: # default
            l = world.get_location("Dragon Village: Fire Breath")
            l.place_locked_item(world.create_item("Fire Breath"))
            itempool.extend((world.create_item("Lightning Breath"), world.create_item("Water Breath"), world.create_item("Ice Breath")))
        case 1: # randomized
            breaths = ["Fire Breath", "Lightning Breath", "Water Breath", "Ice Breath"]
            breath = world.random.choice(breaths)
            breaths.remove(breath)
            i = world.create_item(breath)
            l = world.get_location("Dragon Village: Fire Breath")
            l.place_locked_item(i)
            itempool.extend(world.create_item(i) for i in breaths)
        case 2: # none
            breaths = ["Fire Breath", "Lightning Breath", "Water Breath", "Ice Breath"]
            itempool.extend(world.create_item(i) for i in breaths)
    
    if not world.options.randomize_charge:
        l = world.get_location("Dragon Village: Charge")
        l.place_locked_item(world.create_item("Charge"))
    else:
        itempool.append(world.create_item("Charge"))

    if not world.options.randomize_swim:
        l = world.get_location("Dragon Village: Swim")
        l.place_locked_item(world.create_item("Swim"))
    else:
        itempool.append(world.create_item("Swim"))

    if not world.options.randomize_glide:
        l = world.get_location("Dragon Village: Glide")
        l.place_locked_item(world.create_item("Glide"))
    else:
        itempool.append(world.create_item("Glide"))
    
    unfilled = len(world.multiworld.get_unfilled_locations(world.player))
    print(f"Adding {unfilled - len(itempool)} dragon eggs") # should theoretically always be 80 anyway
    #itempool.extend(world.create_filler() for _ in range(unfilled - len(itempool)))

    world.multiworld.itempool.extend(itempool)
    
