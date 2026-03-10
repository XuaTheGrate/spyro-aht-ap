from __future__ import annotations

from dataclasses import dataclass

from BaseClasses import CollectionState, Region

from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    from .world import SpyroAHTWorld


AccessRule = Callable[['SpyroAHTWorld'], Callable[[CollectionState], bool]]


@dataclass
class DataRegion:
    name: str
    connections: list[str]
    locations: list[DataLocation]
    access_rule: AccessRule


@dataclass
class DataLocation:
    name: str
    id: int # important due to the nature of archipelago
    access_rule: AccessRule


_DEFAULT_RULE = lambda _: lambda __: True


def _builder_all(**items: int) -> AccessRule:
    return lambda world: lambda state: state.has_all_counts(items, world.player)


def _builder_any(**items: int) -> AccessRule:
    return lambda world: lambda state: state.has_any_count(items, world.player)


REGIONS = {r.name: r for r in [
    DataRegion("Dragon Village", ["Dragon Village - After Elder Tomas"], [
        DataLocation("Dragon Village: Glide", 229, _DEFAULT_RULE),
        DataLocation("Dragon Village: Charge", 230, _DEFAULT_RULE),
        DataLocation("Dragon Village: Fire Breath", 231, _DEFAULT_RULE),
        DataLocation("Dragon Village: Swim", 232, _DEFAULT_RULE),
        DataLocation("Dragon Village: Double Jump from Elder Tomas", 1, _DEFAULT_RULE)
    ], access_rule=_DEFAULT_RULE),

    # Implied: Double Jump
    DataRegion("Dragon Village - After Elder Tomas", ["Dragon Village - Gnasty Gnorcs Lair", "Crocoville Swamp", "Dragonfly Falls"], [
        DataLocation("Dragon Village: Dark Gem by Ember", 2, _DEFAULT_RULE),
        DataLocation("Dragon Village: Dark Gem by Elder Tomas", 3, _DEFAULT_RULE),
        DataLocation("Dragon Village: Dragon Egg after Hunter", 4, _builder_all(Glide=1)),
        DataLocation("Dragon Village: Light Gem in Nursery", 5, _builder_all(Glide=1)),
        DataLocation("Dragon Village: Locked Chest near Ball Gadget", 6, _builder_all(Glide=1)),
        DataLocation("Dragon Village: Locked Chest on Cliff", 7, _DEFAULT_RULE),
        DataLocation("Dragon Village: Dragon Egg behind breakable wall", 8, _builder_all(Charge=1)),
        DataLocation("Dragon Village: Light Gem above Lab Secret Entrance", 9, _builder_all(Charge=1)),
        DataLocation("Dragon Village: Light Gem across timed platforms", 10, _builder_all(Charge=1, Glide=1)),
        DataLocation("Dragon Village: Dark Gem by Sgt. Byrd", 11, _builder_all(Charge=1)),
        DataLocation("Dragon Village: Dragon Egg behind Dark Gem by Sgt. Byrd", 12, _builder_all(Charge=1)),
        DataLocation("Dragon Village: Dragon Egg from Sgt. Byrd", 13, _DEFAULT_RULE),
        DataLocation("Dragon Village: Light Gem from Sgt. Byrd", 14, _DEFAULT_RULE),
        DataLocation("Dragon Village: Locked Chest before Crocoville Swamp", 15, _DEFAULT_RULE),
    ], access_rule=lambda world: lambda state: state.has("Double Jump", world.player)),

    # Implied: Double Jump
    DataRegion("Dragon Village - Gnasty Gnorcs Lair", [], [
        DataLocation("Dragon Village: Dragon Egg in Gnastys Lair", 16, _DEFAULT_RULE),
        DataLocation("Dragon Village: Lightning Breath from Gnasty Gnorc", 17, _builder_any(**{"Fire Breath":1,"Charge":1}))
    ], access_rule=lambda world: lambda state: state.has("Dark Gem", world.player, 10)),

    # Implied: Double Jump
    DataRegion("Crocoville Swamp", ["Crocoville Swamp - After Elder Magnus"], [
        DataLocation("Crocoville Swamp: Dark Gem by Moneybags Pad", 18, _DEFAULT_RULE),
        DataLocation("Crocoville Swamp: Locked Chest behind breakable wall", 19, _builder_all(Charge=1)),
        DataLocation("Crocoville Swamp: Dragon Egg across platforms in mud", 20, _DEFAULT_RULE),
        DataLocation("Crocoville Swamp: Light Gem behind reinforced door", 21, _builder_all(Charge=1,**{"Light Gem": 40})),
        DataLocation("Crocoville Swamp: Light Gem on top of pyramid", 22, _builder_all(Glide=1)),
        DataLocation("Crocoville Swamp: Locked Chest before Dogs", 23, _DEFAULT_RULE),
        DataLocation("Crocoville Swamp: Locked Chest in Temple", 24, _builder_any(**{"Fire Breath":1,"Lightning Breath":1,"Charge":1})),
        DataLocation("Crocoville Swamp: Light Gem in Temple", 25, _DEFAULT_RULE),
        DataLocation("Crocoville Swamp: Light Gem in secret room", 26, _builder_all(Charge=1)),
        DataLocation("Crocoville Swamp: Dragon Egg from thief in temple", 27, _builder_all(**{"Charge":1,"Lightning Breath":1})),
        DataLocation("Crocoville Swamp: Light Gem after platforming", 28, _DEFAULT_RULE),
        DataLocation("Crocoville Swamp: Dragon Egg after pole spin left", 29, _builder_all(Charge=1,**{"Pole Spin":1})),
        DataLocation("Crocoville Swamp: Dragon Egg from Blink", 30, _DEFAULT_RULE),
        DataLocation("Crocoville Swamp: Light Gem from Blink", 31, _DEFAULT_RULE),
        DataLocation("Crocoville Swamp: Dark Gem before Elder Magnus", 32, _DEFAULT_RULE),
        DataLocation("Crocoville Swamp: Pole Spin from Elder Magnus", 33, _DEFAULT_RULE)
    ], access_rule=_DEFAULT_RULE),

    # Implied: Double Jump, Pole Spin
    DataRegion("Crocoville Swamp - After Elder Magnus", [], [
        DataLocation("Crocoville Swamp: Dragon Egg in Elder Magnus House", 34, _builder_any(Charge=1,Glide=1)), # can be glided to
        DataLocation("Crocoville Swamp: Light Gem in Elder Magnus House", 35, _DEFAULT_RULE),
        DataLocation("Crocoville Swamp: Dark Gem above Blink", 36, _DEFAULT_RULE),
        DataLocation("Crocoville Swamp: Dragon Egg from Fredneck", 37, _DEFAULT_RULE),
        DataLocation("Crocoville Swamp: Light Gem from Fredneck", 38, _DEFAULT_RULE),
        # Achieveable without Glide
        DataLocation("Crocoville Swamp: Light Gem across the lilypads", 39, _builder_all(Glide=1))
    ], access_rule=_builder_all(**{"Pole Spin":1})),

    DataRegion("Dragonfly Falls", ["Dragonfly Falls - Vulture Dark Gem"], [
        DataLocation("Dragonfly Falls: Locked Chest near Ball Gadget", 40, _builder_all(Glide=1)),
        DataLocation("Dragonfly Falls: Dark Gem behind breakable wall", 41, _builder_all(Charge=1)),
        DataLocation("Dragonfly Falls: Dragon Egg after Dark Gem behind breakable wall", 42, _builder_all(Charge=1)),
        DataLocation("Dragonfly Falls: Light Gem behind reinforced wall", 43, _builder_all(Glide=1)),
    ], access_rule=_builder_all(**{"Light Gem": 8})),

    # Implied: Double Jump, Glide
    DataRegion("Dragonfly Falls - Vulture Dark Gem", ["Dragonfly Falls - 70 Light Gem Door"], [
        DataLocation("Dragonfly Falls: Dark Gem near vultures", 44, _DEFAULT_RULE),
        DataLocation("Dragonfly Falls: Dragon Egg in vulture's nest", 45, _DEFAULT_RULE),
        DataLocation("Dragonfly Falls: Dark Gem before large pool", 46, _DEFAULT_RULE),
        DataLocation("Dragonfly Falls: Light Gem behind breakable wall in large pool", 47, _builder_all(Swim=1)),
        DataLocation("Dragonfly Falls: Dragon Egg from Sparx", 48, _DEFAULT_RULE),
        DataLocation("Dragonfly Falls: Light Gem from Sparx", 49, _DEFAULT_RULE),
        DataLocation("Dragonfly Falls: Dragon Egg behind breakable wall above wall kick", 50, _builder_all(Charge=1,**{"Wall Kick":1})),
        DataLocation("Dragonfly Falls: Light Gem in Piranha Pool", 51, _DEFAULT_RULE),
        DataLocation("Dragonfly Falls: Locked Chest in Piranha Pool", 52, _DEFAULT_RULE),
        DataLocation("Dragonfly Falls: Dragon Egg in vultures nest (Hunter)", 53, _DEFAULT_RULE),
        DataLocation("Dragonfly Falls: Complete Hunters trial", 54, _DEFAULT_RULE),
        DataLocation("Dragonfly Falls: Dark Gem at end of zone", 55, _DEFAULT_RULE),
        DataLocation("Dragonfly Falls: Light Gem glide from wall kick", 58, _builder_all(**{"Wall Kick":1}))
    ], access_rule=_builder_all(Glide=1)),

    # TODO: randomized light gem costs for doors
    # This region can technically be reached without glide (via charge jumping)
    DataRegion("Dragonfly Falls - 70 Light Gem Door", [], [
        DataLocation("Dragonfly Falls: Light Gem behind breakable wall beyond 70 Light Gem door", 56, _DEFAULT_RULE),
        DataLocation("Dragonfly Falls: Dragon Egg from thief beyond 70 Light Gem door", 57, _DEFAULT_RULE),
    ], access_rule=_builder_all(**{"Light Gem": 70, "Charge": 1, "Glide": 1})),

    DataRegion("Coastal Remains", ["Coastal Remains - Cloudy Domain Entrance", "Coastal Remains - After Otto", "Coastal Remains - 20 Light Gem Door", "Coastal Remains - After Cannon Dark Gem", "Coastal Remains - Ineptunes Lair"], [
        DataLocation("Coastal Remains: Dragon Egg from Turtle Mother", 63, _builder_all(Charge=1)),
        DataLocation("Coastal Remains: Light Gem from Turtle Mother", 64, _builder_all(Charge=1)),
        DataLocation("Coastal Remains: Dark Gem in cannon room", 65, _builder_all(Glide=1, **{"Double Jump": 1})),
        DataLocation("Coastal Remains: Light Gem at beach above water mill", 69, _builder_all(**{"Water Breath": 1, "Double Jump": 1})),
        DataLocation("Coastal Remains: Dragon Egg after Piranha pool", 78, _builder_all(**{"Double Jump": 1})),
        DataLocation("Coastal Remains: Locked Chest behind Moneybags", 234, _DEFAULT_RULE),
        DataLocation("Coastal Remains: Locked Chest hidden on beach", 235, _DEFAULT_RULE)
    ], access_rule=_DEFAULT_RULE),

    # Implied: Double Jump, Glide
    DataRegion("Coastal Remains - Cloudy Domain Entrance", ["Cloudy Domain"], [
        DataLocation("Coastal Remains: Light Gem after Windmills", 59, _builder_all(**{"Pole Spin": 1})),
        DataLocation("Coastal Remains: Light Gem beyond moving platform", 60, _builder_all(**{"Lightning Breath": 1})),
    ], access_rule=_builder_all(Glide=1, **{"Double Jump": 1})),

    # Implied: 20x Light Gem
    DataRegion("Coastal Remains - 20 Light Gem Door", [], [
        DataLocation("Coastal Remains: Dragon Egg from thief beyond 20 Light Gem door", 61, _builder_all(Charge=1)),
        DataLocation("Coastal Remains: Light Gem in 20 Light Gem door", 62, _DEFAULT_RULE)
    ], access_rule=_builder_all(**{"Light Gem": 20})),

    # Implied: Double Jump, Pole Spin, Glide
    DataRegion("Coastal Remains - After Cannon Dark Gem", [], [
        DataLocation("Coastal Remains: Dragon Egg in cannon room", 66, _DEFAULT_RULE),
        DataLocation("Coastal Remains: Dark Gem after Swinging Shells", 67, _builder_all(Charge=1)),
        DataLocation("Coastal Remains: Dragon Egg after moving platforms", 68, _DEFAULT_RULE)
    ], access_rule=_builder_all(**{"Pole Spin":1,"Double Jump":1}, Glide=1)),

    # Implied: Double Jump, Pole Spin
    DataRegion("Coastal Remains - After Otto", ["Sunken Ruins"], [
        DataLocation("Coastal Remains: Light Gem in Ottos pool", 70, _DEFAULT_RULE),
        DataLocation("Coastal Remains: Light Gem reward from Otto", 71, _DEFAULT_RULE),
        DataLocation("Coastal Remains: Dragon Egg from Blink", 72, _DEFAULT_RULE),
        DataLocation("Coastal Remains: Light Gem from Blink", 73, _DEFAULT_RULE),
        DataLocation("Coastal Remains: Dark Gem near Blink", 74, _DEFAULT_RULE),
        DataLocation("Coastal Remains: Dragon Egg after Crossbow Gnorcs", 75, _DEFAULT_RULE),
        DataLocation("Coastal Remains: Dark Gem before Sunken Ruins", 76, _DEFAULT_RULE),
        DataLocation("Coastal Remains: Light Gem before Sunken Ruins", 77, _DEFAULT_RULE),
    ], access_rule=_builder_all(**{"Pole Spin":1,"Double Jump":1})),

    # Implied: Charge, 20x Dark Gem
    DataRegion("Coastal Remains - Ineptunes Lair", [], [
        DataLocation("Coastal Remains: Water Breath from Ineptune", 79, _DEFAULT_RULE)
    ], access_rule=_builder_all(**{"Dark Gem": 20}, Charge=1)),

    # Implied: Double Jump, Glide
    DataRegion("Cloudy Domain", ["Cloudy Domain - After Elder Titan"], [
        DataLocation("Cloudy Domain: Locked Chest at entrance", 80, _DEFAULT_RULE),
        DataLocation("Cloudy Domain: Dark Gem after locked door", 81, _DEFAULT_RULE),
        DataLocation("Cloudy Domain: Light Gem before Elder Titan", 82, _DEFAULT_RULE),
    ], access_rule=_DEFAULT_RULE),

    # Implied: Double Jump, Glide, Charge
    DataRegion("Cloudy Domain - After Elder Titan", ["Cloudy Domain - Wing Shield"], [
        DataLocation("Cloudy Domain: Wing Shield from Elder Titan", 83, _DEFAULT_RULE),
        DataLocation("Cloudy Domain: Dragon Egg after Elder Titan", 84, _DEFAULT_RULE),
        DataLocation("Cloudy Domain: Locked Chest beyond Reinforced Door", 85, _builder_all(**{"Light Gem": 40})),
        DataLocation("Cloudy Domain: Locked Chest after Crossroads left", 87, _DEFAULT_RULE),
        DataLocation("Cloudy Domain: Light Gem after platforming at Crossroads left", 88, _DEFAULT_RULE)
    ], access_rule=_builder_all(Charge=1)),

    # Implied: Double Jump, Glide, Charge, Wing Shield
    DataRegion("Cloudy Domain - Wing Shield", [], [
        DataLocation("Cloudy Domain: Locked Chest in Wing Shield Tutorial", 236, _DEFAULT_RULE),
        DataLocation("Cloudy Domain: Light Gem after Wing Shield Tutorial", 86, _DEFAULT_RULE),
        DataLocation("Cloudy Domain: Light Gem after temporary platforms at Crossroads right", 89, _DEFAULT_RULE),
        DataLocation("Cloudy Domain: Dragon Egg on temporary platform after Crossroads right", 90, _DEFAULT_RULE),
        DataLocation("Cloudy Domain: Dragon Egg from thief after rotating platforms", 91, _DEFAULT_RULE),
        DataLocation("Cloudy Domain: Dark Gem after rotating platforms", 92, _DEFAULT_RULE),
        DataLocation("Cloudy Domain: Dragon Egg from Sgt. Byrd", 93, _DEFAULT_RULE),
        DataLocation("Cloudy Domain: Light Gem from Sgt. Byrd", 94, _DEFAULT_RULE),
        DataLocation("Cloudy Domain: Light Gem after Sgt. Byrd", 95, _builder_all(**{"Wall Kick": 1})),
        DataLocation("Cloudy Domain: Dark Gem after Sgt. Byrd", 96, _DEFAULT_RULE),
        DataLocation("Cloudy Domain: Dragon Egg in Ball Gadget", 97, _builder_all(**{"Light Gem": 8})),
        DataLocation("Cloudy Domain: Light Gem in Ball Gadget", 98, _builder_all(**{"Light Gem": 8})),
    ], access_rule=_builder_all(**{"Wing Shield":1})),

    # Implied: Double Jump, Pole Spin, Swim
    DataRegion("Sunken Ruins", ["Sunken Ruins - Invulnerability Gadget"], [
        DataLocation("Sunken Ruins: Locked Chest at entrance", 237, _DEFAULT_RULE),
        DataLocation("Sunken Ruins: Locked Chest behind Swim Exit", 99, _DEFAULT_RULE),
        DataLocation("Sunken Ruins: Dark Gem after Swim", 100, _DEFAULT_RULE),
        DataLocation("Sunken Ruins: Dragon Egg above Dark Gem", 101, _builder_all(Glide=1)),
        DataLocation("Sunken Ruins: Locked Chest above Dark Gem", 102, _builder_all(Glide=1)),
        DataLocation("Sunken Ruins: Locked Chest behind Lily", 103, _DEFAULT_RULE),
        DataLocation("Sunken Ruins: Light Gem after Acid Swim", 104, _builder_all(**{"Light Gem": 24})),
        DataLocation("Sunken Ruins: Dragon Egg from Sparx", 105, _DEFAULT_RULE),
        DataLocation("Sunken Ruins: Light Gem from Sparx", 106, _DEFAULT_RULE),
        DataLocation("Sunken Ruins: Dragon Egg above heated wall kick", 107, _builder_all(**{"Light Gem": 24, "Wall Kick": 1})),
        DataLocation("Sunken Ruins: Locked Chest near fish", 108, _DEFAULT_RULE),
        DataLocation("Sunken Ruins: Light Gem after fish", 109, _builder_all(Glide=1))
    ], access_rule=_builder_all(Swim=1)),

    # Implied: Double Jump, Pole Spin, Swim, Lightning Breath, 24x Light Gems, Glide
    DataRegion("Sunken Ruins - Invulnerability Gadget", [], [
        DataLocation("Sunken Ruins: Light Gem inside Acid Swim", 110, _DEFAULT_RULE),
        DataLocation("Sunken Ruins: Dark Gem after Acid Swim", 111, _DEFAULT_RULE),
        DataLocation("Sunken Ruins: Locked Chest after Dark Gem", 112, _builder_all(Glide=1)),
        DataLocation("Sunken Ruins: Dark Gem under Acid Pool", 113, _builder_all(Glide=1)),
        DataLocation("Sunken Ruins: Locked Chest near Acid Pool Dark Gem", 114, _DEFAULT_RULE),
        DataLocation("Sunken Ruins: Locked Chest after Acid Pool Dark Gem", 115, _builder_all(Glide=1))
    ], access_rule=_builder_all(**{"Lightning Breath": 1, "Light Gem": 24}, Glide=1)),

    DataRegion("Frostbite Village", ["Frostbite Village - After Phils Gate", "Frostbite Village - After Horn Dive Switch", "Frostbite Village - Reds Lair"], [
    ], access_rule=_DEFAULT_RULE),

    DataRegion("Frostbite Village - After Horn Dive Switch", ["Frostbite Village - Before Gloomy Glacier"], [
        DataLocation("Frostbite Village: Dark Gem under avalanche", 121, _DEFAULT_RULE),
        DataLocation("Frostbite Village: Dragon Egg from thief after spinning totem", 122, _builder_all(Charge=1)),
        DataLocation("Frostbite Village: Light Gem after spinning totem after thief", 123, _DEFAULT_RULE),
        DataLocation("Frostbite Village: Dragon Egg from Blink", 124, _DEFAULT_RULE),
        DataLocation("Frostbite Village: Light Gem from Blink", 125, _DEFAULT_RULE),
    ], access_rule=_builder_all(**{"Double Jump": 1})),

    DataRegion("Frostbite Village - Reds Lair", [], [
        DataLocation("Frostbite Village: Ice Breath from Red", 136, _DEFAULT_RULE)
        # a breath is required to kill the dogs
    ], access_rule=lambda world: lambda state: state.has_any(("Fire Breath", "Lightning Breath", "Charge"), world.player) and state.has("Dark Gem", world.player, 30)),

    # Implied: Double Jump, Lightning Breath
    DataRegion("Frostbite Village - After Phils Gate", [], [
        DataLocation("Frostbite Village: Light Gem after Phils Gate", 116, _builder_all(**{"Water Breath": 1})),
        DataLocation("Frostbite Village: Dragon Egg from Peggy", 117, _DEFAULT_RULE),
        DataLocation("Frostbite Village: Light Gem from Peggy", 118, _DEFAULT_RULE),
        DataLocation("Frostbite Village: Dark Gem near Peggy", 119, _DEFAULT_RULE),
        DataLocation("Frostbite Village: Dragon Egg after Dark Gem near Peggy", 120, _DEFAULT_RULE),
        DataLocation("Frostbite Village: Locked Chest by Dragon Egg", 238, _DEFAULT_RULE)
    ], access_rule=_builder_all(**{"Lightning Breath": 1})),

    # Implied: Double Jump, Glide
    DataRegion("Frostbite Village - Before Gloomy Glacier", ["Gloomy Glacier", "Frostbite Village - Wall Kick"], [
        DataLocation("Frostbite Village: Dragon Egg behind breakable wall", 130, _builder_all(Charge=1)),
        DataLocation("Frostbite Village: Return to Manny", 135, _DEFAULT_RULE)
    ], access_rule=_builder_all(Glide=1)),

    # Implied: Double Jump, Glide, Wall Kick
    DataRegion("Frostbite Village - Wall Kick", [], [
        DataLocation("Frostbite Village: Dark Gem in slippery room", 131, _DEFAULT_RULE),
        DataLocation("Frostbite Village: Light Gem in slippery room", 132, _DEFAULT_RULE)
    ], access_rule=_builder_all(**{"Wall Kick": 1})),

    # Implied: Double Jump, Glide
    DataRegion("Gloomy Glacier", ["Ice Citadel"], [
        DataLocation("Gloomy Glacier: Locked Chest in Bentleys Living Room", 239, _DEFAULT_RULE),
        DataLocation("Gloomy Glacier: Locked Chest in Bentleys Bedroom", 137, _DEFAULT_RULE),
        DataLocation("Gloomy Glacier: Reward from Bentley", 138, _DEFAULT_RULE),
        DataLocation("Gloomy Glacier: Light Gem in Ambush room", 139, _DEFAULT_RULE),
        DataLocation("Gloomy Glacier: Locked Chest after Ambush room", 140, _DEFAULT_RULE),
        DataLocation("Gloomy Glacier: Dragon Egg behind breakable wall in swinging rocks", 141, _DEFAULT_RULE),
        DataLocation("Gloomy Glacier: Light Gem behind Yeti behind breakable bones", 142, _DEFAULT_RULE),
        DataLocation("Gloomy Glacier: Dragon Egg under bone platform", 143, _DEFAULT_RULE),
        DataLocation("Gloomy Glacier: Light Gem behind Yeti in temporary platform room", 144, _DEFAULT_RULE),
        DataLocation("Gloomy Glacier: Dragon Egg after spinning bones", 145, _DEFAULT_RULE),
        DataLocation("Gloomy Glacier: Dragon Egg from Sparx", 146, _DEFAULT_RULE),
        DataLocation("Gloomy Glacier: Light Gem from Sparx", 147, _DEFAULT_RULE),
        # This one is a bit vague but i'm not sure how to word it better
        DataLocation("Gloomy Glacier: Light Gem after moving platform right of entrance", 148, _DEFAULT_RULE),
        DataLocation("Gloomy Glacier: Light Gem behind locked door above climbable wall", 149, _DEFAULT_RULE),
        DataLocation("Gloomy Glacier: Light Gem at end of zone", 150, _DEFAULT_RULE)
    ], access_rule=_DEFAULT_RULE),
    
    # Implied: Double Jump, Glide
    DataRegion("Ice Citadel", ["Ice Citadel - Inner"], [
        DataLocation("Ice Citadel: Locked Chest in entrance", 240, _DEFAULT_RULE),
        DataLocation("Ice Citadel: Reward for lighting 1 boiler", 151, _builder_all(**{"Fire Breath": 1})),
        DataLocation("Ice Citadel: Light Gem above moving platform", 152, _DEFAULT_RULE)
    ], access_rule=_DEFAULT_RULE),

    # Implied: Double Jump, Glide, Water Breath
    DataRegion("Ice Citadel - Inner", ["Ice Citadel - Above Elder Astor"], [
        DataLocation("Ice Citadel: Locked Chest behind breakable wall", 153, _builder_all(Charge=1))
    ], access_rule=_builder_all(**{"Water Breath": 1})),

    # the extra breaths + charge rule is required because the armoured gnorc in front of the door must be defeated before you can access elder astor's dark gem
    # Implied: Double Jump, Glide, Water Breath, Fire Breath OR Lightning Breath OR Ice Breath, Charge
    DataRegion("Ice Citadel - Above Elder Astor", ["Ice Citadel - After Elder Astor"], [
        DataLocation("Ice Citadel: Dark Gem above Elder Astor", 154, _DEFAULT_RULE),
        DataLocation("Ice Citadel: Wall Kick from Elder Astor", 155, _DEFAULT_RULE)
    ], access_rule=lambda world: lambda state: state.has_any(("Fire Breath", "Lightning Breath", "Ice Breath"), world.player) and state.has("Charge", world.player)),

    # Implied: Double Jump, Glide, Water Breath, Fire Breath OR Lightning Breath OR Ice Breath, Charge, Wall Kick
    DataRegion("Ice Citadel - After Elder Astor", ["Frostbite Village - Reinforced Door"], [
        DataLocation("Ice Citadel: Locked Chest after Elder Astor", 156, _DEFAULT_RULE),
        DataLocation("Ice Citadel: Dark Gem after sewer sprint", 157, _builder_all(**{"Light Gem": 40})),
        DataLocation("Ice Citadel: Dragon Egg after Dark Gem in sewer", 158, _builder_all(**{"Light Gem": 40})),
        DataLocation("Ice Citadel: Locked Chest in supercharge tunnel", 241, _DEFAULT_RULE),
        DataLocation("Ice Citadel: Locked Chest before reinforced wall", 242, _DEFAULT_RULE),
        DataLocation("Ice Citadel: Dragon Egg beind reinforced wall", 159, _builder_all(**{"Light Gem": 40})),
        DataLocation("Ice Citadel: Dragon Egg from Sgt. Byrd", 160, _DEFAULT_RULE),
        DataLocation("Ice Citadel: Light Gem from Sgt. Byrd", 161, _DEFAULT_RULE),
        DataLocation("Ice Citadel: Reward for lighting 3 boilers", 162, _builder_all(**{"Fire Breath": 1})),
        DataLocation("Ice Citadel: Locked Chest by Ice Princess", 243, _DEFAULT_RULE),
        DataLocation("Ice Citadel: Dark Gem after Ice Princess", 163, _DEFAULT_RULE),
        DataLocation("Ice Citadel: Dragon Egg after pole spin after Yetis", 164, _builder_all(**{"Pole Spin": 1})),
        DataLocation("Ice Citadel: Dark Gem after Yetis", 165, _builder_all(**{"Lightning Breath": 1, "Pole Spin": 1})),
        DataLocation("Ice Citadel: Dragon Egg beind cannon reinforced wall", 166, _DEFAULT_RULE),
        DataLocation("Ice Citadel: Light Gem beind cannon reinforced wall", 167, _DEFAULT_RULE),
        DataLocation("Ice Citadel: Reward for lighting 5 boilers", 168, _builder_all(**{"Fire Breath": 1})),
        DataLocation("Ice Citadel: Reward for lighting all boilers from Ice Princess", 169, _builder_all(**{"Fire Breath": 1})),
        DataLocation("Ice Citadel: Dark Gem above slippery slope", 170, _builder_all(**{"Light Gem": 40})),
        DataLocation("Ice Citadel: Dragon Egg from thief after Dark Gem", 171, _builder_all(**{"Light Gem": 40})),
    ], access_rule=_builder_all(**{"Wall Kick": 1})),

    # Implied: Double Jump, Glide, Water Breath, Fire Breath OR Lightning Breath OR Ice Breath, Charge, Wall Kick, 40x Light Gem
    DataRegion("Frostbite Village - Reinforced Door", ["Frostbite Village - 95 Light Gem Door"], [
        DataLocation("Frostbite Village: Light Gem through reinforced door to Frostbite Village", 172, _DEFAULT_RULE),
        DataLocation("Frostbite Village: Dark Gem after reinforced door", 126, _DEFAULT_RULE),
        DataLocation("Frostbite Village: Dark Gem after falling icicles", 127, _DEFAULT_RULE),
        DataLocation("Frostbite Village: Locked Chest in falling icicles room", 128, _DEFAULT_RULE),
        DataLocation("Frostbite Village: Light Gem after falling icicles", 129, _builder_all(**{"Pole Spin": 1})),
        DataLocation("Frostbite Village: Locked Chest under platform after falling icicles", 244, _DEFAULT_RULE)
    ], access_rule=_builder_all(**{"Light Gem": 40})),

    # Implied: Double Jump, Glide, Water Breath, Fire Breath OR Lightning Breath OR Ice Breath, Charge, Wall Kick, 95x Light Gem
    DataRegion("Frostbite Village - 95 Light Gem Door", [], [
        DataLocation("Frostbite Village: Locked Chest beyond 95 Light Gem Door", 133, _DEFAULT_RULE),
        DataLocation("Frostbite Village: Light Gem beyond 95 Light Gem Door", 134, _DEFAULT_RULE)
    ], access_rule=_builder_all(**{"Light Gem": 95})),

    DataRegion("Stormy Beach", ["Molten Mount"], [
        DataLocation("Stormy Beach: Locked Chest 1 in left cove by teleporter", 245, _DEFAULT_RULE),
        DataLocation("Stormy Beach: Locked Chest 2 in left cove by teleporter", 246, _DEFAULT_RULE),
        DataLocation("Stormy Beach: Light Gem in left cove by teleporter", 173, _builder_all(**{"Double Jump":1})),
        DataLocation("Stormy Beach: Dragon Egg from thief underneath Moneybags", 174, _builder_all(Charge=1)),
        DataLocation("Stormy Beach: Locked Chest by Wally", 247, _builder_all(**{"Double Jump":1})),
        DataLocation("Stormy Beach: Dragon Egg from Wally", 175, _builder_all(**{"Double Jump":1})),
        DataLocation("Stormy Beach: Light Gem from Wally", 176, _builder_all(**{"Double Jump":1})),
        DataLocation("Stormy Beach: Locked Chest after armored Gnorc", 248, _builder_all(**{"Double Jump":1})),
        DataLocation("Stormy Beach: Locked Chest guarded by crossbow Gnorcs", 249, _builder_all(Glide=1,**{"Wall Kick":1,"Double Jump":1})),
        DataLocation("Stormy Beach: Dark Gem at entrance to volcano", 177, _builder_all(**{"Double Jump":1}))
    ], access_rule=_DEFAULT_RULE),

    # Implied: Double Jump, Glide, Water Breath OR Ice Breath
    DataRegion("Molten Mount", ["Molten Mount - Pole Spin"], [
        DataLocation("Molten Mount: Dark Gem after Rock Monsters", 178, _DEFAULT_RULE),
        DataLocation("Molten Mount: Reward from Teena", 179, _builder_all(Charge=1)),
        DataLocation("Molten Mount: Dragon Egg across Imp platforms", 180, _DEFAULT_RULE),
        DataLocation("Molten Mount: Dragon Egg from Sgt. Byrd", 181, _DEFAULT_RULE),
        DataLocation("Molten Mount: Light Gem from Sgt. Byrd", 182, _DEFAULT_RULE),
        DataLocation("Molten Mount: Locked Chest next to Sgt. Byrd", 183, _DEFAULT_RULE),
        DataLocation("Molten Mount: Light Gem behind Imp", 184, _DEFAULT_RULE)
    ], access_rule=lambda world: lambda state: state.has_any(["Water Breath", "Ice Breath"], world.player) and state.has_all(["Double Jump", "Glide"], world.player)),

    # Implied: Double Jump, Glide, Water Breath OR Ice Breath, Pole Spin
    DataRegion("Molten Mount - Pole Spin", ["Magma Falls Top"], [
        DataLocation("Molten Mount: Light Gem after Imp ambush", 185, _DEFAULT_RULE),
        DataLocation("Molten Mount: Dark Gem before lava fall", 186, _DEFAULT_RULE),
        DataLocation("Molten Mount: Light Gem after platform challenge", 187, _builder_all(Charge=1,**{"Light Gem": 24})),
        DataLocation("Molten Mount: Locked Chest behind breakable wall", 188, _builder_all(Charge=1)),
        DataLocation("Molten Mount: Dragon Egg from thief", 189, _builder_all(Charge=1)),
        DataLocation("Molten Mount: Locked Chest in thief room", 250, _DEFAULT_RULE),
        DataLocation("Molten Mount: Locked Chest behind breakable wall near end of zone", 190, _builder_all(Charge=1)),
        DataLocation("Molten Mount: Dark Gem at end of zone", 191, _DEFAULT_RULE)
    ], access_rule=_builder_all(**{"Pole Spin": 1})),

    # Implied: Double Jump, Water Breath OR Ice Breath, Pole Spin, Wall Kick
    DataRegion("Magma Falls Top", ["Magma Falls - Ball Gadget"], [
        DataLocation("Magma Falls Top: Light Gem in wall kick room", 192, _DEFAULT_RULE),
        DataLocation("Magma Falls Top: Locked Chest behind Moneybags", 193, _builder_all(Charge=1)),
        DataLocation("Magma Falls Top: Locked Chest above Imps", 251, _DEFAULT_RULE)
    ], access_rule=_builder_all(**{"Wall Kick": 1})),

    # Implied: Double Jump, Water Breath OR Ice Breath, Pole Spin, Wall Kick, 8x Light Gems
    DataRegion("Magma Falls - Ball Gadget", ["Magma Falls Bottom"], [
        DataLocation("Magma Falls Top: Dragon Egg 1 in Ball Gadget", 194, _DEFAULT_RULE),
        DataLocation("Magma Falls Top: Light Gem 1 in Ball Gadget", 195, _DEFAULT_RULE),
        DataLocation("Magma Falls Top: Dragon Egg 2 in Ball Gadget", 196, _DEFAULT_RULE),
        DataLocation("Magma Falls Top: Light Gem 2 in Ball Gadget", 197, _DEFAULT_RULE)
    ], access_rule=_builder_all(**{"Light Gem": 8})),

    # Implied: Double Jump, Water Breath OR Ice Breath, Pole Spin, Wall Kick, 8x Light Gems
    DataRegion("Magma Falls Bottom", ["Dark Mine"], [
        DataLocation("Magma Falls Bottom: Dark Gem above wall kick", 198, _DEFAULT_RULE),
        DataLocation("Magma Falls Bottom: Locked Chest after Dark Gem", 199, _DEFAULT_RULE),
        DataLocation("Magma Falls Bottom: Light Gem after Imp platforming", 200, _DEFAULT_RULE),
        DataLocation("Magma Falls Bottom: Dragon Egg from Sparx", 202, _DEFAULT_RULE),
        DataLocation("Magma Falls Bottom: Light Gem from Sparx", 203, _DEFAULT_RULE),
        DataLocation("Magma Falls Bottom: Dragon Egg from thief behind breakable wall", 201, _builder_all(Charge=1))
    ], access_rule=_DEFAULT_RULE),

    # Implied: Double Jump, Water Breath OR Ice Breath, Pole Spin, Wall Kick, 8x Light Gems, Charge, Lightning Breath
    DataRegion("Dark Mine", ["Dark Mine - 45 Light Gem Door", "Dark Mine - Steam Vents"], [
        DataLocation("Dark Mine: Locked Chest at entrance", 252, _DEFAULT_RULE),
        DataLocation("Dark Mine: Locked Chest by bear traps", 206, _DEFAULT_RULE),
        DataLocation("Dark Mine: Locked Chest glide from Green Robo-Gnorc", 207, _DEFAULT_RULE),
        DataLocation("Dark Mine: Light Gem over wall after locked chest", 208, _DEFAULT_RULE),
        DataLocation("Dark Mine: Dark Gem in laser gun room", 209, _DEFAULT_RULE),
        DataLocation("Dark Mine: Dragon Egg from Blink", 210, _DEFAULT_RULE),
        DataLocation("Dark Mine: Light Gem from Blink", 211, _DEFAULT_RULE),
        DataLocation("Dark Mine: Dragon Egg below shield Robo-Gnorc", 212, _DEFAULT_RULE)
    ], access_rule=lambda world: lambda state: state.has_all(("Charge", "Lightning Breath"), world.player)),

    # Implied: Double Jump, Water Breath OR Ice Breath, Pole Spin, Wall Kick, 45x Light Gems, Charge, Lightning Breath, Swim
    DataRegion("Dark Mine - 45 Light Gem Door", [], [
        DataLocation("Dark Mine: Light Gem in Acid Pool beyond 45 Light Gem Door", 204, _DEFAULT_RULE),
        DataLocation("Dark Mine: Dragon Egg in Acid Pool beyond 45 Light Gem Door", 205, _DEFAULT_RULE)
    ], access_rule=_builder_all(**{"Light Gem": 45}, Swim=1)),

    # Implied: Double Jump, Water Breath, Pole Spin, Wall Kick, 8x Light Gems, Charge, Lightning Breath, Ice Breath,
    DataRegion("Dark Mine - Steam Vents", ["Red's Laboratory"], [
        DataLocation("Dark Mine: Light Gem in temporary platform room", 213, _DEFAULT_RULE),
        DataLocation("Dark Mine: Dragon Egg next to Moneybags", 214, _DEFAULT_RULE),
        DataLocation("Dark Mine: Light Gem on platform above wall kick", 215, _DEFAULT_RULE),
        DataLocation("Dark Mine: Dark Gem after pole spin", 216, _DEFAULT_RULE)
    ], access_rule=_builder_all(**{"Ice Breath": 1})),

    # Implied: Double Jump, Water Breath, Pole Spin, Wall Kick, 8x Light Gems, Charge, Lightning Breath, Ice Breath, Fire Breath
    DataRegion("Red's Laboratory", [], [
        DataLocation("Red's Laboratory: Locked Chest after pole spin", 253, _DEFAULT_RULE),
        DataLocation("Red's Laboratory: Locked Chest above 4 charge switches", 254, _DEFAULT_RULE),
        DataLocation("Red's Laboratory: Dragon Egg from thief in hub area", 217, _DEFAULT_RULE),
        DataLocation("Red's Laboratory: Light Gem after pole spin in SE section", 218, _DEFAULT_RULE),
        DataLocation("Red's Laboratory: Dark Gem in sealed chamber after laser parkour in SE section", 219, _DEFAULT_RULE),
        DataLocation("Red's Laboratory: Light Gem above boiler elevator in SE section", 220, _DEFAULT_RULE),
        DataLocation("Red's Laboratory: Dragon Egg behind lasers in SE section", 221, _DEFAULT_RULE),
        DataLocation("Red's Laboratory: Dragon Egg in piston room W section", 222, _DEFAULT_RULE),
        DataLocation("Red's Laboratory: Light Gem after laser parkour in W section", 223, _DEFAULT_RULE),
        DataLocation("Red's Laboratory: Dark Gem in sealed chamber in W section", 224, _DEFAULT_RULE),
        DataLocation("Red's Laboratory: Light Gem after pole spin by Dark Gem in W section", 225, _DEFAULT_RULE),
        DataLocation("Red's Laboratory: Light Gem after metal press", 226, _builder_all(**{"Light Gem": 24})),
        DataLocation("Red's Laboratory: Dark Gem guarded by Staff Robo-Gnorcs", 227, _DEFAULT_RULE)
    ], access_rule=_builder_all(**{"Fire Breath": 1}))
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
            r.connect(c, entrance, rule=REGIONS[con].access_rule(world))
    
    if world.options.misc_allow_immediate_realm_access:
        dv = world.get_region("Dragon Village")
        dv.connect(world.get_region("Coastal Remains"), "DragonVillage=>CoastalRemains")
        dv.connect(world.get_region("Frostbite Village"), "DragonVillage=>FrostbiteVillage")
        dv.connect(world.get_region("Stormy Beach"), "DragonVillage=>StormyBeach")
    else:
        world.get_region("Dragon Village - Gnasty Gnorcs Lair").connect(world.get_region("Coastal Remains"), "DragonVillage-GnastyGnorcsLair=>CoastalRemains")
        world.get_region("Coastal Remains - Ineptunes Lair").connect(world.get_region("Frostbite Village"), "CoastalRemains-IneptunesLair=>FrostbiteVillage")
        world.get_region("Frostbite Village - Reds Lair").connect(world.get_region("Stormy Beach"), "FrostbiteVillage-RedsLair=>StormyBeach")
