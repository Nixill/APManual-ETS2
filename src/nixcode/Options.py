# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from typing import Any
from src.nixcode.Func import snake_case
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState, Item

from .CsvData import dlc_connections, dlc_aliases_dict, dlc_states_dict
from .OptionDefs import QuickTravelTicketItem, StartingLocation
from ..Helpers import is_option_enabled, get_option_value

def validate_options_early(world: World):
    """
    Verifies integrity of game options, applying the following fixes if necessary:

    - If enabled DLCs are not all connected and the Quick Travel Ticket is disabled, enable it.
    - Ensure required counts don't exceed available counts.
    - Validates the starting state, re-choosing if necessary.
    - Ensures that the starting state has checks that exist.
    - Ensures that at least one player level is enabled if the goal is player level checks.
    - Ensures that at least one check type is enabled.
    """
    options = world.options

    options.dlcs_available.value = chosen_dlcs = get_enabled_dlcs(options.dlcs_available.value)
    available_states = get_available_states(chosen_dlcs)

    # If enabled DLCs are not all connected and the Quick Travel Ticket is disabled, enable it.
    if not options.quick_travel_ticket_item and not are_dlcs_connected(chosen_dlcs):
        options.quick_travel_ticket_item.value = QuickTravelTicketItem

    # Ensure required counts don't exceed available counts.
    if options.delivery_tokens_required > options.delivery_tokens_available:
        options.delivery_tokens_required.value = options.delivery_tokens_available.value

    if options.secret_deliveries_required > options.secret_deliveries_available:
        options.secret_deliveries_required.value = options.secret_deliveries_available.value

    # Validates the starting state, re-choosing if necessary.
    start_array = [state for state in available_states if snake_case(state) == starting_location.removeprefix('option_')]
    if start_array:
        starting_location = start_array.pop()
    if options.starting_location.current_key not in [snake_case(state) for state in available_states]:
        starting_location = world.random.choice(available_states)
        options.starting_location.value = getattr(StartingLocation, f'option_{snake_case(new_starting_location)}')

    # Ensures that the starting state has checks that exist.
    options.states_available.value.add(starting_location)

    # Ensures that at least one check type is enabled
    if not options.enable_city_checks and \
        not options.enable_company_checks and \
        not options.enable_photosanity and \
        not options.enable_viewpointsanity and \
        not options.player_level_checks:
            options.enable_city_checks.value = 1

def are_dlcs_connected(dlcs: set[str]) -> bool:
    """
    Checks whether all enabled DLCs are connected to each other and to the base game.
    """
    unconnected: set[str] = dlcs
    unprocessed: set[str] = {'Base Game'}
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

def get_enabled_dlcs(dlcs_in: set[str]) -> set[str]:
    """
    Returns the set of all enabled DLCs, with aliases parsed.
    """
    dlcs_out = set[str]()
    for dlc_in in dlcs_in:
        dlc_in = dlc_in.lower()
        dlc_out = dlc_aliases_dict[dlc_in]
        dlcs_out.add(dlc_out)
    return dlcs_out

def get_available_states(dlcs: set[str]) -> set[str]:
    states_out = set[str]()
    for dlc, states in dlc_states_dict.items():
        if dlc in dlcs:
            states_out = states_out.union(states)

    return states_out
