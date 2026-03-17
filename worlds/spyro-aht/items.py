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
    "Electric Breath": 0x5,
    "Water Breath": 0x6,
    "Ice Breath": 0x7,

    "Swim": 0xB,
    "Glide": 0xC,
    "Charge": 0xD,

    "Lockpick": 0x1C,
    "Health Unit+": 0xF,

    "Butterfly Jar": 0x19,
    "Double Gems": 0x1A,
    "Shockwave": 0x1B,

    "Gem Pack": 0x1D,

    "Fire Bomb": 0x1E,
    "Electric Bomb": 0x1F,
    "Water Bomb": 0x20,
    "Ice Bomb": 0x21
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
    "Electric Breath": ItemClassification.progression,
    "Water Breath": ItemClassification.progression,
    "Ice Breath": ItemClassification.progression,

    "Swim": ItemClassification.progression,
    "Glide": ItemClassification.progression,
    "Charge": ItemClassification.progression,

    "Dark Gem": ItemClassification.progression,
    "Light Gem": ItemClassification.progression | ItemClassification.filler,
    "Dragon Egg": ItemClassification.filler,

    "Lockpick": ItemClassification.progression,
    "Health Unit+": ItemClassification.useful,
    
    "Butterfly Jar": ItemClassification.useful,
    "Double Gems": ItemClassification.useful,
    "Shockwave": ItemClassification.useful,

    "Gem Pack": ItemClassification.filler,

    "Fire Bomb": ItemClassification.filler,
    "Electric Bomb": ItemClassification.filler,
    "Water Bomb": ItemClassification.filler,
    "Ice Bomb": ItemClassification.filler
}


ITEM_COUNTS = {
    "Dark Gem": 40,
    "Light Gem": 100,
    "Dragon Egg": 80
}


class SpyroAHTItem(Item):
    game = "Spyro: A Hero's Tail"


def create_item_with_correct_classification(world: SpyroAHTWorld, name: str) -> SpyroAHTItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    return SpyroAHTItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


byrd_locations = [[
    "Dragon Village: Dragon Egg from Sgt. Byrd",
    "Cloudy Domain: Dragon Egg from Sgt. Byrd",
    "Ice Citadel: Dragon Egg from Sgt. Byrd",
    "Molten Mount: Dragon Egg from Sgt. Byrd"
], [
    "Cloudy Domain: Light Gem from Sgt. Byrd",
    "Dragon Village: Light Gem from Sgt. Byrd",
    "Ice Citadel: Light Gem from Sgt. Byrd",
    "Molten Mount: Light Gem from Sgt. Byrd"
]]

blink_locations = [[
    "Crocovile Swamp: Dragon Egg from Blink",
    "Coastal Remains: Dragon Egg from Blink",
    "Frostbite Village: Dragon Egg from Blink",
    "Dark Mine: Dragon Egg from Blink",
], [
    "Crocovile Swamp: Light Gem from Blink",
    "Coastal Remains: Light Gem from Blink",
    "Frostbite Village: Light Gem from Blink",
    "Dark Mine: Light Gem from Blink",
]]

turret_locations = [[
    "Crocovile Swamp: Dragon Egg from Fredneck",
    "Coastal Remains: Dragon Egg from Turtle Mother",
    "Frostbite Village: Dragon Egg from Peggy",
    "Stormy Beach: Dragon Egg from Wally",
], [
    "Crocovile Swamp: Light Gem from Fredneck",
    "Coastal Remains: Light Gem from Turtle Mother",
    "Frostbite Village: Light Gem from Peggy",
    "Stormy Beach: Light Gem from Wally",
]]

sparx_locations = [[
    "Dragonfly Falls: Dragon Egg from Sparx",
    "Sunken Ruins: Dragon Egg from Sparx",
    "Gloomy Glacier: Dragon Egg from Sparx",
    "Magma Falls Bottom: Dragon Egg from Sparx",
], [
    "Dragonfly Falls: Light Gem from Sparx",
    "Sunken Ruins: Light Gem from Sparx",
    "Gloomy Glacier: Light Gem from Sparx",
    "Magma Falls Bottom: Light Gem from Sparx",
]]


def create_all_items(world: SpyroAHTWorld) -> None:
    counts = ITEM_COUNTS.copy()

    itempool: list[Item] = []
    
    match world.options.randomize_breath:
        case 0: # default
            l = world.get_location("Dragon Village: Fire Breath")
            l.place_locked_item(world.create_item("Fire Breath"))
            itempool.extend((world.create_item("Electric Breath"), world.create_item("Water Breath"), world.create_item("Ice Breath")))
        case 1: # randomized
            breaths = ["Fire Breath", "Electric Breath", "Water Breath", "Ice Breath"]
            breath = world.random.choice(breaths)
            breaths.remove(breath)
            i = world.create_item(breath)
            l = world.get_location("Dragon Village: Fire Breath")
            l.place_locked_item(i)
            itempool.extend(world.create_item(i) for i in breaths)
        case 2: # none
            breaths = ["Fire Breath", "Electric Breath", "Water Breath", "Ice Breath"]
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

    if not world.options.randomize_sgt_byrd_minigames:
        for n in byrd_locations[0]:
            l = world.get_location(n)
            l.place_locked_item(world.create_item("Dragon Egg"))
            counts['Dragon Egg'] -= 1
        for n in byrd_locations[1]:
            l = world.get_location(n)
            l.place_locked_item(world.create_item("Light Gem"))
            counts['Light Gem'] -= 1
    
    if not world.options.randomize_blink_minigames:
        for n in blink_locations[0]:
            l = world.get_location(n)
            l.place_locked_item(world.create_item("Dragon Egg"))
            counts['Dragon Egg'] -= 1
        for n in blink_locations[1]:
            l = world.get_location(n)
            l.place_locked_item(world.create_item("Light Gem"))
            counts['Light Gem'] -= 1
    
    if not world.options.randomize_turret_minigames:
        for n in turret_locations[0]:
            l = world.get_location(n)
            l.place_locked_item(world.create_item("Dragon Egg"))
            counts['Dragon Egg'] -= 1
        for n in turret_locations[1]:
            l = world.get_location(n)
            l.place_locked_item(world.create_item("Light Gem"))
            counts['Light Gem'] -= 1
    
    if not world.options.randomize_sparx_minigames:
        for n in sparx_locations[0]:
            l = world.get_location(n)
            l.place_locked_item(world.create_item("Dragon Egg"))
            counts['Dragon Egg'] -= 1
        for n in sparx_locations[1]:
            l = world.get_location(n)
            l.place_locked_item(world.create_item("Light Gem"))
            counts['Light Gem'] -= 1
    
    if world.options.randomize_shop_items:
        itempool.extend(world.create_item(i) for i in ("Health Unit+", "Butterfly Jar", "Double Gems", "Shockwave"))
        itempool.extend(world.create_item("Lockpick") for _ in range(52))

        itempool.extend(world.create_item(i) for i in ('Fire Bomb', 'Water Bomb', 'Electric Bomb', 'Ice Bomb') for _ in range(3))
        itempool.append(world.create_item("Gem Pack"))

    for item in DEFAULT_ITEMS:
        for _ in range(counts.get(item, 1)):
            itempool.append(world.create_item(item))
    
    for i in range(21 - (12 if world.options.randomize_shop_items else 0)):
        itempool.append(world.create_item("Gem Pack"))

    world.multiworld.itempool.extend(itempool)
