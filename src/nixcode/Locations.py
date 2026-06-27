from collections import Counter, defaultdict
from dataclasses import dataclass
from math import floor
from typing import Any, Optional

from BaseClasses import MultiWorld
from worlds.AutoWorld import World
from .CsvData import Region, city_dict, company_list, photo_trophies_dict, viewpoints_dict, company_regions_dict
from .Func import dbgprint, pop_iter
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

    def __str__(self): return f'{self.check_type} - {self.name}'

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

    dbgprint(lambda : f'chance_of_state: {chance_of_state}')
    dbgprint(lambda : f'chance_of_check: {chance_of_check}')
    dbgprint(lambda : f'max_check_count: {max_check_count}')
    dbgprint(lambda : f'max_count_per_state: {max_count_per_state}')
    dbgprint(lambda : f'max_count_companies: {max_count_companies}')
    dbgprint(lambda : f'max_check_count: {max_check_count}')

    progression_count = count_progression_items(options)

    dbgprint(lambda : f'progression_count.mandatory: {progression_count.mandatory}')
    dbgprint(lambda : f'progression_count.total(): {progression_count.total()}')

    all_states = list[str](options.states_available.value)
    available_dlcs = set[str](options.dlcs_available.value)
    dbgprint(lambda : f'all_states: {all_states}')

    starting_state = get_starting_state()
    dbgprint(lambda : f'starting_state: {get_starting_state()}')
    all_states.remove(get_starting_state())
    randomizer.shuffle(all_states)

    accepted_states: list[str] = [starting_state]
    rejected_states: list[str] = []

    for state in pop_iter(all_states):
        # Don't call for randomization if min check count isn't met or chance is guaranteed:
        if chance_of_state == 1 or randomizer.random() <= chance_of_state:
            dbgprint(lambda : f'added state: {state}')
            accepted_states.append(state)
            if max_state_count and len(accepted_states) >= max_state_count:
                dbgprint(lambda : f'max state count reached!')
                break
        else:
            dbgprint(lambda : f'skipped state: {state}')
            rejected_states.append(state)

    dbgprint(lambda : f'accepted_states (without min check check): {accepted_states}')

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

    available_checks_set = set[CheckInfo]()

    # Now populate the all_checks_set with potential checks from selected states
    for state in accepted_states:
        dbgprint(lambda : f'Adding checks from {state}:')
        dbgprint(lambda : f'Added {len(potential_checks_dict[state])} checks')
        available_checks_set |= potential_checks_dict[state]
        del potential_checks_dict[state]
        dbgprint(lambda : f'New all checks length: {len(available_checks_set)}')

    while rejected_states and len(available_checks_set) < progression_count.mandatory:
        dbgprint(lambda : f'Moved state {state} to accepted for check count.')
        state = rejected_states.pop()
        accepted_states.append(state)
        dbgprint(lambda : f'Adding checks from {state}:')
        dbgprint(lambda : f'Added {len(potential_checks_dict[state])} checks')
        available_checks_set |= potential_checks_dict[state]
        del potential_checks_dict[state]
        dbgprint(lambda : f'New all checks length: {len(available_checks_set)}')

    available_checks_list = list(available_checks_set)
    randomizer.shuffle(available_checks_list)

    dbgprint(lambda : f'length of all_checks_list: {len(available_checks_list)}')

    # And start tearing it down
    checks_to_remove: list[str] = []
    checks_to_keep: list[str] = []
    sum_checks = 0
    deleted_checks = 0
    reject_all = True

    for check in pop_iter(available_checks_list):
        reject: bool = False

        state = check.region.state if check.region else None
        if state:
            if max_count_per_state and total_checks[state] >= max_count_per_state:
                reject = True
                dbgprint(lambda : f'Removing check: {check} (max checks reached for {state})')
        else:
            if max_count_companies and total_checks[None] >= max_count_companies:
                dbgprint(lambda : f'Removing check: {check} (max companies reached)')
                reject = True

        if (not reject) and chance_of_check < 1 and randomizer.random() > chance_of_check:
            dbgprint(lambda : f'Removing check: {check} (chance failed)')
            reject = True

        if reject:
            # dbgprint(lambda : f'Removing check: {check}')
            checks_to_remove.append(f'{check}')
            deleted_checks += 1
            if progression_count.mandatory >= sum_checks + len(available_checks_list):
                dbgprint(lambda : f'Min check count reached! Accepting all other checks.')
                reject_all = False
                break
        else:
            dbgprint(lambda : f'Keeping check: {check}')
            checks_to_keep.append(f'{check}')
            sum_checks += 1
            total_checks[state] += 1
            if check.count_early:
                dbgprint(lambda : f'  (added to early list)')
                early_checks[state] += 1
            if max_check_count and sum_checks >= max_check_count:
                dbgprint(lambda : f'Max check count reached! Removing all other checks.')
                break

    if reject_all:
        for check in available_checks_list:
            checks_to_remove.append(f'{check}')
    else:
        for check in available_checks_list:
            checks_to_keep.append(f'{check}')
            sum_checks += 1
            total_checks[state] += 1
            if check.count_early:
                early_checks[state] += 1

    for state, state_set in potential_checks_dict.items():
        for check in state_set:
            if f'{check}' not in checks_to_keep and f'{check}' not in checks_to_remove:
                checks_to_remove.append(f'{check}')

    dbgprint(lambda : f'sum_checks: {sum_checks}')
    dbgprint(lambda : f'checks_to_remove: {checks_to_remove}')

    progression_to_remove = progression_count.total() - sum_checks
    dbgprint(lambda : f'progression_to_remove: {progression_to_remove}')

    if progression_to_remove > 0 and progression_count.levels > 0:
        dbgprint(lambda : f'Removing {progression_count.levels} levels')
        progression_to_remove -= progression_count.levels
    if progression_to_remove > 0:
        dbgprint(lambda : f'Still need to remove {progression_to_remove} progression items')
        if progression_count.tokens > 0:
            tokens_to_remove = min(progression_to_remove, progression_count.tokens)
            dbgprint(lambda : f'Removing {tokens_to_remove} tokens')
            tokens_to_keep = options.delivery_tokens_available.value - tokens_to_remove
            factor = options.delivery_tokens_required.value / options.delivery_tokens_available.value
            requirement_to_keep = max(1, floor(tokens_to_keep * factor))
            dbgprint(lambda : f'New tokens requirement: {requirement_to_keep} req. / {tokens_to_keep} avail.')
            options.delivery_tokens_available.value = tokens_to_keep
            options.delivery_tokens_required.value = requirement_to_keep
        elif progression_count.deliveries > 0:
            deliveries_to_remove = min(progression_to_remove, progression_count.deliveries)
            delivery_count_to_remove = deliveries_to_remove / progression_count.delivery_pieces
            dbgprint(lambda : f'Removing {delivery_count_to_remove} deliveries')
            delivery_count_to_keep = options.secret_deliveries_available.value - delivery_count_to_remove
            factor = options.secret_deliveries_required.value / options.secret_deliveries_available.value
            requirement_to_keep = max(1, floor(delivery_count_to_keep * factor))
            dbgprint(lambda : f'New deliveries requirement: {requirement_to_keep} req. / {delivery_count_to_keep} avail.')
            options.secret_deliveries_available.value = delivery_count_to_keep
            options.secret_deliveries_required.value = requirement_to_keep

    return checks_to_remove
