from collections import Counter, defaultdict
from dataclasses import dataclass
from random import Random
from typing import Any, Optional

from worlds.AutoWorld import World
from BaseClasses import MultiWorld

from ..Helpers import get_option_value, remove_specific_item
from ..Items import ManualItem, item_name_to_item

from .CsvData import Region, city_dict, company_list, photo_trophies_dict, viewpoints_dict, land_connections_dict
from .Func import nixprint, snake_case, pop_iter
from .Options import get_starting_state
from .OptionDefs import KeyItemChoice

early_item_count: int = 0
total_checks: Counter[str] = Counter()
early_checks: Counter[str] = Counter()
randomizer: Random = None

@dataclass(frozen=True)
class CheckInfo:
    name: str
    check_type: str
    region: Optional[Region] # Companies do not have a singular region
    count_early: bool

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

def implement_checks_reduction(world: World):
    global total_checks
    global early_checks
    global early_item_count
    global randomizer

    options = world.options
    if not randomizer:
        randomizer = Random(options.checks_reduction_seed.value)

    chance_of_state: float = options.checks_percent_of_state_count.value / 100
    max_state_count: int = options.checks_max_state_count.value
    chance_of_check: float = options.checks_percent.value / 100
    max_count_per_state: int = options.checks_max_per_state_count.value
    max_count_companies: int = options.company_checks_count.value
    max_check_count: int = options.max_checks_count.value

    # nixprint(f'chance_of_state: {chance_of_state}')
    # nixprint(f'chance_of_check: {chance_of_check}')
    # nixprint(f'max_check_count: {max_check_count}')
    # nixprint(f'max_count_per_state: {max_count_per_state}')
    # nixprint(f'max_count_companies: {max_count_companies}')
    # nixprint(f'max_check_count: {max_check_count}')
    # temporarily skipping this shortcut for debugging this method
    # shortcut
    if chance_of_state == 1 and chance_of_check == 1 and max_check_count == 0 \
        and max_count_per_state == 0 and max_count_companies == 0 and max_check_count == 0:
            return []

    all_states = list[str](options.states_available.value)
    # nixprint(f'all_states: {all_states}')
    # nixprint(f'starting_state: {get_starting_state()}')
    all_states.remove(get_starting_state())
    accepted_states = {get_starting_state()}

    randomizer.shuffle(all_states)

    if max_state_count != 1:
        for state in all_states:
            # Don't call for randomization if chance is guaranteed:
            if chance_of_state == 1 or randomizer.random() <= chance_of_state:
                accepted_states.add(state)
                if max_state_count and len(accepted_states) >= max_state_count:
                    break

    # nixprint(f'Accepted states: {accepted_states}')

    all_checks_list: list[CheckInfo] = []

    # Build the list of checks
    if options.enable_citysanity:
        for city in city_dict.values():
            all_checks_list.append(CheckInfo(city.check_name, 'City', city.region, True))

    if options.enable_companysanity:
        for company in company_list:
            all_checks_list.append(CheckInfo(company, 'Company', None, False))

    photosanity_early = (options.enable_photosanity == KeyItemChoice.option_start_with_item)

    if options.enable_photosanity:
        for photo in photo_trophies_dict.values():
            all_checks_list.append(CheckInfo(photo.check_name, 'Photo Trophy', photo.region, photosanity_early))

    viewsanity_early = (options.enable_viewpointsanity == KeyItemChoice.option_start_with_item)

    if options.enable_viewpointsanity:
        for view in viewpoints_dict.values():
            all_checks_list.append(CheckInfo(view.check_name, 'Viewpoint', view.region, viewsanity_early))

    randomizer.shuffle(all_checks_list)

    # And start tearing it down
    checks_to_remove: list[str] = []
    sum_checks = 0

    for check in pop_iter(all_checks_list):
        reject: bool = False

        state = check.region.state if check.region else None
        if state:
            if max_count_per_state and total_checks[state] >= max_count_per_state: reject = True
        else:
            if max_count_companies and total_checks[None] >= max_count_companies: reject = True

        if chance_of_check < 1 and randomizer.random() > chance_of_check:
            reject = True

        if reject:
            # nixprint(f'Removing check: {check.check_type} - {check.name}')
            checks_to_remove.append(f'{check.check_type} - {check.name}')
        else:
            # nixprint(f'Keeping check: {check.check_type} - {check.name}')
            sum_checks += 1
            total_checks[state] += 1
            if check.count_early:
                early_checks[state] += 1
            if max_check_count and sum_checks >= max_check_count: break

    for check in all_checks_list:
        checks_to_remove.append(f'{check.check_type} - {check.name}')

    return checks_to_remove

def perform_final_grants(item_pool: list, world: World) -> list[str]:
    options = world.options

    # Assign the selected Starter Key and Key.
    start_with_item(f'{get_starting_state()} Starter Key', item_pool, world)
    start_with_item(f'{get_starting_state()} Key', item_pool, world)

    # For truck contracts, first we should check which option was selected...
    truck_on_brand = options.truck_contract_item_brand.current_key.removeprefix('option_')

    item_names_to_remove: list[str] = [] # List of item names

    for k, v in item_name_to_item.items():
        if not 'extra_data' in v: continue
        data: dict[str, Any] = v['extra_data']
        tp: str = data.get('type')
        which: str = data.get('which')

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
                elif options.truck_contract_brand_item_location == KeyItemChoice.option_find_item_early:
                    # nixprint(f'Find contract early.')
                    early_item(k, world)
                # else:
                #     nixprint(f'Find contract anywhere.')
            else:
                # nixprint(f'Off brand:')
                if options.truck_contract_off_brand_item_location == KeyItemChoice.option_start_with_item:
                    # nixprint(f'Start with contract.')
                    start_with_item(k, item_pool, world)
                elif options.truck_contract_off_brand_item_location == KeyItemChoice.option_find_item_early:
                    # nixprint(f'Find contract early.')
                    early_item(k, world)
                # else:
                #     nixprint(f'Find contract anywhere.')

        # For grantable items, check the option to find out what's done about it
        if opt := data.get('granting_option'):
            val = getattr(options, opt).value
            if val == KeyItemChoice.option_start_with_item:
                start_with_item(k, item_pool, world)
            elif val == KeyItemChoice.option_find_item_early:
                early_item(k, world)

    # Get additional keys if needed
    get_additional_state_keys(item_pool, world)

    return item_names_to_remove

def get_additional_state_keys(item_pool: list, world: World) -> None:
    """
    Gets additional keys to put enough early checks in logic in sphere 1.
    """
    global early_checks
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
