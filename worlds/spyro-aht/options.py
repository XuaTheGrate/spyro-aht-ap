from dataclasses import dataclass

from Options import PerGameCommonOptions, Toggle, Choice, Range


class RandomizeBreath(Choice):
    """Determines which starting elemental breath you have.
    
    default: Fire breath.
    random: Start with a random breath.
    none: Start with no breath. Adds a starting check.
    """
    display_name = "Starting Breath"
    option_default = 0
    option_random = 1
    option_none = 2
    default = 0


class RandomizeSwim(Toggle):
    """Toggle randomizing Spyro's ability to Swim."""
    display_name = "Randomize Swim"


class RandomizeGlide(Toggle):
    """Toggle randomizing Spyro's ability to Glide."""
    display_name = "Randomize Glide"


class RandomizeCharge(Toggle):
    """Toggle randomizing Spyro's ability to Charge."""
    display_name = "Randomize Charge"


class RandomizeShopPrices(Choice):
    """Sets Moneybags shop prices.
    
    default: No changes to price.
    random: Randomizes the price, defined by the range in **Minimum Shop Price** and **Maximum Shop Price**.
    random_low: Randomizes the price, with a bias towards a lower price.
    random_high: Randomizes the price, with a bias towards a higher price.
    """

    display_name = "Shop Prices"
    rich_text_doc = True
    option_default = 0
    option_random = 1
    option_random_low = 2
    option_random_high = 3
    default = 0


class ShopPricesMin(Range):
    """The minimum price for items in the shop."""
    display_name = "Minimum Shop Price"
    range_start = 1
    range_end = 10000
    default = 1


class ShopPricesMax(Range):
    """The maximum price for items in the shop."""
    display_name = "Maximum Shop Price"
    range_start = 1
    range_end = 10000
    default = 500


class RandomizeLightGemDoorCosts(Choice):
    """Sets the cost of light gem doors.
    
    default: No changes to cost.
    random: Randomizes the pricostce, defined by the range in **Minimum Light Gem Door Cost** and **Maximum Light Gem Door Cost**.
    shuffle: Shuffles the existing prices (20, 45, 70 and 95).
    random_low: Randomizes the cost, with a bias towards a lower cost.
    random_high: Randomizes the cost, with a bias towards a higher cost."""
    display_name = "Light Gem Door Cost"
    option_default = 0
    option_random = 1
    option_shuffle = 2
    option_random_low = 3
    option_random_high = 4
    default = 0


class LightGemDoorCostMin(Range):
    """Sets the minimum cost for light gem doors."""
    display_name = "Minimum Light Gem Door Cost"
    range_start = 1
    range_end = 100
    default = 1


class LightGemDoorCostMax(Range):
    """Sets the maximum cost for light gem doors"""
    display_name = "Maximum Light Gem Door Cost"
    range_start = 1
    range_end = 100
    default = 50


@dataclass
class SpyroAHTOptions(PerGameCommonOptions):
    randomize_breath: RandomizeBreath
    randomize_swim: RandomizeSwim
    randomize_glide: RandomizeGlide
    randomize_charge: RandomizeCharge
    randomize_shop_prices: RandomizeShopPrices
    shop_prices_min: ShopPricesMin
    shop_prices_max: ShopPricesMax
    light_gem_door_costs: RandomizeLightGemDoorCosts
    light_gem_door_cost_min: LightGemDoorCostMin
    light_gem_door_cost_max: LightGemDoorCostMax

