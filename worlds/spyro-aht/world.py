import functools
from collections.abc import Mapping
from typing import Any

from BaseClasses import MultiWorld
from worlds.AutoWorld import World

from . import items, locations, options as ahtoptions, regions, rules, web_world

class SpyroAHTWorld(World):
    """
    Spyro: A Hero's Tail is a 3D platformer and collect-a-thon released in 2004 for the Xbox, Playstation 2 and GameCube.
    """

    game = "Spyro: A Hero's Tail"

    web = web_world.SpyroAHTWebWorld()

    options_dataclass = ahtoptions.SpyroAHTOptions
    options: ahtoptions.SpyroAHTOptions # type: ignore

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "Dragon Village"

    item_name_groups = {
        "Breath": {"Fire Breath", "Ice Breath", "Water Breath", "Electric Breath"},
        "Keychains": set()  # TODO
    }

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

        self._boss_lairs = [10, 20, 30, 40]
        self._lg_doors = [70, 20, 95, 45]
    
    def generate_early(self) -> None:
        match self.options.randomize_boss_lair_doors.value:
            case 0: pass
            case 2: # shuffle
                self.random.shuffle(self._boss_lairs)
            case 1: # random
                self._boss_lairs = [self.random.randint(1, 40) for _ in range(4)]
        
        highest = functools.reduce(max, self._boss_lairs)
        self._boss_lairs.remove(highest)
        if self.options.misc_goal.value < 3:
            self._boss_lairs.insert(self.options.misc_goal.value, highest)
        else:
            self._boss_lairs.append(highest)
        
        lg_door_min = self.options.light_gem_door_cost_min.value
        lg_door_max = self.options.light_gem_door_cost_max.value

        if lg_door_min > lg_door_max:
            lg_door_min, lg_door_max = lg_door_max, lg_door_min

        match self.options.randomize_light_gem_door_costs.value:
            case 0: pass
            case 1:
                self._lg_doors = [self.random.randint(lg_door_min, lg_door_max) for _ in range(4)]
            case 2:
                self.random.shuffle(self._lg_doors)
        
        return super().generate_early()

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)
    
    def create_item(self, name: str) -> items.SpyroAHTItem:
        return items.create_item_with_correct_classification(self, name)
    
    def fill_slot_data(self) -> Mapping[str, Any]:
        min_shop_price = self.options.shop_prices_min.value
        max_shop_price = self.options.shop_prices_max.value
        if min_shop_price > max_shop_price:
            min_shop_price, max_shop_price = max_shop_price, min_shop_price

        return {
            "misc_goal": self.options.misc_goal.value,
            "misc_skip_cutscenes": self.options.misc_skip_cutscenes.value,
            "misc_allow_immediate_realm_access": self.options.misc_allow_immediate_realm_access.value,
            "misc_hint_minigame_rewards": self.options.misc_hint_minigame_rewards.value,

            "randomize_shop_items": self.options.randomize_shop_items.value,
            "randomized_shop_prices": [self.random.randrange(min_shop_price, max_shop_price) for _ in range(0 if not self.options.randomize_shop_items.value else 57)],

            "randomize_boss_lair_doors": self.options.randomize_boss_lair_doors.value,
            "boss_lair_costs": self._boss_lairs,

            "randomize_light_gem_door_costs": self.options.randomize_light_gem_door_costs.value,
            "light_gem_door_costs": self._lg_doors,

            "death_link": self.options.death_link.value
        }
