from collections import Counter, defaultdict
from dataclasses import dataclass
from random import Random
from typing import Any, Optional

from worlds.AutoWorld import World

from ..Helpers import remove_specific_item
from ..Items import ManualItem, item_name_to_item

from .CsvData import Region, city_dict, company_list, photo_trophies_dict, viewpoints_dict, land_connections_dict
from .Func import snake_case, pop_iter
from .Options import starting_state
from .OptionDefs import KeyItemChoice

early_item_count: int = 0
total_checks: Counter[str] = Counter()

@dataclass(frozen=True)
class CheckInfo:
    name: str
    check_type: str
    region: Optional[Region] # Companies do not have a singular region

def adjust_item_counts(item_config: list, world: World) -> None:
    # For countable item types, set the count based on the player options.
    # The countable item types are:

    # Piece of Secret Delivery #(i) Instructions
    for i in range(1, 21):
        piece = f'Piece of Secret Delivery #{i} Instructions'
        if piece in item_config:
            item_config[piece] = world.options.secret_delivery_instruction_parts.value

    # Secret Delivery Completion
    if 'Secret Delivery Completion' in item_config:
        item_config['Secret Delivery Completion'] = world.options.secret_deliveries_available.value

    # Delivery Token
    if 'Delivery Token' in item_config:
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
    opt = world.multiworld.local_early_items[world.player]
    if item_name in opt:
        opt[item_name] += 1
    else:
        opt[item_name] = 1
    early_item_count += 1

def perform_final_grants(item_pool: list, world: World) -> list[str]:
    options = world.options

    # Assign the selected Starter Key and Key.
    start_with_item(f'{starting_state} Starter Key', item_pool, world)
    start_with_item(f'{starting_state} Key', item_pool, world)

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
            if truck_on_brand in [snake_case(which), 'all']:
                if options.truck_contract_brand_item_location == KeyItemChoice.option_start_with_item:
                    start_with_item(k, item_pool, world)
                elif options.truck_contract_brand_item_location == KeyItemChoice.option_find_item_early:
                    early_item(k, world)
            else:
                if options.truck_contract_off_brand_item_location == KeyItemChoice.option_start_with_item:
                    start_with_item(k, item_pool, world)
                elif options.truck_contract_off_brand_item_location == KeyItemChoice.option_find_item_early:
                    early_item(k, world)

        # For grantable items, check the option to find out what's done about it
        if opt := data.get('granting_option'):
            val = options.getattr(opt).value
            if val == KeyItemChoice.option_start_with_item:
                start_with_item(k, item_pool, world)
            elif val == KeyItemChoice.option_find_item_early:
                early_item(k, world)

    # Get additional keys if needed
    get_additional_state_keys(item_pool, world)

    return item_names_to_remove

def implement_checks_reduction(world: World):
    options = world.options
    randomizer: Random = world.random

    chance_of_state: float = options.checks_percent_of_state_count.value / 100
    max_state_count: int = options.checks_max_state_count.value
    chance_of_check: float = options.checks_percent.value / 100
    max_count_per_state: int = options.checks_max_per_state_count.value
    max_count_companies: int = options.company_checks_count.value
    max_check_count: int = options.max_checks_count.value

    # shortcut
    if chance_of_state == 1 and chance_of_check == 1 and max_check_count == 0 \
        and max_count_per_state == 0 and max_count_companies == 0 and max_check_count == 1:
            return []

    all_states = list[str](options.states_available.value)
    all_states.remove(starting_state)
    accepted_states = set[str](starting_state)

    randomizer.shuffle(all_states)

    if max_state_count != 1:
        for state in all_states:
            # Don't call for randomization if chance is guaranteed:
            if chance_of_state == 1 or randomizer.random() <= chance_of_state:
                accepted_states.add(state)
                if max_state_count and len(accepted_states) >= max_state_count:
                    break

    all_checks_list: list[CheckInfo] = []

    # Build the list of checks
    if options.enable_citysanity:
        for city in city_dict.values():
            all_checks_list.append(CheckInfo(city.check_name, 'City', city.region))

    if options.enable_companysanity:
        for company in company_list:
            all_checks_list.append(CheckInfo(company, 'Company', None))

    if options.enable_photosanity:
        for photo in photo_trophies_dict.values():
            all_checks_list.append(CheckInfo(photo.check_name, 'Photo Trophy', photo.region))

    if options.enable_viewpointsanity:
        for view in viewpoints_dict.values():
            all_checks_list.append(CheckInfo(view.check_name, 'Viewpoint', viewpoints_dict))

    randomizer.shuffle(all_checks_list)

    # And start tearing it down
    checks_to_remove: list[str] = []
    sum_checks = 0

    for check in pop_iter(all_checks_list):
        reject: bool = False

        state = check.region.state if check.region else None
        if state:
            if total_checks[state] >= max_count_per_state: reject = True
        else:
            if total_checks[None] >= max_count_companies: reject = True

        if chance_of_check < 1 and randomizer.random() > chance_of_check:
            reject = True

        if reject:
            checks_to_remove.append(f'{check.check_type} - {check.name}')
        else:
            sum_checks += 1
            total_checks[state] += 1
            if sum_checks >= max_check_count: break

    for check in all_checks_list:
        checks_to_remove.append(f'{check.check_type} - {check.name}')

    return checks_to_remove

def get_additional_state_keys(item_pool: list, world: World) -> None:
    """
    Gets additional keys to put enough early checks in logic in sphere 1.
    """

    dlcs = world.options.dlcs_available.value
    total_checks_in_starting_logic = total_checks[starting_state]
    checks_needed = early_item_count + 1

    if total_checks_in_starting_logic >= checks_needed: return

    states_in_starting_logic = {starting_state}
    connected_states = get_land_connected_states(starting_state, world)
    randomizer: Random = world.random

    while total_checks_in_starting_logic < checks_needed and connected_states:
        next_state = randomizer.choice(connected_states)
        connected_states.remove(next_state)
        states_in_starting_logic.add(next_state)
        start_with_item(f'{next_state} Key', item_pool, world)
        total_checks_in_starting_logic += total_checks[next_state]
        connected_states |= get_land_connected_states(next_state, world) - states_in_starting_logic

def get_land_connected_states(state: str, dlc_list: set[str], world: World) -> set[str]:
    out = set[str]()

    for r1, r2_list in land_connections_dict.items():
        if r1.state != state: continue
        if r1.dlc not in dlc_list: continue

        out |= {r.state for r in r2_list if r.dlc in dlc_list and r.state != r1.state}

    return out
