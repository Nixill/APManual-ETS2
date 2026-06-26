from collections import Counter, defaultdict
from dataclasses import dataclass
from random import Random
from typing import Any, Optional

from worlds.AutoWorld import World
from BaseClasses import MultiWorld

from ..Helpers import get_option_value, remove_specific_item
from ..Items import ManualItem, item_name_to_item

from .CsvData import land_connections_dict, truck_makes_list
from .Func import nixprint, snake_case
from .Options import get_available_states, get_starting_state
from .OptionDefs import KeyItemChoice

randomizer: Random = None

def check_for_item(multiworld: MultiWorld, player: int, item:  dict[str, Any]) -> Optional[bool]:
    if not 'extra_data' in item: return None
    extra_data: dict[str, Any] = item["extra_data"]
    tp = extra_data['type']

    if tp == 'secret_delivery_instructions':
        if get_option_value(multiworld, player, 'secret_deliveries_available') < extra_data['secret_delivery_number']: return False

    return None


def adjust_item_counts(item_config: dict[str, int|dict], world: World) -> None:
    # For countable item types, set the count based on the player options.
    # The countable item types are:

    # Piece of Secret Delivery #(i) Instructions
    for i in range(1, 21):
        piece = f'Piece of Secret Delivery #{i} Instructions'
        if piece in item_config and item_config[piece] != 0:
            item_config[piece] = world.options.secret_delivery_instruction_parts.value

    # Secret Delivery Completion
    if 'Secret Delivery Completion' in item_config and item_config['Secret Delivery Completion'] != 0:
        item_config['Secret Delivery Completion'] = world.options.secret_deliveries_available.value

    # Delivery Token
    if 'Delivery Token' in item_config and item_config['Delivery Token'] != 0:
        item_config['Delivery Token'] = world.options.delivery_tokens_available.value

    # and Player Level
    if 'Player Level' in item_config:
        if world.options.skill_items_on_levels.value and not world.options.skill_items_scattered.value:
            item_config['Player Level'] = 36
        else:
            item_config['Player Level'] = world.options.player_level_checks.value

def start_with_item(item_name: str, item_pool: list, world: World) -> None:
    if item_name in world.start_inventory:
        world.start_inventory[item_name] += 1
    else:
        world.start_inventory[item_name] = 1

    item = next(i for i in item_pool if i.name == item_name)
    world.multiworld.push_precollected(item)
    remove_specific_item(item_pool, item)

def early_item(item_name: str, world: World) -> None:
    global early_item_count
    opt = world.multiworld.local_early_items[world.player]
    if item_name in opt:
        opt[item_name] += 1
    else:
        opt[item_name] = 1
    early_item_count += 1

def hint_item(item_name: str, world: World) -> None:
    world.options.start_hints.value.add(item_name)

def perform_final_grants(item_pool: list, world: World) -> list[str]:
    options = world.options

    nixprint(f'Options: {options}', 8)
    nixprint(f'Item Pool: {[item.name for item in item_pool]}', 8)

    # Assign the selected Starter Key and Key.
    start_with_item(f'{get_starting_state()} Starter Key', item_pool, world)
    start_with_item(f'{get_starting_state()} Key', item_pool, world)

    # For truck contracts, first we should check which option was selected...
    truck_on_brand = options.truck_contract_item_brand.current_key.removeprefix('option_')

    # For player skills, check if we're granting those items automatically...
    player_skills_auto_grant = not (options.skill_items_on_levels or options.skill_items_scattered)

    item_names_to_remove: list[str] = [] # List of item names

    for k, v in item_name_to_item.items():
        if not 'extra_data' in v: continue
        data: dict[str, Any] = v['extra_data']
        tp: str = data.get('type')
        which: str = data.get('which')

        # Start with player skills if not scattered
        if tp == 'skill' and player_skills_auto_grant:
            start_with_item(k, item_pool, world)

        # Remove all Starter Keys
        if tp == 'state_starter_key':
            item_names_to_remove.append(k)

        # Truck contract handling
        if tp == 'truck_purchase_contract':
            # nixprint(f'Truck Contract: {k}')
            if truck_on_brand in [snake_case(which), 'all']:
                # nixprint(f'On brand:')
                if options.truck_contract_brand_item_location == KeyItemChoice.option_start_with_item:
                    # nixprint(f'Start with contract.')
                    start_with_item(k, item_pool, world)
                elif options.truck_contract_brand_item_location in \
                    [KeyItemChoice.option_find_item_early, KeyItemChoice.option_find_item_early_with_hint]:
                        # nixprint(f'Find contract early.')
                        early_item(k, world)
                # else:
                #     nixprint(f'Find contract anywhere.')

                if options.truck_contract_brand_item_location in \
                    [KeyItemChoice.option_find_item_with_hint, KeyItemChoice.option_find_item_early_with_hint]:
                        # nixprint(f'Hint enabled for contract.')
                        hint_item(k, world)
            else:
                # nixprint(f'Off brand:')
                if options.truck_contract_off_brand_item_location == KeyItemChoice.option_start_with_item:
                    # nixprint(f'Start with contract.')
                    start_with_item(k, item_pool, world)
                elif options.truck_contract_off_brand_item_location in \
                    [KeyItemChoice.option_find_item_early, KeyItemChoice.option_find_item_early_with_hint]:
                        # nixprint(f'Find contract early.')
                        early_item(k, world)
                # else:
                #     nixprint(f'Find contract anywhere.')

                if options.truck_contract_brand_item_location in \
                    [KeyItemChoice.option_find_item_with_hint, KeyItemChoice.option_find_item_early_with_hint]:
                        # nixprint(f'Hint enabled for contract.')
                        hint_item(k, world)

        # For grantable items, check the option to find out what's done about it
        if opt := data.get('granting_option'):
            val = getattr(options, opt).value
            if val == KeyItemChoice.option_start_with_item:
                start_with_item(k, item_pool, world)
            elif val in [KeyItemChoice.option_find_item_early, KeyItemChoice.option_find_item_early_with_hint]:
                early_item(k, world)

            if val in [KeyItemChoice.option_find_item_with_hint, KeyItemChoice.option_find_item_early_with_hint]:
                hint_item(k, world)

    # Get additional keys if needed
    get_additional_state_keys(item_pool, world)

    return item_names_to_remove

def get_additional_state_keys(item_pool: list, world: World) -> None:
    """
    Gets additional keys to put enough early checks in logic in sphere 1.
    """
    from .Locations import early_checks

    global early_item_count

    dlcs = world.options.dlcs_available.value
    total_checks_in_starting_logic = early_checks[get_starting_state()]
    checks_needed = early_item_count + 1

    nixprint(f'DLCs: {dlcs}', 2)
    nixprint(f'Total checks in starting logic: {total_checks_in_starting_logic}', 2)
    nixprint(f'Total starting checks needed: {checks_needed}', 2)

    if total_checks_in_starting_logic >= checks_needed:
        nixprint('Total check requirement satisfied without additional keys.', 2)
        return

    states_in_starting_logic = {get_starting_state()}
    connected_states = get_land_connected_states(get_starting_state(), dlcs)
    # This uses the existing world.random because it grants state keys rather than altering world state directly
    randomizer: Random = world.random

    nixprint(f'States in starting logic: {states_in_starting_logic}', 2)
    nixprint(f'Connected states: {connected_states}', 2)

    while total_checks_in_starting_logic < checks_needed and connected_states:
        nixprint('Total checks in starting logic still not satisfied.', 2)
        next_state = randomizer.choice(list(connected_states))
        nixprint(f'Next state: {next_state}', 2)
        connected_states.remove(next_state)
        states_in_starting_logic.add(next_state)
        start_with_item(f'{next_state} Key', item_pool, world)
        total_checks_in_starting_logic += early_checks[next_state]
        nixprint(f'Checks now in starting logic: {total_checks_in_starting_logic}')
        connected_states |= get_land_connected_states(next_state, dlcs) - states_in_starting_logic
        nixprint(f'States now connected: {connected_states}', 2)

def get_land_connected_states(state: str, dlc_list: set[str]) -> set[str]:
    nixprint(f'Checking land connections for {state} with DLCs {dlc_list}:', 2)
    out = set[str]()

    subdict = {k: v for k, v in land_connections_dict.items() if k.state == state and k.dlc in dlc_list}
    nixprint(f'Subdict of land connections: {subdict}')

    for r2_list in subdict.values():
        out |= {r.state for r in r2_list if r.dlc in dlc_list and r.state != state}

    return out

def item_options_enabled(options: World.Options, keys: set[str]) -> int:
    count = 0
    for key in keys:
        if 'find_item' in getattr(options, key):
            count += 1
    return count

@dataclass(frozen=False)
class ProgressionCount:
    mandatory: int = 0
    '''
    Mandatory progression items.

    Country keys, misc items, on-brand truck contract(s), progression skills, and at least one victory item.

    Up to 16 player levels are also counted, if there are fewer than 16 Skill locations.
    '''
    trucks: int = 0
    '''Off-brand truck contracts, which are considered optional.'''
    levels: int = 0
    '''
    Removable player levels.

    20 of the 36 player levels are non-progression and can be removed. If there are more than 16 Skill locations,
    this number is reduced by (16 less than) the number of Skill locations.
    '''
    tokens: int = -1
    '''
    Delivery tokens.

    -1 means the goal is disabled. Otherwise, this counts the number of REMOVABLE tokens.
    At least one must be kept, which is not part of this count.
    '''
    deliveries: int = -1
    '''
    Secret deliveries.

    -1 means the goal is disabled. Otherwise, this counts the number of REMOVABLE PARTS of secret deliveries.
    At least one secret delivery must be kept, which is not part of this count.
    '''
    def total(self) -> int:
        '''Total count of all items counted.'''
        return self.mandatory + self.trucks + self.levels + self.tokens + self.deliveries

def count_progression_items(options: World.Options) -> ProgressionCount:
    output = ProgressionCount()

    # One for each available state you don't start in
    output.mandatory += get_available_states(options.dlcs_available.value) - 1

    # One for each singular Misc Item that needs to be found (not started or disabled)
    output.mandatory += item_options_enabled(options, [
        'enable_photosanity', 'enable_viewpointsanity', 'ferry_ticket_item', 'bank_loan_approval_item', 'trailer_contract_item', 'quick_travel_item'
    ])

    # For truck contracts, figure out on brand vs off brand
    truck_count = len(truck_makes_list)
    on_brand = 0

    if options.truck_contract_item_brand.key == 'all':
        on_brand = truck_count
    elif options.truck_contract_item_brand.key != 'none':
        on_brand = 1

    off_brand = truck_count - on_brand

    output.mandatory += on_brand * item_options_enabled(options, ['truck_contract_brand_item_location'])
    output.trucks += off_brand * item_options_enabled(options, ['truck_contract_off_brand_item_location'])

    # Player skills, if enabled
    if options.skill_items_scattered:
        levels = 36
        if options.skill_items_on_levels:
            levels -= options.player_level_count.value

        if levels > 20:
            output.mandatory += levels - 20
            output.levels = 20
        else:
            output.levels = levels

    # Delivery tokens, if enabled
    if options.goal.key == 'all delivery tokens collected':
        output.tokens += options.delivery_tokens_available.value - 1
        output.mandatory += 1

    # Secret deliveries, if enabled
    elif options.goal.key == 'all secret deliveries completed':
        pieces = options.secret_delivery_instruction_parts.value
        output.deliveries += (options.secret_deliveries_available.value - 1) * pieces
        output.mandatory += 1

    return output
