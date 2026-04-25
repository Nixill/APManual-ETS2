from typing import Any, Optional

from BaseClasses import MultiWorld
from .DataClasses import Region
from ..hooks.Helpers import get_option_value, is_region_enabled

def check_for_location(multiworld: MultiWorld, player: int, location:  dict[str, Any]) -> Optional[bool]:
    if not 'extra_data' in location: return None
    extra_data: dict[str, Any] = location["extra_data"]

    tp = extra_data['type']

    if tp == 'company':
        if not is_region_enabled([Region(d['state'], d['dlc']) for d in extra_data['region_list']], multiworld, player): return False
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
    elif tp == 'secret_delivery_location':
        if get_option_value(multiworld, player, 'secret_deliveries_available') < extra_data['secret_delivery_number']: return False
        else: return None

    return None
