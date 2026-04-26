import math
from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import clamp, get_items_with_value
from BaseClasses import MultiWorld, CollectionState
from ..nixcode.CsvData import region_list

import re

def playerLevelRegionsCheck(world: World, state: CollectionState, n: int):
    """
    The region accessibility requirement for a player level.

    Is based on both the number of enabled level checks and the factor.
    """
    if n <= 1: return "|@Regions Reachable:0|"

    allow_rule = world.options.enable_citysanity \
        or world.options.enable_photosanity \
        or world.options.enable_viewpointsanity

    if not allow_rule: return "|@Regions Reachable:0|"

    enabled_dlcs = world.options.dlcs_available.value
    enabled_regions = {r for r in region_list if r.dlc in enabled_dlcs}
    region_count = len(enabled_regions)

    player_level_max = world.options.player_level_checks.value
    lock_factor = world.options.player_level_logical_lock_factor.value / 100

    if region_count == 1 or player_level_max == 1: return "|@Regions Reachable:0|"
    if lock_factor == 0: return "|@Regions Reachable:0|"

    if n > player_level_max: n = player_level_max

    n -= 1
    player_level_max -= 1
    region_count -= 1

    region_need = math.ceil(region_count * (n / player_level_max) * lock_factor) + 1

    return f"|@Regions Reachable:{region_need}|"

# Sometimes you have a requirement that is just too messy or repetitive to write out with boolean logic.
# Define a function here, and you can use it in a requires string with {function_name()}.
def overfishedAnywhere(world: World, state: CollectionState, player: int):
    """Has the player collected all fish from any fishing log?"""
    for cat, items in world.item_name_groups:
        if cat.endswith("Fishing Log") and state.has_all(items, player):
            return True
    return False

# You can also pass an argument to your function, like {function_name(15)}
# Note that all arguments are strings, so you'll need to convert them to ints if you want to do math.
def anyClassLevel(state: CollectionState, player: int, level: str):
    """Has the player reached the given level in any class?"""
    for item in ["Figher Level", "Black Belt Level", "Thief Level", "Red Mage Level", "White Mage Level", "Black Mage Level"]:
        if state.count(item, player) >= int(level):
            return True
    return False

# You can also return a string from your function, and it will be evaluated as a requires string.
def requiresMelee():
    """Returns a requires string that checks if the player has unlocked the tank."""
    return "|Figher Level:15| or |Black Belt Level:15| or |Thief Level:15|"
