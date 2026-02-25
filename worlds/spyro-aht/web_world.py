from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

class SpyroAHTWebWorld(WebWorld):
    game = "Spyro: A Hero's Tail"
    theme = "grassFlowers"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Spyro: A Hero's Tail for Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["MayaXTG"]
    )

    tutorials = [setup_en]