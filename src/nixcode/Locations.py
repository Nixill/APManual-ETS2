from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any, Optional

from BaseClasses import MultiWorld
from worlds.AutoWorld import World
from .CsvData import Region, city_dict, company_list, photo_trophies_dict, viewpoints_dict, company_regions_dict
from .Func import nixprint, pop_iter
from .OptionDefs import KeyItemChoice
from .Options import get_starting_state
from .DataClasses import Region
from .Items import count_progression_items
from ..hooks.Helpers import get_option_value, is_region_enabled

total_checks: Counter[str] = Counter()
early_checks: Counter[str] = Counter()

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

@dataclass(frozen=True)
class CheckInfo:
    name: str
    check_type: str
    region: Optional[Region] # Companies do not have a singular region
    count_early: bool

def implement_checks_reduction(world: World):
    # do nothing in a fake gen (UT)
    if hasattr(world.multiworld, 'generation_is_fake'): return []

    from .Items import count_progression_items, ProgressionCount

    global total_checks
    global early_checks

    options = world.options
    randomizer = world.random

    chance_of_state: float = options.checks_percent_of_state_count.value / 100
    max_state_count: int = options.checks_max_state_count.value
    chance_of_check: float = options.checks_percent.value / 100
    max_count_per_state: int = options.checks_max_per_state_count.value
    max_count_companies: int = options.company_checks_count.value
    max_check_count: int = options.max_checks_count.value

    nixprint(f'chance_of_state: {chance_of_state}', 10)
    nixprint(f'chance_of_check: {chance_of_check}', 10)
    nixprint(f'max_check_count: {max_check_count}', 10)
    nixprint(f'max_count_per_state: {max_count_per_state}', 10)
    nixprint(f'max_count_companies: {max_count_companies}', 10)
    nixprint(f'max_check_count: {max_check_count}', 10)

    progression_count = count_progression_items(options)

    nixprint(f'progression_count.mandatory: {progression_count.mandatory}', 10)
    nixprint(f'progression_count.total(): {progression_count.total()}', 10)

    all_states = list[str](options.states_available.value)
    available_dlcs = set[str](options.dlcs_available.value)
    nixprint(f'all_states: {all_states}', 10)

    starting_state = get_starting_state()
    nixprint(f'starting_state: {get_starting_state()}', 10)
    all_states.remove(get_starting_state())
    randomizer.shuffle(all_states)

    accepted_states: list[str] = [starting_state]
    rejected_states: list[str] = []

    if max_state_count != 1:
        for state in pop_iter(all_states):
            # Don't call for randomization if min check count isn't met or chance is guaranteed:
            if chance_of_state == 1 or randomizer.random() <= chance_of_state:
                nixprint(f'added state: {state}', 10)
                accepted_states.add(state)
                if len(all_checks_set) > progression_count.mandatory and max_state_count and len(accepted_states) >= max_state_count:
                    nixprint(f'max state count reached!', 10)
                    break
            else:
                nixprint(f'skipped state: {state}', 10)
                rejected_states.append(state)

    nixprint(f'accepted_states (without min check check): {accepted_states}')

    # Build the list of potential checks
    potential_checks_dict: defaultdict[str, set[CheckInfo]] = defaultdict(set)

    ferry_early = (options.ferry_ticket_item == KeyItemChoice.option_start_with_item)

    if options.enable_citysanity:
        for city in city_dict.values():
            if city.region.dlc in available_dlcs:
                potential_checks_dict[city.region.state].add(
                    CheckInfo(city.check_name, 'City', city.region, ferry_early or not city.ferry_required))

    photosanity_early = (options.enable_photosanity == KeyItemChoice.option_start_with_item)

    if options.enable_photosanity:
        for photo in photo_trophies_dict.values():
            if photo.region.dlc in available_dlcs:
                potential_checks_dict[photo.region.state].add(
                    CheckInfo(photo.check_name, 'Photo Trophy', photo.region, photosanity_early and (ferry_early or not photo.ferry_required)))

    viewsanity_early = (options.enable_viewpointsanity == KeyItemChoice.option_start_with_item)

    if options.enable_viewpointsanity:
        for view in viewpoints_dict.values():
            if view.region.dlc in available_dlcs:
                potential_checks_dict[view.region.state].add(
                    CheckInfo(view.check_name, 'Viewpoint', view.region, viewsanity_early and (ferry_early or not view.ferry_required)))

    if options.enable_companysanity:
        for company in company_list:
            for region in company_regions_dict[company]:
                if region.dlc in available_dlcs:
                    potential_checks_dict[region.state].add(CheckInfo(company, 'Company', None, False))

    all_checks_set = set[CheckInfo]()

    # Now populate the all_checks_set with potential checks from selected states
    for state in accepted_states:
        all_checks_set |= potential_checks_dict[state]

    while rejected_states and len(all_checks_set) < progression_count.mandatory:
        nixprint(f'Moved state {state} to accepted for check count.')
        state = rejected_states.pop()
        accepted_states.append(state)
        all_checks_set |= potential_checks_dict[state]

    all_checks_list = list(all_checks_set)
    randomizer.shuffle(all_checks_list)

    nixprint(f'length of all_checks_list: {len(all_checks_list)}', 10)

    # And start tearing it down
    checks_to_remove: list[str] = []
    sum_checks = 0
    deleted_checks = 0
    reject_all = True

    for check in pop_iter(all_checks_list):
        reject: bool = False

        state = check.region.state if check.region else None
        if state:
            if max_count_per_state and total_checks[state] >= max_count_per_state:
                reject = True
                nixprint(f'Removing check: {check.check_type} - {check.name} (max checks reached for {state})', 10)
        else:
            if max_count_companies and total_checks[None] >= max_count_companies:
                nixprint(f'Removing check: {check.check_type} - {check.name} (max companies reached)', 10)
                reject = True

        if (not reject) and chance_of_check < 1 and randomizer.random() > chance_of_check:
            nixprint(f'Removing check: {check.check_type} - {check.name} (chance failed)', 10)
            reject = True

        if reject:
            # nixprint(f'Removing check: {check.check_type} - {check.name}', 10)
            checks_to_remove.append(f'{check.check_type} - {check.name}')
            deleted_checks += 1
            if progression_count.mandatory >= sum_checks + len(all_checks_list):
                nixprint(f'Min check count reached! Accepting all other checks.', 10)
                reject_all = False
        else:
            nixprint(f'Keeping check: {check.check_type} - {check.name}', 10)
            sum_checks += 1
            total_checks[state] += 1
            if check.count_early:
                nixprint(f'  (added to early list)', 10)
                early_checks[state] += 1
            if max_check_count and sum_checks >= max_check_count:
                nixprint(f'Max check count reached! Removing all other checks.', 10)
                break

    if reject_all:
        for check in all_checks_list:
            checks_to_remove.append(f'{check.check_type} - {check.name}')
    else:
        for check in all_checks_list:
            sum_checks += 1
            total_checks[state] += 1
            if check.count_early:
                early_checks[state] += 1

    nixprint(f'sum_checks: {sum_checks}', 10)
    nixprint(f'len(checks_to_remove): {checks_to_remove}', 10)

    return checks_to_remove
