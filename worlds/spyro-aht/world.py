from collections.abc import Mapping
from typing import Any

from worlds.AutoWorld import World

from . import items, locations, options as ahtoptions, regions, rules, web_world

class SpyroAHTWorld(World):
    """
    Spyro: A Hero's Tail is a 3D platformer and collect-a-thon released in 2004 for the Playstation 2.
    """

    game = "Spyro: A Hero's Tail"

    web = web_world.SpyroAHTWebWorld()

    options_dataclass = ahtoptions.SpyroAHTOptions
    options: ahtoptions.SpyroAHTOptions # type: ignore

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "Dragon Village"

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)
        pass

    def create_items(self) -> None:
        items.create_all_items(self)
    
    def create_item(self, name: str) -> items.SpyroAHTItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.FILLER_ITEM_NAME
    
    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict("example_toggle")
