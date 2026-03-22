from dataclasses import dataclass

from Options import PerGameCommonOptions, Toggle, Choice, Range


class RandomizeSgtByrdMinigames(Toggle):
    """Toggle randomizing Sgt. Byrds mini game rewards."""
    display_name = "Randomize Sgt. Byrd Mini Games"
    default = 1


class RandomizeBlinkMinigames(Toggle):
    """Toggle randomizing Blinks mini game rewards."""
    display_name = "Randomize Blink Mini Games"
    default = 0


class RandomizeTurretMinigames(Toggle):
    """Toggle randomizing Turret mini game rewards."""
    display_name = "Randomize Turret Mini Games"
    default = 1


class RandomizeSparxMinigames(Toggle):
    """Toggle randomizing Sparxs mini game rewards."""
    display_name = "Randomize Sparx Mini Games"
    default = 1


class MiscHintMinigameRewards(Toggle):
    """When talking to a mini game npc, hint out their rewards."""
    display_name = "Hint Mini Game Rewards"
    default = 1


class MiscHintBossRewards(Toggle):
    """Hint out the item for beating a boss."""
    display_name = "Hint Boss Rewards"
    default = 0


class RandomizeBreath(Choice):
    """Determines which starting elemental breath you have.
    
    default: Fire breath.
    random: Start with a random breath.
    none: Start with no breath. Adds a starting check.
    """
    display_name = "Starting Breath"
    option_default = 0
    option_randomized = 1
    option_none = 2
    default = 0


class RandomizeSwim(Toggle):
    """Toggle randomizing Spyro's ability to Swim."""
    display_name = "Randomize Swim"
    default = 0


class RandomizeGlide(Toggle):
    """Toggle randomizing Spyro's ability to Glide."""
    display_name = "Randomize Glide"
    default = 0


class RandomizeCharge(Toggle):
    """Toggle randomizing Spyro's ability to Charge."""
    display_name = "Randomize Charge"
    default = 0


class RandomizeShopItems(Toggle):
    """Randomize Moneybags shop items. """
    display_name = "Randomize Shop Items"
    default = 0


class RandomizeShopPrices(Choice):
    """Sets Moneybags shop prices.
    NOTE: ``default`` currently does nothing.

    default: No changes to price. If ``Randomize Shop Items`` is enabled, this setting will automatically change to ``random``.
    random: Randomizes the price, defined by the range in **Minimum Shop Price** and **Maximum Shop Price**.
    random_low: Randomizes the price, with a bias towards a lower price.
    random_high: Randomizes the price, with a bias towards a higher price.
    """

    display_name = "Shop Prices"
    rich_text_doc = True
    option_default = 0
    option_randomized = 1
    option_randomized_low = 2
    option_randomized_high = 3
    default = 0


class ShopPricesMin(Range):
    """The minimum price for items in the shop."""
    display_name = "Minimum Shop Price"
    range_start = 1
    range_end = 10000
    default = 500


class ShopPricesMax(Range):
    """The maximum price for items in the shop."""
    display_name = "Maximum Shop Price"
    range_start = 1
    range_end = 10000
    default = 5000


class RandomizeBossLairDoorCosts(Choice):
    """Sets the Dark Gem requirement of the Boss Lairs.
    Note: The door to your goal boss will always be the most expensive of the 4.

    default: No changes to cost.
    randomized: Randomizes the cost, between 1 and 40.
    shuffle: Shuffles the existing costs (10, 20, 30, 40)
    """
    display_name = "Randomize Boss Lair Requirements"
    option_default = 0
    option_randomized = 1
    option_shuffle = 2
    default = 0


class BossLairDoorCostMin(Range):
    """Sets the minimum cost for the boss lairs."""
    display_name = "Boss Lair Door Cost Minimum"
    range_start = 1
    range_end = 40
    default = 1


class BossLairDoorCostMax(Range):
    """Sets the maximum cost for the boss lairs."""
    display_name = "Boss Lair Door Cost Maximum"
    range_start = 1
    range_end = 40
    default = 40


class RandomizeLightGemDoorCosts(Choice):
    """Sets the cost of light gem doors.
    
    default: No changes to cost.
    randomized: Randomizes the cost, defined by the range in **Minimum Light Gem Door Cost** and **Maximum Light Gem Door Cost**.
    shuffle: Shuffles the existing prices (20, 45, 70 and 95)."""
    display_name = "Randomize Light Gem Door Cost"
    option_default = 0
    option_randomized = 1
    option_shuffle = 2
    default = 0


class LightGemDoorCostMin(Range):
    """Sets the minimum cost for light gem doors."""
    display_name = "Minimum Light Gem Door Cost"
    range_start = 1
    range_end = 100
    default = 1


class LightGemDoorCostMax(Range):
    """Sets the maximum cost for light gem doors."""
    display_name = "Maximum Light Gem Door Cost"
    range_start = 1
    range_end = 100
    default = 50


class MiscGoal(Choice):
    """Set the goal condition."""
    display_name = "Goal"
    option_gnorc = 0
    option_ineptune = 1
    option_red = 2
    option_mechared = 3
    option_all = 4
    default = 3


class MiscSkipCutscenes(Toggle):
    """Enable a patch that skips realm intro cutscenes. USE WITH CAUTION, maybe have glitchy side-effects."""
    display_name = "Auto Skip Cutscenes"
    default = 0


class MiscAllowImmediateRealmAccess(Toggle):
    """
    Enable a patch to access all realms at any time, instead of having to beat the previous realms boss first.
    IT IS RECOMMENDED TO KEEP THIS ENABLED, disabling may cause a generation failure.
    """
    display_name = "Allow Immediate Realm Access"
    default = 1


class MiscSkipElevators(Toggle):
    """Enable a patch to skip the long elevator waits to Cloudy Domain, Sunken Ruins and Magma Falls"""
    display_name = "Skip Elevators"
    default = 1


class MiscDeathLink(Choice):
    """Enable DeathLinking.

    disabled: Disabled.
    Shielded: The Butterfly Jar will protect you from a DeathLink, if you have it.
    Enabled: Enabled.
    """
    display_name = "DeathLink"
    option_disabled = 0
    option_shielded = 1
    option_enabled = 2
    default = 0


@dataclass
class SpyroAHTOptions(PerGameCommonOptions):
    randomize_sgt_byrd_minigames: RandomizeSgtByrdMinigames
    randomize_blink_minigames: RandomizeBlinkMinigames
    randomize_turret_minigames: RandomizeTurretMinigames
    randomize_sparx_minigames: RandomizeSparxMinigames

    randomize_breath: RandomizeBreath
    randomize_swim: RandomizeSwim
    randomize_glide: RandomizeGlide
    randomize_charge: RandomizeCharge

    randomize_shop_items: RandomizeShopItems
    randomize_shop_prices: RandomizeShopPrices
    shop_prices_min: ShopPricesMin
    shop_prices_max: ShopPricesMax

    randomize_light_gem_door_costs: RandomizeLightGemDoorCosts
    light_gem_door_cost_min: LightGemDoorCostMin
    light_gem_door_cost_max: LightGemDoorCostMax

    randomize_boss_lair_doors: RandomizeBossLairDoorCosts
    boss_lair_door_cost_min: BossLairDoorCostMin
    boss_lair_door_cost_max: BossLairDoorCostMax

    misc_goal: MiscGoal
    misc_hint_minigame_rewards: MiscHintMinigameRewards
    misc_hint_boss_rewards: MiscHintBossRewards
    misc_skip_cutscenes: MiscSkipCutscenes
    misc_allow_immediate_realm_access: MiscAllowImmediateRealmAccess
    misc_skip_elevators: MiscSkipElevators

    death_link: MiscDeathLink

