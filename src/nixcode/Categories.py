from typing import Optional

from .Func import dbgprint

from ..hooks.Helpers import get_option_value, is_dlc_enabled
from .Options import get_available_states
from BaseClasses import MultiWorld

printed_multiworld_options = False

def check_for_category(multiworld: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    global printed_multiworld_options
    if not printed_multiworld_options:
        dbgprint(lambda : f'Options as of multiworld: {multiworld.worlds[player].options}')
        printed_multiworld_options = True

    # Pull category from existing data
    from ..Data import category_table
    category: dict = category_table[category_name]
    if not 'extra_data' in category: return None
    extra_data: dict = category["extra_data"]

    # No required DLCs are enabled: Disable category
    if 'dlc_list' in extra_data and not is_dlc_enabled(extra_data["dlc_list"], multiworld, player): return False

    tp = extra_data['type']

    if tp == 'state':
        dbgprint(lambda : f'Checking for State eligibility for category {category_name}:')
        dlcs = get_option_value(multiworld, player, 'dlcs_available')
        dbgprint(lambda : f'DLCs available: {dlcs}')
        if extra_data['which'] not in get_available_states(dlcs):
            dbgprint(lambda : 'State not available, returning false.')
            return False
        else:
            dbgprint(lambda : 'State available, returning true.')

    elif tp == 'state_checks':
        if extra_data['which'] not in get_option_value(multiworld, player, 'states_available'): return False

    elif tp == 'dlc':
        if extra_data['which'] not in get_option_value(multiworld, player, 'dlcs_available'): return False

    # Moving this to "grant skills automatically"
    # elif tp == 'type_categories' and extra_data['which'] == 'skill':
    #     if not get_option_value(multiworld, player, 'skill_items_on_levels') and not get_option_value(multiworld, player, 'skill_items_scattered'): return False

    elif tp == 'victory':
        goal_option = multiworld.worlds[player].options.goal
        victory_condition = goal_option.value
        if extra_data['which'] == 'delivery_tokens':
            # dbgprint(lambda : f'Delivery tokens (category {category_name}):')
            if victory_condition != getattr(goal_option, 'option_All Delivery Tokens Collected'):
                # dbgprint(lambda : 'Removing, not goal.')
                return False
            # else:
            #     dbgprint(lambda : 'Keeping, goal.')
        if extra_data['which'] == 'secret_delivery':
            # dbgprint(lambda : f'Secret deliveries (category {category_name}):')
            if victory_condition != getattr(goal_option, 'option_All Secret Deliveries Completed'):
                # dbgprint(lambda : 'Removing, not goal.')
                return False
            # else:
            #     dbgprint(lambda : 'Keeping, goal.')

    return None
