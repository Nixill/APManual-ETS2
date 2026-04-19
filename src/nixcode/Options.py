# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from typing import Any
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState, Item

from .CsvData import dlc_connections
from ..Helpers import is_option_enabled, get_option_value

def validate_options_early(world: World):
    """
    Verifies integrity of game options, applying the following fixes if necessary:

    - If enabled DLCs are not all connected and the Quick Travel Ticket is disabled, enable it.
    - Ensure required counts don't exceed available counts.
    """
    options = world.options

    if not options.quick_travel_item and not are_dlcs_connected(options.as_dict(toggles_as_bools=True)):
        options.quick_travel_item.value = 'in_starting_inventory'

    if options.delivery_tokens_required > options.delivery_tokens_available:
        options.delivery_tokens_required.value = options.delivery_tokens_available.value

    if options.secret_deliveries_required > options.secret_deliveries_available:
        options.secret_deliveries_required.value = options.secret_deliveries_available.value

def are_dlcs_connected(options: dict[str, Any]) -> bool:
    """
    Checks whether all enabled DLCs are connected to each other and to the base game.
    """
    unconnected: set[str] = get_enabled_dlcs(options)
    unprocessed: set[str] = {'base_game'}
    # If I change base game to optional:
    # unprocessed: set[str] = {unconnected.pop}
    processed: set[str] = set()

    while unconnected and unprocessed:
        this = unprocessed.pop()
        new_connections = set(dlc_connections[this]) & unconnected
        unconnected -= new_connections
        unprocessed |= new_connections
        processed.add(this)

    return not unconnected

def get_enabled_dlcs(options: dict[str, Any]) -> set[str]:
    """
    Returns the set of all enabled DLCs.
    """
    prefix = 'enable_dlc_'
    return {k.remove_prefix(prefix) for k,v in options.as_dict.items() if k.startswith(prefix) and v}
