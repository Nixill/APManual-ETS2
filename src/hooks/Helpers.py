from typing import Optional, Any, Union
from BaseClasses import MultiWorld
from ..nixcode.DataClasses import Region

# Copied from ..Helpers to avoid circuler import
def get_option_value(multiworld: MultiWorld, player: int, name: str) -> Union[int, dict]:
    option = getattr(multiworld.worlds[player].options, name, None)
    if option is None:
        return 0

    return option.value

def is_dlc_enabled(dlc_list: list[str], multiworld: MultiWorld, player: int) -> bool:
    if 'Base Game' in dlc_list: return True
    return bool(get_option_value(multiworld, player, 'dlcs_available').intersect(dlc_list))

def is_region_enabled(region_list: list[Region], multiworld: MultiWorld, player: int) -> bool:
    states: set[str] = get_option_value(multiworld, player, 'states_available')
    dlcs: set[str] = get_option_value(multiworld, player, 'dlcs_available')

    for r in region_list:
        if r.dlc in dlcs and r.state in states: return True

    return False

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the category, False to disable it, or None to use the default behavior
def before_is_category_enabled(multiworld: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    # Pull category from existing data
    from ..Data import category_table
    category: dict = category_table[category_name]
    if not 'extra_data' in category: return None
    extra_data: dict = category["extra_data"]

    # No required DLCs are enabled: Disable category
    if 'dlc_list' in extra_data and not is_dlc_enabled(extra_data["dlc_list"], multiworld, player): return False

    tp = extra_data['type']
    if tp == 'state_checks':
        if extra_data['which'] not in get_option_value(multiworld, player, 'states_available'): return False

    elif tp == 'dlc':
        if extra_data['which'] not in get_option_value(multiworld, player, 'dlcs_available'): return False

    elif tp == 'type_categories' and extra_data['which'] == 'skill':
        if not get_option_value(multiworld, player, 'skill_items_on_levels') and not get_option_value(multiworld, player, 'skill_items_scattered'): return False

    elif tp == 'victory':
        goal_option = multiworld.worlds[player].options.goal
        victory_condition = goal_option.value
        if victory_condition != goal_option.all_delivery_tokens_collected and extra_data['which'] == 'delivery_tokens': return False
        if victory_condition != goal_option.all_secret_deliveries_completed and extra_data['which'] == 'secret_delivery': return False

    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the item, False to disable it, or None to use the default behavior
def before_is_item_enabled(multiworld: MultiWorld, player: int, item:  dict[str, Any]) -> Optional[bool]:
    if not 'extra_data' in item: return None
    extra_data: dict[str, Any] = item["extra_data"]
    tp = extra_data['type']

    if tp == 'secret_delivery_instructions':
        if get_option_value(multiworld, player, 'secret_deliveries_available') < extra_data['secret_delivery_number']: return False

    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the location, False to disable it, or None to use the default behavior
def before_is_location_enabled(multiworld: MultiWorld, player: int, location:  dict[str, Any]) -> Optional[bool]:
    if not 'extra_data' in location: return None
    extra_data: dict[str, Any] = location["extra_data"]

    tp = extra_data['type']

    if tp == 'company':
        if not is_region_enabled(extra_data['region_list'], multiworld, player): return False
    elif tp == 'player_level_external':
        if get_option_value(multiworld, player, 'player_level_checks') < extra_data['player_level']: return False
    elif tp == 'player_level_skill':
        if get_option_value(multiworld, player, 'skill_items_on_levels'):
            if get_option_value(multiworld, player, 'skill_items_scattered'):
                if get_option_value(multiworld, player, 'player_level_checks') < extra_data['player_level']: return False
            else:
                return None
        else:
            return False
    elif tp == 'player_level_internal':
        if get_option_value(multiworld, player, 'skill_items_on_levels'):
            if get_option_value(multiworld, player, 'skill_items_scattered'):
                if get_option_value(multiworld, player, 'player_level_checks') < extra_data['player_level']: return False
            else:
                return None
        else:
            if get_option_value(multiworld, player, 'player_level_checks') < extra_data['player_level']: return False

    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the event, False to disable it, or None to use the default behavior
def before_is_event_enabled(multiworld: MultiWorld, player: int, event:  dict[str, Any]) -> Optional[bool]:
    return None
