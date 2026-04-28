from typing import Optional

from .Func import nixprint

from ..hooks.Helpers import get_option_value, is_dlc_enabled
from .Options import get_available_states
from BaseClasses import MultiWorld

def check_for_category(multiworld: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    # Pull category from existing data
    from ..Data import category_table
    category: dict = category_table[category_name]
    if not 'extra_data' in category: return None
    extra_data: dict = category["extra_data"]

    # No required DLCs are enabled: Disable category
    if 'dlc_list' in extra_data and not is_dlc_enabled(extra_data["dlc_list"], multiworld, player): return False

    tp = extra_data['type']

    if tp == 'state':
        # nixprint(f'Checking for State eligibility for category {category_name}:')
        if extra_data['which'] not in get_available_states(get_option_value(multiworld, player, 'dlcs_available')):
            # nixprint('State not available, returning false.')
            return False
        # else:
        #     nixprint('State available, returning true.')

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
            # nixprint(f'Delivery tokens (category {category_name}):')
            if victory_condition != getattr(goal_option, 'option_All Delivery Tokens Collected'):
                # nixprint('Removing, not goal.')
                return False
            # else:
            #     nixprint('Keeping, goal.')
        if extra_data['which'] == 'secret_delivery':
            # nixprint(f'Secret deliveries (category {category_name}):')
            if victory_condition != getattr(goal_option, 'option_All Secret Deliveries Completed'):
                # nixprint('Removing, not goal.')
                return False
            # else:
            #     nixprint('Keeping, goal.')

    return None
