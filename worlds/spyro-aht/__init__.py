from multiprocessing import Process

from .world import SpyroAHTWorld as SpyroAHTWorld

from worlds.LauncherComponents import Component, components

def run_client():
    from .client import main
    Process(target=main,name="SpyroAHTClient").start()


components.append(Component("Spyro AHT Client", func=run_client))