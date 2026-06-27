from collections import Counter, defaultdict
from dataclasses import dataclass
from random import Random
from typing import Any, Optional

from worlds.AutoWorld import World
from BaseClasses import MultiWorld, Item

from ..Helpers import get_option_value
from ..Items import ManualItem, item_name_to_item

from .CsvData import land_connections_dict, truck_makes_list
from .Func import dbgprint, snake_case
from .Options import get_available_states, get_starting_state
from .OptionDefs import KeyItemChoice, KeyItemChoiceWithDisable

randomizer: Random = None
early_item_count: int = 0

from ..Helpers import remove_specific_item
# def remove_specific_item(source: list[Item], item: Item) -> Item:
#     """Remove and return an item from a list in a more precise way, base AP only check for name and player id before removing.
#     \nThis checks that the item IS the exact same in the list.
#     \nUnlike core code, DO NOT raise ValueError if the item is not in the list."""
#     # Inspired by https://stackoverflow.com/a/58761459
#     for i in range(len(source)): # check all elements of the list like a normal remove does
#         if item is source[i]:
#             return source.pop(i)

#     # if we reach here we didn't get any item

def check_for_item(multiworld: MultiWorld, player: int, item:  dict[str, Any]) -> Optional[bool]:
    if not 'extra_data' in item: return None
    extra_data: dict[str, Any] = item["extra_data"]
    tp = extra_data['type']

    if tp == 'secret_delivery_instructions':
        if get_option_value(multiworld, player, 'secret_deliveries_available') < extra_data['secret_delivery_number']: return False

    return None


def adjust_item_counts(item_config: dict[str, int|dict], world: World) -> None:
    # do nothing in a fake gen (UT)
    if hasattr(world.multiworld, 'generation_is_fake'): return

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

def start_with_item(item_name: str, item_pool: list, world: World, count: int = 1) -> None:
    if item_name in world.start_inventory:
        world.start_inventory[item_name] += count
    else:
        world.start_inventory[item_name] = count

    for i in range(count):
        dbgprint(lambda : f'Precollecting and removing {item_name} #{i + 1} from item pool.')
        item = next(i for i in item_pool if i.name == item_name)
        world.multiworld.push_precollected(item)
        remove_specific_item(item_pool, item)
        dbgprint(lambda : f'Item pool after removal: {[item.name for item in item_pool]}')

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
    # do nothing in a fake gen (UT)
    if hasattr(world.multiworld, 'generation_is_fake'): return []

    options = world.options

    dbgprint(lambda : f'Options: {options}')
    dbgprint(lambda : f'Item Pool at start of final grants: {[item.name for item in item_pool]}')

    # Assign the selected Starter Key and Key.
    start_with_item(f'{get_starting_state()} Starter Key', item_pool, world)
    start_with_item(f'{get_starting_state()} Key', item_pool, world)

    dbgprint(lambda : f'Item pool after selected state starter key: {[item.name for item in item_pool]}')

    # For truck contracts, first we should check which option was selected...
    truck_on_brand = options.truck_contract_item_brand.current_key.removeprefix('option_')

    # For player skills, check if we're granting those items automatically...
    player_skills_auto_grant = not (options.skill_items_on_levels or options.skill_items_scattered)
    dbgprint(lambda : f'player_skills_auto_grant: {player_skills_auto_grant}')

    item_names_to_remove: list[str] = [] # List of item names

    for k, v in item_name_to_item.items():
        if not 'extra_data' in v: continue
        data: dict[str, Any] = v['extra_data']
        tp: str = data.get('type')
        which: str = data.get('which')

        # Start with player skills if not scattered
        if tp == 'skill' and player_skills_auto_grant:
            dbgprint(lambda : v)
            if 'count' in v:
                start_with_item(k, item_pool, world, v['count'])
            elif 'classification_count' in v:
                start_with_item(k, item_pool, world, sum(i for t, i in v['classification_count'].items()))

        # Remove all Starter Keys
        if tp == 'state_starter_key':
            item_names_to_remove.append(k)

        # Truck contract handling
        if tp == 'truck_purchase_contract':
            # dbgprint(lambda : f'Truck Contract: {k}')
            if truck_on_brand in [snake_case(which), 'all']:
                # dbgprint(lambda : f'On brand:')
                if options.truck_contract_brand_item_location == KeyItemChoice.option_start_with_item:
                    # dbgprint(lambda : f'Start with contract.')
                    start_with_item(k, item_pool, world)
                elif options.truck_contract_brand_item_location in \
                    [KeyItemChoice.option_find_item_early, KeyItemChoice.option_find_item_early_with_hint]:
                        # dbgprint(lambda : f'Find contract early.')
                        early_item(k, world)
                # else:
                #     dbgprint(lambda : f'Find contract anywhere.')

                if options.truck_contract_brand_item_location in \
                    [KeyItemChoice.option_find_item_with_hint, KeyItemChoice.option_find_item_early_with_hint]:
                        # dbgprint(lambda : f'Hint enabled for contract.')
                        hint_item(k, world)
            else:
                # dbgprint(lambda : f'Off brand:')
                if options.truck_contract_off_brand_item_location == KeyItemChoice.option_start_with_item:
                    # dbgprint(lambda : f'Start with contract.')
                    start_with_item(k, item_pool, world)
                elif options.truck_contract_off_brand_item_location in \
                    [KeyItemChoice.option_find_item_early, KeyItemChoice.option_find_item_early_with_hint]:
                        # dbgprint(lambda : f'Find contract early.')
                        early_item(k, world)
                # else:
                #     dbgprint(lambda : f'Find contract anywhere.')

                if options.truck_contract_brand_item_location in \
                    [KeyItemChoice.option_find_item_with_hint, KeyItemChoice.option_find_item_early_with_hint]:
                        # dbgprint(lambda : f'Hint enabled for contract.')
                        hint_item(k, world)

        # For grantable items, check the option to find out what's done about it
        if opt := data.get('granting_option'):
            val = getattr(options, opt).value
            if val == KeyItemChoiceWithDisable.option_disabled:
                dbgprint(lambda : f'Removing item {k}')
                item = next((i for i in item_pool if i.name == k), None)
                if item:
                    remove_specific_item(item_pool, item)
                else:
                    dbgprint(lambda : '  (not found)')
            elif val == KeyItemChoice.option_start_with_item:
                dbgprint(lambda : f'Starting with item {k}')
                start_with_item(k, item_pool, world)
            elif val in [KeyItemChoice.option_find_item_early, KeyItemChoice.option_find_item_early_with_hint]:
                dbgprint(lambda : f'Early item {k}')
                early_item(k, world)

            if val in [KeyItemChoice.option_find_item_with_hint, KeyItemChoice.option_find_item_early_with_hint]:
                dbgprint(lambda : f'Hinting item {k}')
                hint_item(k, world)

    # Get additional keys if needed
    get_additional_state_keys(item_pool, world)

    dbgprint(lambda : f'Item pool after final grants: {item_pool}')
    dbgprint(lambda : f'Item names to remove: {item_names_to_remove}')

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

    dbgprint(lambda : f'DLCs: {dlcs}')
    dbgprint(lambda : f'Total checks in starting logic: {total_checks_in_starting_logic}')
    dbgprint(lambda : f'Total starting checks needed: {checks_needed}')

    if total_checks_in_starting_logic >= checks_needed:
        dbgprint(lambda : 'Total check requirement satisfied without additional keys.')
        return

    states_in_starting_logic = {get_starting_state()}
    connected_states = get_land_connected_states(get_starting_state(), dlcs)
    # This uses the existing world.random because it grants state keys rather than altering world state directly
    randomizer: Random = world.random

    dbgprint(lambda : f'States in starting logic: {states_in_starting_logic}')
    dbgprint(lambda : f'Connected states: {connected_states}')

    while total_checks_in_starting_logic < checks_needed and connected_states:
        dbgprint(lambda : 'Total checks in starting logic still not satisfied.')
        next_state = randomizer.choice(list(connected_states))
        dbgprint(lambda : f'Next state: {next_state}')
        connected_states.remove(next_state)
        states_in_starting_logic.add(next_state)
        start_with_item(f'{next_state} Key', item_pool, world)
        total_checks_in_starting_logic += early_checks[next_state]
        dbgprint(lambda : f'Checks now in starting logic: {total_checks_in_starting_logic}')
        connected_states |= get_land_connected_states(next_state, dlcs) - states_in_starting_logic
        dbgprint(lambda : f'States now connected: {connected_states}')

def get_land_connected_states(state: str, dlc_list: set[str]) -> set[str]:
    dbgprint(lambda : f'Checking land connections for {state} with DLCs {dlc_list}:')
    out = set[str]()

    subdict = {k: v for k, v in land_connections_dict.items() if k.state == state and k.dlc in dlc_list}
    dbgprint(lambda : f'Subdict of land connections: {subdict}')

    for r2_list in subdict.values():
        out |= {r.state for r in r2_list if r.dlc in dlc_list and r.state != state}

    return out

def item_options_enabled(options: Any, keys: set[str]) -> int:
    count = 0
    for key in keys:
        if 'find_item' in getattr(options, key).current_key:
            count += 1
    return count

@dataclass(frozen=False)
class ProgressionCount:
    mandatory: int = 0
    '''
    Mandatory progression items.

    Country keys, misc items, truck contract(s), progression skills, and at least one victory item.

    Up to 16 player levels are also counted, if there are fewer than 16 Skill locations.
    '''

    levels: int = 0
    '''
    Removable player levels.

    20 of the 36 player levels are non-progression and can be removed. If there are more than 16 Skill locations,
    this number is reduced by (16 less than) the number of Skill locations.
    '''

    tokens: int = 0
    '''
    Delivery tokens.

    0 means the goal is disabled, or no tokens are removable. At least one token must be kept,
    which is not part of this count.
    '''

    deliveries: int = 0
    '''
    Secret deliveries.

    0 means the goal is disabled, or no deliveries are removable. At least one delivery must be
    kept, whose parts are not part of this count.
    '''

    delivery_pieces: int = 0
    '''
    Secret delivery pieces.

    0 means the goal is disabled. Otherwise, this counts the number of instruction pieces per
    secret delivery.

    This property is not counted in the total.
    '''

    delivery_count: int = 0
    '''
    Secret delivery counts.

    0 means the goal is disabled, or no deliveries are removable. At least one delivery must be
    kept, which is not part of this count.

    This property is not counted in the total.
    '''

    def total(self) -> int:
        '''Total count of all items counted.'''
        return self.mandatory + self.levels + self.tokens + self.deliveries

def count_progression_items(options: Any) -> ProgressionCount:
    output = ProgressionCount()

    # One for each available state you don't start in
    output.mandatory += len(get_available_states(options.dlcs_available.value)) - 1

    # One for each singular Misc Item that needs to be found (not started or disabled)
    output.mandatory += item_options_enabled(options, [
        'enable_photosanity', 'enable_viewpointsanity', 'ferry_ticket_item', 'bank_loan_approval_item', 'trailer_contract_item', 'quick_travel_item'
    ])

    # For truck contracts, figure out on brand vs off brand
    truck_count = len(truck_makes_list)
    on_brand = 0

    if options.truck_contract_item_brand.current_key == 'all':
        on_brand = truck_count
    elif options.truck_contract_item_brand.current_key != 'none':
        on_brand = 1

    off_brand = truck_count - on_brand

    output.mandatory += on_brand * item_options_enabled(options, ['truck_contract_brand_item_location'])
    output.mandatory += off_brand * item_options_enabled(options, ['truck_contract_off_brand_item_location'])

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
    if options.goal.value == getattr(options.goal, 'option_All Delivery Tokens Collected'):
        output.tokens += options.delivery_tokens_available.value - 1
        output.mandatory += 1

    # Secret deliveries, if enabled
    if options.goal.value == getattr(options.goal, 'option_All Secret Deliveries Completed'):
        output.delivery_pieces = options.secret_delivery_instruction_parts.value
        output.delivery_count = options.secret_deliveries_available.value - 1
        output.deliveries += output.delivery_count * output.delivery_pieces
        output.mandatory += 1

    return output
