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
    if dlc_list is False or 'Base Game' in dlc_list: return True
    return bool(get_option_value(multiworld, player, 'dlcs_available').intersection(dlc_list))

def is_region_enabled(region_list: list[Region], multiworld: MultiWorld, player: int) -> bool:
    states: set[str] = get_option_value(multiworld, player, 'states_available')
    dlcs: set[str] = get_option_value(multiworld, player, 'dlcs_available')

    for r in region_list:
        if r.dlc in dlcs and r.state in states: return True

    return False

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the category, False to disable it, or None to use the default behavior
def before_is_category_enabled(multiworld: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    from ..nixcode.Categories import check_for_category
    return check_for_category(multiworld, player, category_name)

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the item, False to disable it, or None to use the default behavior
def before_is_item_enabled(multiworld: MultiWorld, player: int, item:  dict[str, Any]) -> Optional[bool]:
    from ..nixcode.Items import check_for_item
    return check_for_item(multiworld, player, item)

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the location, False to disable it, or None to use the default behavior
def before_is_location_enabled(multiworld: MultiWorld, player: int, location:  dict[str, Any]) -> Optional[bool]:
    from ..nixcode.Locations import check_for_location
    return check_for_location(multiworld, player, location)

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the event, False to disable it, or None to use the default behavior
def before_is_event_enabled(multiworld: MultiWorld, player: int, event:  dict[str, Any]) -> Optional[bool]:
    return None
