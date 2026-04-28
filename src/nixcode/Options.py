# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from random import Random
from typing import Any, Iterable
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState, Item

from .CsvData import dlc_connections, dlc_aliases_dict, dlc_states_dict, dlc_name_list, state_list, dlc_dict
from .OptionDefs import QuickTravelTicketItem, StartingLocation
from .Func import get_case_key_opt, get_case_opt, in_case, nixprint, snake_case, random_string
from ..Helpers import is_option_enabled, get_option_value

starting_state = ''

def get_starting_state() -> str:
    return starting_state

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
    global starting_state
    options = world.options

    options.dlcs_available.value = chosen_dlcs = get_enabled_dlcs_and_base_game(options.dlcs_available.value)
    available_states = get_available_states(chosen_dlcs)
    options.states_available.value = enabled_states = get_enabled_states(options.states_available.value, chosen_dlcs)

    # If enabled DLCs are not all connected and the Quick Travel Ticket is disabled, enable it.
    if not options.quick_travel_item and not are_dlcs_connected(chosen_dlcs):
        options.quick_travel_item.value = QuickTravelTicketItem.option_start_with_item

    # Ensure required counts don't exceed available counts.
    if options.delivery_tokens_required > options.delivery_tokens_available:
        options.delivery_tokens_required.value = options.delivery_tokens_available.value

    if options.secret_deliveries_required > options.secret_deliveries_available:
        options.secret_deliveries_required.value = options.secret_deliveries_available.value

    # Validates the starting state, re-choosing if necessary.
    starting_location = options.starting_location.current_key
    start_array = [state for state in available_states if snake_case(state) == starting_location.removeprefix('option_')]
    if start_array:
        starting_state = start_array.pop()
    if options.starting_location.current_key not in [snake_case(state) for state in available_states]:
        starting_state = world.random.choice([*available_states])
        options.starting_location.value = getattr(StartingLocation, f'option_{snake_case(starting_state)}')

    # Ensures that the starting state has checks that exist.
    options.states_available.value.add(starting_state)

    # Ensures that at least one level is enabled if the goal is player level checks.
    if options.goal.value == getattr(options.goal, 'option_Max Player Level Check Reached') and options.player_level_checks.value < 5:
        options.player_level_checks.value = 5

    # Ensures that at least one check type is enabled
    if not options.enable_citysanity and \
        not options.enable_companysanity and \
        not options.enable_photosanity and \
        not options.enable_viewpointsanity and \
        not options.player_level_checks:
            options.enable_citysanity.value = 1

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

def get_enabled_dlcs_and_base_game(dlcs_in: set[str]) -> set[str]:
    result = {"Base Game", *get_enabled_dlcs(dlcs_in)}
    # nixprint(f'Enabled DLCs: {result}')
    return result

def get_enabled_dlcs(dlcs_in: set[str]) -> set[str]:
    """
    Returns the set of all enabled DLCs, with aliases parsed.
    """
    if 'all' in {a.lower() for a in dlcs_in}:
        result = {dlc.name for dlc in dlc_dict.values() if dlc.is_main_map}
        nixprint(f'ALL detected, returning {result}', 5)
        return result
    if 'really_all' in {snake_case(a) for a in dlcs_in}:
        result = {*dlc_name_list}
        nixprint(f'REALLY_ALL detected, returning {result}', 5)
        return result
    return [*parse_dlc_names(dlcs_in)]
    # dlc_aliases_dict[dlc_in.lower()] for dlc_in in dlcs_in

def parse_dlc_names(dlcs_in: set[str]) -> Iterable[str]:
    for name in dlcs_in:
        preceding_mode = False

        if name.startswith('<'):
            name = name[1:].lstrip()
            preceding_mode = True

        if name.lower() in dlc_aliases_dict:
            name = dlc_aliases_dict[name]

        yield name

        if preceding_mode:
            release = dlc_dict[name].date
            for dlc in [dlc.name for dlc in dlc_dict.values() if dlc.date < release and dlc.is_main_map]:
                yield dlc

def get_available_states(dlcs: set[str]) -> set[str]:
    """
    Returns the set of all available DLCs in the given set of DLCs.
    """
    states_out = set[str]()
    for dlc, states in dlc_states_dict.items():
        if dlc in dlcs or dlc == 'Base Game':
            states_out = states_out.union(states)

    # nixprint(f'Available states: {states_out}')
    return states_out

def get_enabled_states(states: set[str], dlcs: set[str]) -> set[str]:
    """
    Parses the enabled state list, returning the intersection of available and enabled states,
    and parsing DLC names as well.
    """
    available_states = get_available_states(dlcs)
    if not states or in_case(states, 'all'):
        # nixprint('No states specified in option. Returning all available, which was just printed above.')
        return available_states

    states_output = set[str]()

    for state in states:
        if state := get_case_opt(state_list, state):
            states_output.add(state)
        if states_by_dlc := get_case_key_opt(dlc_name_list, state):
            states_output.update(states_by_dlc)

    result = states_output.intersection(available_states)
    # nixprint(f'Enabled states: {result}')
    return result
