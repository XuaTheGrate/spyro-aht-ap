from __future__ import annotations

from dataclasses import dataclass

from BaseClasses import CollectionState, Region
from rule_builder.options import OptionFilter
from rule_builder.rules import CanReachLocation, CanReachRegion, Has, HasAll, HasAllCounts, HasAny, HasAnyCount, Or, Rule, True_

from .options import MiscAllowImmediateRealmAccess, RandomizeShopItems

from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    from .world import SpyroAHTWorld

@dataclass
class DataRegion:
    name: str
    connections: list[str]
    locations: list[DataLocation]
    access_rule: Rule


@dataclass
class DataLocation:
    name: str
    id: int # important due to the nature of archipelago
    access_rule: Rule

REGIONS = {r.name: r for r in [
    DataRegion("Dragon Village", ["Dragon Village - After Elder Tomas"], [
        DataLocation("Dragon Village: Glide", 229, True_()),
        DataLocation("Dragon Village: Charge", 230, True_()),
        DataLocation("Dragon Village: Fire Breath", 231, True_()),
        DataLocation("Dragon Village: Swim", 232, True_()),
        DataLocation("Dragon Village: Double Jump from Elder Tomas", 1, True_())
    ], access_rule=True_()),

    DataRegion("Dragon Village - After Elder Tomas", ["Dragon Village - Gnasty Gnorcs Lair", "Crocoville Swamp", "Dragonfly Falls"], [
        DataLocation("Dragon Village: Dark Gem by Ember", 2, True_()),
        DataLocation("Dragon Village: Dark Gem by Elder Tomas", 3, True_()),
        DataLocation("Dragon Village: Dragon Egg after Hunter", 4, Has("Glide")),
        DataLocation("Dragon Village: Light Gem in Nursery", 5, Has("Glide")),
        DataLocation("Dragon Village: Locked Chest near Ball Gadget", 6, Has("Glide") & Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Dragon Village: Locked Chest on Cliff", 7, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Dragon Village: Dragon Egg behind breakable wall", 8, Has("Charge")),
        DataLocation("Dragon Village: Light Gem above Lab Secret Entrance", 9, Has("Charge")),
        DataLocation("Dragon Village: Light Gem across timed platforms", 10, HasAll("Charge", "Glide")),
        DataLocation("Dragon Village: Dark Gem by Sgt. Byrd", 11, HasAll("Charge", "Double Jump")),
        DataLocation("Dragon Village: Dragon Egg behind Dark Gem by Sgt. Byrd", 12, Has("Charge")),
        DataLocation("Dragon Village: Dragon Egg from Sgt. Byrd", 13, True_()),
        DataLocation("Dragon Village: Light Gem from Sgt. Byrd", 14, True_()),
        DataLocation("Dragon Village: Locked Chest before Crocoville Swamp", 15, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
    ], access_rule=Has("Double Jump")),

    # Double Jump (via Dragon Village - After Elder Tomas)
    DataRegion("Dragon Village - Gnasty Gnorcs Lair", [], [
        DataLocation("Dragon Village: Dragon Egg in Gnastys Lair", 16, True_()),
        DataLocation("Dragon Village: Lightning Breath from Gnasty Gnorc", 17, HasAny("Fire Breath", "Charge"))
    ], access_rule=Has("Dark Gem", 10)),

    # Double Jump (via Dragon Village - After Elder Tomas)
    DataRegion("Crocoville Swamp", ["Crocoville Swamp - After Elder Magnus"], [
        DataLocation("Crocoville Swamp: Dark Gem by Moneybags Pad", 18, True_()),
        DataLocation("Crocoville Swamp: Locked Chest behind breakable wall", 19, Has("Charge") & Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Crocoville Swamp: Dragon Egg across platforms in mud", 20, True_()),
        DataLocation("Crocoville Swamp: Light Gem behind reinforced door", 21, Has("Charge") & Has("Light Gem", 40)),
        DataLocation("Crocoville Swamp: Light Gem on top of pyramid", 22, Has("Glide")),
        DataLocation("Crocoville Swamp: Locked Chest before Dogs", 23, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Crocoville Swamp: Locked Chest in Temple", 24, HasAny("Fire Breath", "Lightning Breath", "Charge") & Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Crocoville Swamp: Light Gem in Temple", 25, True_()),
        DataLocation("Crocoville Swamp: Light Gem in secret room", 26, Has("Charge")),
        DataLocation("Crocoville Swamp: Dragon Egg from thief in temple", 27, HasAll("Charge", "Lightning Breath")),
        DataLocation("Crocoville Swamp: Light Gem after platforming", 28, HasAny("Fire Breath", "Lightning Breath") | HasAll("Ice Breath", "Charge")), # fuck the piranha plant
        DataLocation("Crocoville Swamp: Dragon Egg after pole spin left", 29, HasAll("Charge", "Pole Spin")),
        DataLocation("Crocoville Swamp: Dragon Egg from Blink", 30, True_()),
        DataLocation("Crocoville Swamp: Light Gem from Blink", 31, True_()),
        DataLocation("Crocoville Swamp: Dark Gem before Elder Magnus", 32, True_()),
        DataLocation("Crocoville Swamp: Pole Spin from Elder Magnus", 33, True_())
    ], access_rule=True_()),

    # Double Jump (via Dragon Village - After Elder Tomas)
    DataRegion("Crocoville Swamp - After Elder Magnus", [], [
        DataLocation("Crocoville Swamp: Dragon Egg in Elder Magnus House", 34, HasAll("Charge", "Glide")), # can be glided to
        DataLocation("Crocoville Swamp: Light Gem in Elder Magnus House", 35, True_()),
        DataLocation("Crocoville Swamp: Dark Gem above Blink", 36, True_()),
        DataLocation("Crocoville Swamp: Dragon Egg from Fredneck", 37, True_()),
        DataLocation("Crocoville Swamp: Light Gem from Fredneck", 38, True_()),
        # Achieveable without Glide
        DataLocation("Crocoville Swamp: Light Gem across the lilypads", 39, Has("Glide"))
    ], access_rule=Has("Pole Spin")),

    # Double Jump (via Dragon Village - After Elder Tomas)
    DataRegion("Dragonfly Falls", ["Dragonfly Falls - Vulture Dark Gem"], [
        DataLocation("Dragonfly Falls: Locked Chest near Ball Gadget", 40, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Dragonfly Falls: Dark Gem behind breakable wall", 41, HasAll("Charge", "Double Jump")),
        DataLocation("Dragonfly Falls: Dragon Egg after Dark Gem behind breakable wall", 42, Has("Charge")),
        DataLocation("Dragonfly Falls: Light Gem behind reinforced wall", 43, True_()),
    ], access_rule=Has("Light Gem", 8) & Has("Glide")),

    # Double Jump (via Dragon Village - After Elder Tomas)
    # Light Gem x8 & Glide (via Dragonfly Falls)
    DataRegion("Dragonfly Falls - Vulture Dark Gem", ["Dragonfly Falls - 70 Light Gem Door"], [
        DataLocation("Dragonfly Falls: Dark Gem near vultures", 44, True_()),
        DataLocation("Dragonfly Falls: Dragon Egg in vulture's nest", 45, True_()),
        DataLocation("Dragonfly Falls: Dark Gem before large pool", 46, True_()),
        DataLocation("Dragonfly Falls: Light Gem behind breakable wall in large pool", 47, Has("Swim")),
        DataLocation("Dragonfly Falls: Dragon Egg from Sparx", 48, True_()),
        DataLocation("Dragonfly Falls: Light Gem from Sparx", 49, True_()),
        DataLocation("Dragonfly Falls: Dragon Egg behind breakable wall above wall kick", 50, Has("Charge") & HasAny("Wall Kick", "Glide")),
        DataLocation("Dragonfly Falls: Light Gem in Piranha Pool", 51, True_()),
        DataLocation("Dragonfly Falls: Locked Chest in Piranha Pool", 52, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Dragonfly Falls: Dragon Egg in vultures nest (Hunter)", 53, True_()),
        DataLocation("Dragonfly Falls: Complete Hunters trial", 54, True_()),
        DataLocation("Dragonfly Falls: Dark Gem at end of zone", 55, True_()),
        DataLocation("Dragonfly Falls: Light Gem glide from wall kick", 58, HasAll("Wall Kick", "Glide"))
    ], access_rule=True_()),

    # Double Jump (via Dragon Village - After Elder Tomas)
    # Light Gem x8 & Glide (via Dragonfly Falls)
    DataRegion("Dragonfly Falls - 70 Light Gem Door", [], [
        DataLocation("Dragonfly Falls: Light Gem behind breakable wall beyond 70 Light Gem door", 56, True_()),
        DataLocation("Dragonfly Falls: Dragon Egg from thief beyond 70 Light Gem door", 57, True_()),
    ], access_rule=Has("Light Gem", 70) & Has("Charge")),

    DataRegion("Coastal Remains", ["Coastal Remains - Cloudy Domain Entrance", "Coastal Remains - After Otto", "Coastal Remains - 20 Light Gem Door", "Coastal Remains - After Cannon Dark Gem", "Coastal Remains - Ineptunes Lair"], [
        DataLocation("Coastal Remains: Dragon Egg from Turtle Mother", 63, Has("Charge")),
        DataLocation("Coastal Remains: Light Gem from Turtle Mother", 64, Has("Charge")),
        DataLocation("Coastal Remains: Dark Gem in cannon room", 65, HasAll("Glide", "Double Jump")),
        DataLocation("Coastal Remains: Light Gem at beach above water mill", 69, HasAll("Water Breath", "Double Jump")),
        DataLocation("Coastal Remains: Dragon Egg after Piranha pool", 78, HasAll("Double Jump", "Glide")),
        DataLocation("Coastal Remains: Locked Chest behind Moneybags", 234, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Coastal Remains: Locked Chest hidden on beach", 235, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)])))
    ], access_rule=(
        True_(options=[OptionFilter(MiscAllowImmediateRealmAccess, 1)])) |
        CanReachRegion("Dragon Village - Gnasty Gnorcs Lair", options=[OptionFilter(MiscAllowImmediateRealmAccess, 0)])
    ),

    DataRegion("Coastal Remains - Cloudy Domain Entrance", ["Cloudy Domain"], [
        DataLocation("Coastal Remains: Light Gem after Windmills", 59, Has("Pole Spin")),
        DataLocation("Coastal Remains: Light Gem beyond moving platform", 60, Has("Lightning Breath")),
    ], access_rule=HasAll("Glide", "Double Jump")),

    DataRegion("Coastal Remains - 20 Light Gem Door", [], [
        DataLocation("Coastal Remains: Dragon Egg from thief beyond 20 Light Gem door", 61, Has("Charge")),
        DataLocation("Coastal Remains: Light Gem in 20 Light Gem door", 62, True_())
    ], access_rule=Has("Light Gem", 20)),

    DataRegion("Coastal Remains - After Cannon Dark Gem", [], [
        DataLocation("Coastal Remains: Dragon Egg in cannon room", 66, True_()),
        DataLocation("Coastal Remains: Dark Gem after Swinging Shells", 67, Has("Charge")),
        DataLocation("Coastal Remains: Dragon Egg after moving platforms", 68, True_())
    ], access_rule=HasAll("Pole Spin", "Double Jump", "Glide")),

    DataRegion("Coastal Remains - After Otto", ["Sunken Ruins"], [
        DataLocation("Coastal Remains: Light Gem in Ottos pool", 70, True_()),
        DataLocation("Coastal Remains: Light Gem reward from Otto", 71, True_()),
        DataLocation("Coastal Remains: Dragon Egg from Blink", 72, True_()),
        DataLocation("Coastal Remains: Light Gem from Blink", 73, True_()),
        DataLocation("Coastal Remains: Dark Gem near Blink", 74, True_()),
        DataLocation("Coastal Remains: Dragon Egg after Crossbow Gnorcs", 75, Has("Lightning Breath")),
        DataLocation("Coastal Remains: Dark Gem before Sunken Ruins", 76, True_()),
        DataLocation("Coastal Remains: Light Gem before Sunken Ruins", 77, True_()),
    ], access_rule=HasAll("Pole Spin", "Double Jump")),

    DataRegion("Coastal Remains - Ineptunes Lair", [], [
        DataLocation("Coastal Remains: Water Breath from Ineptune", 79, True_())
    ], access_rule=Has("Dark Gem", 20) & Has("Charge")),

    # Double Jump & Glide (via Coastal Remains - Cloudy Domain Entrance)
    DataRegion("Cloudy Domain", ["Cloudy Domain - After Elder Titan"], [
        DataLocation("Cloudy Domain: Locked Chest at entrance", 80, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Cloudy Domain: Dark Gem after locked door", 81, True_()),
        DataLocation("Cloudy Domain: Light Gem before Elder Titan", 82, True_()),
    ], access_rule=True_()),

    # Double Jump & Glide (via Coastal Remains - Cloudy Domain Entrance)
    DataRegion("Cloudy Domain - After Elder Titan", ["Cloudy Domain - Wing Shield"], [
        DataLocation("Cloudy Domain: Wing Shield from Elder Titan", 83, True_()),
        DataLocation("Cloudy Domain: Dragon Egg after Elder Titan", 84, True_()),
        DataLocation("Cloudy Domain: Locked Chest beyond Reinforced Door", 85, Has("Light Gem", 40) & Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Cloudy Domain: Locked Chest after Crossroads left", 87, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Cloudy Domain: Light Gem after platforming at Crossroads left", 88, True_())
    ], access_rule=Has("Charge")),

    # Double Jump & Glide (via Coastal Remains - Cloudy Domain Entrance)
    # Charge (via Cloudy Domain - After Elder Titan)
    DataRegion("Cloudy Domain - Wing Shield", [], [
        DataLocation("Cloudy Domain: Locked Chest in Wing Shield Tutorial", 236, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Cloudy Domain: Light Gem after Wing Shield Tutorial", 86, True_()),
        DataLocation("Cloudy Domain: Light Gem after temporary platforms at Crossroads right", 89, True_()),
        DataLocation("Cloudy Domain: Dragon Egg on temporary platform after Crossroads right", 90, True_()),
        DataLocation("Cloudy Domain: Dragon Egg from thief after rotating platforms", 91, True_()),
        DataLocation("Cloudy Domain: Dark Gem after rotating platforms", 92, True_()),
        DataLocation("Cloudy Domain: Dragon Egg from Sgt. Byrd", 93, True_()),
        DataLocation("Cloudy Domain: Light Gem from Sgt. Byrd", 94, True_()),
        DataLocation("Cloudy Domain: Light Gem after Sgt. Byrd", 95, Has("Wall Kick")),
        DataLocation("Cloudy Domain: Dark Gem after Sgt. Byrd", 96, True_()),
        DataLocation("Cloudy Domain: Dragon Egg in Ball Gadget", 97, True_()),
        DataLocation("Cloudy Domain: Light Gem in Ball Gadget", 98, True_()),
    ], access_rule=Has("Wing Shield")),

    # Double Jump & Pole Spin (via Coastal Remains - After Otto)
    DataRegion("Sunken Ruins", ["Sunken Ruins - Invulnerability Gadget"], [
        # Logically this location does not need swim, but it's far easier to include it
        DataLocation("Sunken Ruins: Locked Chest at entrance", 237, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Sunken Ruins: Locked Chest behind Swim Exit", 99, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Sunken Ruins: Dark Gem after Swim", 100, True_()),
        DataLocation("Sunken Ruins: Dragon Egg above Dark Gem", 101, Has("Glide")),
        DataLocation("Sunken Ruins: Locked Chest above Dark Gem", 102, Has("Glide") & Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Sunken Ruins: Locked Chest behind Lily", 103, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Sunken Ruins: Light Gem after Acid Swim", 104, Has("Light Gem", 24)),
        DataLocation("Sunken Ruins: Dragon Egg from Sparx", 105, True_()),
        DataLocation("Sunken Ruins: Light Gem from Sparx", 106, True_()),
        DataLocation("Sunken Ruins: Dragon Egg above heated wall kick", 107, Has("Light Gem", 24) & Has("Wall Kick")),
        DataLocation("Sunken Ruins: Locked Chest near fish", 108, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Sunken Ruins: Light Gem after fish", 109, True_())
    ], access_rule=Has("Swim")),

    # Double Jump & Pole Spin (via Coastal Remains - After Otto)
    # Swim (via Sunken Ruins)
    DataRegion("Sunken Ruins - Invulnerability Gadget", [], [
        DataLocation("Sunken Ruins: Light Gem inside Acid Swim", 110, True_()),
        DataLocation("Sunken Ruins: Dark Gem after Acid Swim", 111, True_()),
        DataLocation("Sunken Ruins: Locked Chest after Dark Gem", 112, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Sunken Ruins: Dark Gem under Acid Pool", 113, True_()),
        DataLocation("Sunken Ruins: Locked Chest near Acid Pool Dark Gem", 114, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Sunken Ruins: Locked Chest after Acid Pool Dark Gem", 115, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)])))
    ], access_rule=HasAll("Lightning Breath", "Glide") & Has("Light Gem", 24)),

    DataRegion("Frostbite Village", ["Frostbite Village - After Phils Gate", "Frostbite Village - After Horn Dive Switch", "Frostbite Village - Reds Lair"], [
    ], access_rule=(
        True_(options=[OptionFilter(MiscAllowImmediateRealmAccess, 1)]) |
        CanReachRegion("Coastal Remains - Ineptunes Lair", options=[OptionFilter(MiscAllowImmediateRealmAccess, 0)])
    )),

    DataRegion("Frostbite Village - After Horn Dive Switch", ["Frostbite Village - Before Gloomy Glacier"], [
        DataLocation("Frostbite Village: Dark Gem under avalanche", 121, True_()),
        DataLocation("Frostbite Village: Dragon Egg from thief after spinning totem", 122, Has("Charge")),
        DataLocation("Frostbite Village: Light Gem after spinning totem after thief", 123, True_()),
        DataLocation("Frostbite Village: Dragon Egg from Blink", 124, True_()),
        DataLocation("Frostbite Village: Light Gem from Blink", 125, True_()),
    ], access_rule=Has("Double Jump")),

    DataRegion("Frostbite Village - Reds Lair", [], [
        DataLocation("Frostbite Village: Ice Breath from Red", 136, True_())
        # a breath is required to kill the dogs
    ], access_rule=HasAny("Fire Breath", "Lightning Breath", "Charge") & Has("Dark Gem", 30)),

    DataRegion("Frostbite Village - After Phils Gate", [], [
        DataLocation("Frostbite Village: Light Gem after Phils Gate", 116, HasAll("Water Breath", "Double Jump", "Glide")),
        DataLocation("Frostbite Village: Dragon Egg from Peggy", 117, True_()),
        DataLocation("Frostbite Village: Light Gem from Peggy", 118, True_()),
        DataLocation("Frostbite Village: Dark Gem near Peggy", 119, Has("Double Jump")),
        DataLocation("Frostbite Village: Dragon Egg after Dark Gem near Peggy", 120, Has("Double Jump")),
        DataLocation("Frostbite Village: Locked Chest by Dragon Egg", 238, Has("Double Jump") & Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)])))
    ], access_rule=HasAll("Lightning Breath", "Charge")),

    # Double Jump (via Frostbite Village - After Horn Dive Switch)
    DataRegion("Frostbite Village - Before Gloomy Glacier", ["Gloomy Glacier", "Frostbite Village - Wall Kick"], [
        DataLocation("Frostbite Village: Dragon Egg behind breakable wall", 130, Has("Charge")),
        DataLocation("Frostbite Village: Return to Manny", 135, True_())
    ], access_rule=Has("Glide")),

    # Double Jump (via Frostbite Village - After Horn Dive Switch)
    DataRegion("Frostbite Village - Wall Kick", [], [
        DataLocation("Frostbite Village: Dark Gem in slippery room", 131, True_()),
        DataLocation("Frostbite Village: Light Gem in slippery room", 132, True_())
    ], access_rule=Has("Wall Kick")),

    # Double Jump (via Frostbite Village - After Horn Dive Switch)
    # Glide (via Frostbite Village - Before Gloomy Glacier)
    DataRegion("Gloomy Glacier", ["Ice Citadel"], [
        DataLocation("Gloomy Glacier: Locked Chest in Bentleys Living Room", 239, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Gloomy Glacier: Locked Chest in Bentleys Bedroom", 137, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Gloomy Glacier: Reward from Bentley", 138, True_()),
        DataLocation("Gloomy Glacier: Light Gem in Ambush room", 139, True_()),
        DataLocation("Gloomy Glacier: Locked Chest after Ambush room", 140, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Gloomy Glacier: Dragon Egg behind breakable wall in swinging rocks", 141, True_()),
        DataLocation("Gloomy Glacier: Light Gem behind Yeti behind breakable bones", 142, True_()),
        DataLocation("Gloomy Glacier: Dragon Egg under bone platform", 143, True_()),
        DataLocation("Gloomy Glacier: Light Gem behind Yeti in temporary platform room", 144, True_()),
        DataLocation("Gloomy Glacier: Dragon Egg after spinning bones", 145, True_()),
        DataLocation("Gloomy Glacier: Dragon Egg from Sparx", 146, True_()),
        DataLocation("Gloomy Glacier: Light Gem from Sparx", 147, True_()),
        # This one is a bit vague but i'm not sure how to word it better
        DataLocation("Gloomy Glacier: Light Gem after moving platform right of entrance", 148, True_()),
        DataLocation("Gloomy Glacier: Light Gem behind locked door above climbable wall", 149, True_()),
        DataLocation("Gloomy Glacier: Light Gem at end of zone", 150, True_())
    ], access_rule=True_()),
    
    # Double Jump (via Frostbite Village - After Horn Dive Switch)
    # Glide (via Frostbite Village - Before Gloomy Glacier)
    DataRegion("Ice Citadel", ["Ice Citadel - Inner"], [
        DataLocation("Ice Citadel: Locked Chest in entrance", 240, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Ice Citadel: Reward for lighting 1 boiler", 151, Has("Fire Breath")),
        DataLocation("Ice Citadel: Light Gem above moving platform", 152, True_())
    ], access_rule=True_()),

    # Double Jump (via Frostbite Village - After Horn Dive Switch)
    # Glide (via Frostbite Village - Before Gloomy Glacier)
    DataRegion("Ice Citadel - Inner", ["Ice Citadel - Above Elder Astor"], [
        DataLocation("Ice Citadel: Locked Chest behind breakable wall", 153, Has("Charge") & Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)])))
    ], access_rule=Has("Water Breath")),

    # the extra breaths + charge rule is required because the armoured gnorc in front of the door must be defeated before you can access elder astor's dark gem
    # Double Jump (via Frostbite Village - After Horn Dive Switch)
    # Glide (via Frostbite Village - Before Gloomy Glacier)
    # Water Breath (via Ice Citadel - Inner)
    DataRegion("Ice Citadel - Above Elder Astor", ["Ice Citadel - After Elder Astor"], [
        DataLocation("Ice Citadel: Dark Gem above Elder Astor", 154, True_()),
        DataLocation("Ice Citadel: Wall Kick from Elder Astor", 155, True_())
    ], access_rule=HasAny("Fire Breath", "Lightning Breath", "Ice Breath") & Has("Charge")),

    # Double Jump (via Frostbite Village - After Horn Dive Switch)
    # Glide (via Frostbite Village - Before Gloomy Glacier)
    # Water Breath (via Ice Citadel - Inner)
    # (Fire Breath | Lightning Breath | Ice Breath) & Charge via (Ice Citadel - Above Elder Astor)
    DataRegion("Ice Citadel - After Elder Astor", ["Frostbite Village - Reinforced Door"], [
        DataLocation("Ice Citadel: Locked Chest after Elder Astor", 156, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Ice Citadel: Dark Gem after sewer sprint", 157, Has("Light Gem", 40)),
        DataLocation("Ice Citadel: Dragon Egg after Dark Gem in sewer", 158, Has("Light Gem", 40)),
        DataLocation("Ice Citadel: Locked Chest in supercharge tunnel", 241, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Ice Citadel: Locked Chest before reinforced wall", 242, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Ice Citadel: Dragon Egg beind reinforced wall", 159, Has("Light Gem", 40)),
        DataLocation("Ice Citadel: Dragon Egg from Sgt. Byrd", 160, True_()),
        DataLocation("Ice Citadel: Light Gem from Sgt. Byrd", 161, True_()),
        DataLocation("Ice Citadel: Reward for lighting 3 boilers", 162, Has("Fire Breath")),
        DataLocation("Ice Citadel: Locked Chest by Ice Princess", 243, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Ice Citadel: Dark Gem after Ice Princess", 163, True_()),
        DataLocation("Ice Citadel: Dragon Egg after pole spin after Yetis", 164, Has("Pole Spin")),
        DataLocation("Ice Citadel: Dark Gem after Yetis", 165, HasAll("Lightning Breath", "Pole Spin")),
        DataLocation("Ice Citadel: Dragon Egg beind cannon reinforced wall", 166, True_()),
        DataLocation("Ice Citadel: Light Gem beind cannon reinforced wall", 167, True_()),
        DataLocation("Ice Citadel: Reward for lighting 5 boilers", 168, Has("Fire Breath")),
        DataLocation("Ice Citadel: Reward for lighting all boilers from Ice Princess", 169, Has("Fire Breath")),
        DataLocation("Ice Citadel: Dark Gem above slippery slope", 170, Has("Light Gem", 40)),
        DataLocation("Ice Citadel: Dragon Egg from thief after Dark Gem", 171, Has("Light Gem", 40)),
    ], access_rule=Has("Wall Kick")),

    # Double Jump (via Frostbite Village - After Horn Dive Switch)
    # Glide (via Frostbite Village - Before Gloomy Glacier)
    # Water Breath (via Ice Citadel - Inner)
    # (Fire Breath | Lightning Breath | Ice Breath) & Charge via (Ice Citadel - Above Elder Astor)
    # Wall Kick (via Ice Citadel - After Elder Astor)
    DataRegion("Frostbite Village - Reinforced Door", ["Frostbite Village - 95 Light Gem Door"], [
        DataLocation("Frostbite Village: Light Gem through reinforced door to Frostbite Village", 172, True_()),
        DataLocation("Frostbite Village: Dark Gem after reinforced door", 126, True_()),
        DataLocation("Frostbite Village: Dark Gem after falling icicles", 127, True_()),
        DataLocation("Frostbite Village: Locked Chest in falling icicles room", 128, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Frostbite Village: Light Gem after falling icicles", 129, Has("Pole Spin")),
        DataLocation("Frostbite Village: Locked Chest under platform after falling icicles", 244, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)])))
    ], access_rule=Has("Light Gem", 40)),

    # Double Jump (via Frostbite Village - After Horn Dive Switch)
    # Glide (via Frostbite Village - Before Gloomy Glacier)
    # Water Breath (via Ice Citadel - Inner)
    # (Fire Breath | Lightning Breath | Ice Breath) & Charge via (Ice Citadel - Above Elder Astor)
    # Wall Kick (via Ice Citadel - After Elder Astor)
    # Light Gem x40 (via Frostbite Village - Reinforced Door)
    DataRegion("Frostbite Village - 95 Light Gem Door", [], [
        DataLocation("Frostbite Village: Locked Chest beyond 95 Light Gem Door", 133, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Frostbite Village: Light Gem beyond 95 Light Gem Door", 134, True_())
    ], access_rule=Has("Light Gem", 95)),

    DataRegion("Stormy Beach", ["Molten Mount"], [
        DataLocation("Stormy Beach: Locked Chest 1 in left cove by teleporter", 245, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Stormy Beach: Locked Chest 2 in left cove by teleporter", 246, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Stormy Beach: Light Gem in left cove by teleporter", 173, Has("Double Jump")),
        DataLocation("Stormy Beach: Dragon Egg from thief underneath Moneybags", 174, Has("Charge")),
        DataLocation("Stormy Beach: Locked Chest by Wally", 247, Has("Double Jump") & Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Stormy Beach: Dragon Egg from Wally", 175, Has("Double Jump")),
        DataLocation("Stormy Beach: Light Gem from Wally", 176, Has("Double Jump")),
        DataLocation("Stormy Beach: Locked Chest after armored Gnorc", 248, Has("Double Jump") & Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Stormy Beach: Locked Chest guarded by crossbow Gnorcs", 249, HasAll("Glide", "Double Jump", "Wall Kick") & Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Stormy Beach: Dark Gem at entrance to volcano", 177, Has("Double Jump"))
    ], access_rule=(
        True_(options=[OptionFilter(MiscAllowImmediateRealmAccess, 1)]) |
        CanReachRegion("Frostbite Village - Reds Lair", options=[OptionFilter(MiscAllowImmediateRealmAccess, 0)])
    )),

    DataRegion("Molten Mount", ["Molten Mount - Pole Spin"], [
        DataLocation("Molten Mount: Dark Gem after Rock Monsters", 178, Has("Double Jump")),
        DataLocation("Molten Mount: Reward from Teena", 179, Has("Charge")),
        DataLocation("Molten Mount: Dragon Egg across Imp platforms", 180, True_()),
        DataLocation("Molten Mount: Dragon Egg from Sgt. Byrd", 181, True_()),
        DataLocation("Molten Mount: Light Gem from Sgt. Byrd", 182, True_()),
        DataLocation("Molten Mount: Locked Chest next to Sgt. Byrd", 183, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Molten Mount: Light Gem behind Imp", 184, True_())
    ], access_rule=HasAny("Water Breath", "Ice Breath") & HasAll("Double Jump", "Glide")),

    # Double Jump & Glide & (Water Breath | Ice Breath) via (Molten Mount)
    DataRegion("Molten Mount - Pole Spin", ["Magma Falls Top"], [
        DataLocation("Molten Mount: Light Gem after Imp ambush", 185, True_()),
        DataLocation("Molten Mount: Dark Gem before lava fall", 186, True_()),
        DataLocation("Molten Mount: Light Gem after platform challenge", 187, Has("Charge") & Has("Light Gem", 24)),
        DataLocation("Molten Mount: Locked Chest behind breakable wall", 188, Has("Charge") & Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Molten Mount: Dragon Egg from thief", 189, Has("Charge")),
        DataLocation("Molten Mount: Locked Chest in thief room", 250, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Molten Mount: Locked Chest behind breakable wall near end of zone", 190, Has("Charge") & Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Molten Mount: Dark Gem at end of zone", 191, True_())
    ], access_rule=Has("Pole Spin")),

    # Double Jump & Glide & (Water Breath | Ice Breath) via (Molten Mount)
    # Pole Spin (via Molten Mount - Pole Spin)
    DataRegion("Magma Falls Top", ["Magma Falls - Ball Gadget"], [
        DataLocation("Magma Falls Top: Light Gem in wall kick room", 192, True_()),
        DataLocation("Magma Falls Top: Locked Chest behind Moneybags", 193, Has("Charge") & Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Magma Falls Top: Locked Chest above Imps", 251, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)])))
    ], access_rule=Has("Wall Kick")),

    # Double Jump & Glide & (Water Breath | Ice Breath) via (Molten Mount)
    # Pole Spin (via Molten Mount - Pole Spin)
    # Wall Kick (via Magma Falls Top)
    DataRegion("Magma Falls - Ball Gadget", ["Magma Falls Bottom"], [
        DataLocation("Magma Falls Top: Dragon Egg 1 in Ball Gadget", 194, True_()),
        DataLocation("Magma Falls Top: Light Gem 1 in Ball Gadget", 195, True_()),
        DataLocation("Magma Falls Top: Dragon Egg 2 in Ball Gadget", 196, True_()),
        DataLocation("Magma Falls Top: Light Gem 2 in Ball Gadget", 197, True_())
    ], access_rule=True_()),

    # Double Jump & Glide & (Water Breath | Ice Breath) via (Molten Mount)
    # Pole Spin (via Molten Mount - Pole Spin)
    # Wall Kick (via Magma Falls Top)
    DataRegion("Magma Falls Bottom", ["Dark Mine"], [
        DataLocation("Magma Falls Bottom: Dark Gem above wall kick", 198, True_()),
        DataLocation("Magma Falls Bottom: Locked Chest after Dark Gem", 199, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Magma Falls Bottom: Light Gem after Imp platforming", 200, True_()),
        DataLocation("Magma Falls Bottom: Dragon Egg from Sparx", 202, True_()),
        DataLocation("Magma Falls Bottom: Light Gem from Sparx", 203, True_()),
        DataLocation("Magma Falls Bottom: Dragon Egg from thief behind breakable wall", 201, Has("Charge"))
    ], access_rule=True_()),

    # Double Jump & Glide & (Water Breath | Ice Breath) via (Molten Mount)
    # Pole Spin (via Molten Mount - Pole Spin)
    # Wall Kick (via Magma Falls Top)
    DataRegion("Dark Mine", ["Dark Mine - 45 Light Gem Door", "Dark Mine - Steam Vents"], [
        DataLocation("Dark Mine: Locked Chest at entrance", 252, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Dark Mine: Locked Chest by bear traps", 206, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Dark Mine: Locked Chest glide from Green Robo-Gnorc", 207, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Dark Mine: Light Gem over wall after locked chest", 208, True_()),
        DataLocation("Dark Mine: Dark Gem in laser gun room", 209, True_()),
        DataLocation("Dark Mine: Dragon Egg from Blink", 210, True_()),
        DataLocation("Dark Mine: Light Gem from Blink", 211, True_()),
        DataLocation("Dark Mine: Dragon Egg below shield Robo-Gnorc", 212, True_())
    ], access_rule=HasAll("Ice Breath", "Charge") | Has("Lightning Breath")),

    # Double Jump & Glide & (Water Breath | Ice Breath) via (Molten Mount)
    # Pole Spin (via Molten Mount - Pole Spin)
    # Wall Kick (via Magma Falls Top)
    # (Ice Breath & Charge) | Lightning Breath (via Dark Mine)
    DataRegion("Dark Mine - 45 Light Gem Door", [], [
        DataLocation("Dark Mine: Light Gem in Acid Pool beyond 45 Light Gem Door", 204, True_()),
        DataLocation("Dark Mine: Dragon Egg in Acid Pool beyond 45 Light Gem Door", 205, True_())
    ], access_rule=Has("Light Gem", 45) & Has("Swim")),

    # Double Jump & Glide & (Water Breath | Ice Breath) via (Molten Mount)
    # Pole Spin (via Molten Mount - Pole Spin)
    # Wall Kick (via Magma Falls Top)
    # (Ice Breath & Charge) | Lightning Breath (via Dark Mine)
    DataRegion("Dark Mine - Steam Vents", ["Red's Laboratory"], [
        DataLocation("Dark Mine: Light Gem in temporary platform room", 213, True_()),
        DataLocation("Dark Mine: Dragon Egg next to Moneybags", 214, True_()),
        DataLocation("Dark Mine: Light Gem on platform above wall kick", 215, True_()),
        DataLocation("Dark Mine: Dark Gem after pole spin", 216, True_())
    ], access_rule=Has("Ice Breath")),

    # Double Jump & Glide & (Water Breath?) via (Molten Mount)
    # Pole Spin (via Molten Mount - Pole Spin)
    # Wall Kick (via Magma Falls Top)
    # Charge | Lightning Breath (via Dark Mine)
    # Ice Breath via (Dark Mine - Steam Vents)
    DataRegion("Red's Laboratory", [], [
        DataLocation("Red's Laboratory: Locked Chest after pole spin", 253, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Red's Laboratory: Locked Chest above 4 charge switches", 254, Or(True_(options=[OptionFilter(RandomizeShopItems, 0)]), Has("Lockpick", 52, options=[OptionFilter(RandomizeShopItems, 1)]))),
        DataLocation("Red's Laboratory: Dragon Egg from thief in hub area", 217, True_()),
        DataLocation("Red's Laboratory: Light Gem after pole spin in SE section", 218, True_()),
        DataLocation("Red's Laboratory: Dark Gem in sealed chamber after laser parkour in SE section", 219, True_()),
        DataLocation("Red's Laboratory: Light Gem above boiler elevator in SE section", 220, Has("Fire Breath")),
        DataLocation("Red's Laboratory: Dragon Egg behind lasers in SE section", 221, True_()),
        DataLocation("Red's Laboratory: Dragon Egg in piston room W section", 222, True_()),
        DataLocation("Red's Laboratory: Light Gem after laser parkour in W section", 223, True_()),
        DataLocation("Red's Laboratory: Dark Gem in sealed chamber in W section", 224, True_()),
        DataLocation("Red's Laboratory: Light Gem after pole spin by Dark Gem in W section", 225, True_()),
        DataLocation("Red's Laboratory: Light Gem after metal press", 226, Has("Light Gem", 24)),
        DataLocation("Red's Laboratory: Dark Gem guarded by Staff Robo-Gnorcs", 227, True_())
    ], access_rule=True_())
]}


def create_and_connect_regions(world: SpyroAHTWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: SpyroAHTWorld) -> None:
    for region in REGIONS.keys():
        r = Region(region, world.player, world.multiworld)
        world.multiworld.regions.append(r)


def connect_regions(world: SpyroAHTWorld) -> None:
    for region in REGIONS.values():
        r = world.get_region(region.name)
        for con in region.connections:
            c = world.get_region(con)
            entrance = region.name.replace(' ', '') + '=>' + con.replace(' ', '')
            r.connect(c, entrance, rule=REGIONS[con].access_rule)
            REGIONS[con].access_rule.to_dict()
    
    if world.options.misc_allow_immediate_realm_access:
        dv = world.get_region("Dragon Village")
        dv.connect(world.get_region("Coastal Remains"), "DragonVillage=>CoastalRemains")
        dv.connect(world.get_region("Frostbite Village"), "DragonVillage=>FrostbiteVillage")
        dv.connect(world.get_region("Stormy Beach"), "DragonVillage=>StormyBeach")
    else:
        world.get_region("Dragon Village - Gnasty Gnorcs Lair").connect(world.get_region("Coastal Remains"), "DragonVillage-GnastyGnorcsLair=>CoastalRemains")
        world.get_region("Coastal Remains - Ineptunes Lair").connect(world.get_region("Frostbite Village"), "CoastalRemains-IneptunesLair=>FrostbiteVillage")
        world.get_region("Frostbite Village - Reds Lair").connect(world.get_region("Stormy Beach"), "FrostbiteVillage-RedsLair=>StormyBeach")
