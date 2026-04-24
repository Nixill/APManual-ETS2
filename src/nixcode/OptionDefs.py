# Option definitions
from typing import Any, Type
from worlds.AutoWorld import World
from Options import Option, FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange, OptionGroup, PerGameCommonOptions, OptionSet
from .Func import snake_case
from .CsvData import state_list, dlc_list, truck_makes_list, company_list, photo_trophies_dict, viewpoints_dict, city_dict, dlc_aliases_dict

class StartingLocation(Choice):
    """
    Which country should the player start in?

    If this is set to a country that's not loaded in a DLC, it will be reset to a random country.

    If the country selected has its checks disabled, those will be re-enabled.
    """
    display_name = 'Starting Location'
    rich_text_doc = True

for i, s in enumerate(state_list):
    setattr(StartingLocation, f'option_{snake_case(s)}', i)

StartingLocation.default = StartingLocation.option_germany

class _DeliveryTokenOption(Range):
    rich_text_doc = True
    range_start = 1
    range_end = 100

class DeliveryTokensAvailable(_DeliveryTokenOption):
    """
    Number of delivery tokens available in the multiworld item pool.

    If the number of items exceeds the number of locations, this value may be reduced to
    accommodate. If so, `delivery_tokens_required` will be reduced proportionally.
    """
    display_name = 'Delivery Tokens Available'
    default = 25

class DeliveryTokensRequired(_DeliveryTokenOption):
    """
    Number of delivery tokens required to click goal. Must not exceed `delivery_tokens_available`,
    and this value will automatically be reduced to that value if needed.

    If the number of items exceeds the number of locations, `delivery_tokens_available` may be
    reduced to accommodate. If so, this value will be reduced proportionally.
    """
    display_name = 'Delivery Tokens Required'
    default = 20

class _SecretDeliveryCountOption(Range):
    rich_text_doc = True
    range_start = 1
    range_end = 20

class SecretDeliveriesAvailable(_SecretDeliveryCountOption):
    """
    Number of Secret Deliveries available to perform.

    If the number of items exceeds the number of locations, this value may be reduced to
    accommodate. If so, `secret_deliveries_required` will be reduced proportionally.
    `secret_delivery_instruction_parts` will not be reduced.
    """
    display_name = 'Secret Deliveries Available'
    default = 10

class SecretDeliveriesRequired(_SecretDeliveryCountOption):
    """
    Number of Secret Deliveries that must be performed to win. Must not exceed
    `secret_deliveries_available`, and this option will automatically be reduced to that option if
    necessary.

    If the number of items exceeds the number of locations, `secret_deliveries_available` may be
    reduced to accommodate. If so, this value will be reduced proportionally.
    `secret_delivery_instruction_parts` will not be reduced.
    """
    display_name = 'Secret Deliveries Required'
    default = 8

class SecretDeliveryInstructionParts(Range):
    """
    Number of separate parts to the instructions of each Secret Delivery.

    Not all parts must be found in order to perform a Secret Delivery; once the instructions are
    readable, the delivery may be performed.
    """
    display_name = 'Secret Delivery Instruction Parts'
    rich_text_doc = True
    range_start = 1
    range_end = 5
    default = 2

class DLCsAvailableOption(OptionSet):
    """
    Which DLCs are enabled?

    A disabled DLC does not contribute any checks or items to the multiworld. However, companies
    specifically may be present in multiple DLCs and may be checks if any such DLC is enabled.

    Valid values are any DLC name or "All".

    "Base Game" is implied and cannot be disabled.
    """
    display_name = 'Available DLCs'
    rich_text_doc = True
    valid_keys = {*dlc_aliases_dict.values(), 'all'} - {'base game', 'base'}
    valid_keys_casefold = True
    default = set()

class StatesAvailableOption(OptionSet):
    """
    Which countries are enabled?

    A disabled country does not contribute any checks to the multiworld. It will still have a
    country key that you must find before driving in that country. Companies in the country may be
    present if they have locations in other countries.

    Valid values are any country's name, any DLC's name (or "Base Game") for all the countries in
    that DLC, or "All" for everything. (Note that for countries split across multiple DLCs,
    specifying either DLC name includes the whole country.)

    If this is empty, "All" is implied.
    """
    display_name = 'Available Countries'
    rich_text_doc = True
    valid_keys = state_list + dlc_list + ['All']
    valid_keys_casefold = True
    default = set()

class EnableCityChecks(DefaultOnToggle):
    """
    Whether or not cities are checks. If so, the check is performed by driving into the city; the
    check may be clicked as soon as the "(City Name) Discovered" popup appears.

    If all check types are disabled, Cities will be enabled.
    """
    display_name = 'Enable City Checks'
    rich_text_doc = True

class EnableCompanyChecks(Toggle):
    """
    Whether or not companies are checks. If so, the player chooses from one of the following:
    - A check is performed by driving onto any of that company's depos. Click it when the depot on
      the map turns yellow.
    - A check is performed by performing a delivery to that company. Click it when the results
      screen appears.
    - A check is performed by performing a delivery to or from that company. Click it when the
      results screen appears.
    """
    display_name = 'Enable Company Checks'
    rich_text_doc = True

class KeyItemChoice(Choice):
    rich_text_doc = True
    option_find_item = 1
    option_find_item_early = 2
    default = option_start_with_item = 3

class _KeyItemChoiceWithDisable(KeyItemChoice):
    rich_text_doc = True
    default = option_disabled = 0

class EnablePhotosanity(_KeyItemChoiceWithDisable):
    """
    Whether or not photo trophies are checks. If so, the check is performed when the picture of the
    named monument is taken. The Camera item is required before you can take photos; it can be part
    of the multiworld item pool or part of the player's starting inventory.
    """
    display_name = 'Enable Photosanity'

class EnableViewpointsanity(_KeyItemChoiceWithDisable):
    """
    Whether or not viewpoints are checks. If so, the check is performed when you've begun watching
    the viewpoint cutscene. The Television item is required before you can watch viewpoints; it can
    be part of the multiworld item pool or part of the player's starting inventory.
    """
    display_name = 'Enable Viewpointsanity'

class PlayerLevelChecks(NamedRange):
    """
    How many player levels should be checks? All levels from 1 to the specified number will be
    included. The check may be clicked when the level shown on the left side of the bar is at least
    the level being clicked.

    If this is set to disabled, no level checks apply. If the goal is set to Player Level Reached,
    this option must have a value of at least 5, and will be incremented if necessary.
    """
    rich_text_doc = True
    default = range_start = 0
    range_end = 36
    special_range_names = {
        'disabled': 0,
        'recommended': 15,
        'all': 36
    }

class SkillItemsOnLevels(Toggle):
    """
    Should player skills be placed on level-up checks?

    If this option is enabled, the skills to which player skill points may be assigned are
    converted to items and placed on locations created to receive them.

    If this option is enabled AND skill_items_scattered is disabled, these locations are created
    for all 36 levels, regardless of the value of player_level_checks (even if it's 0/disabled).
    What the player does with them after the final player_level_check is up to the player, with the
    following possibilities:
    - Ignore remaining skills and skill points. They cannot be spent in any fashion.
    - Reveal remaining skills when attaining the respective levels.
    - Ignore remaining skill level locations, allow free assignment after player_level_checks
      levels.
    """
    display_name = 'Skills on Levels'

class SkillItemsScattered(Toggle):
    """
    Should player skill points be scattered in the multiworld item pool?

    If this option is enabled, the skills to which player skill points may be assigned are
    converted to items and spread throughout the multiworld item pool.

    If this option AND skill_items_on_levels are enabled, skill items are placed on level up
    checks first, and then the remainder are spread throughout the multiworld item pool.
    """
    display_name = ''

class BankLoanApprovalItem(KeyItemChoice):
    """
    A Bank Loan Approval is required before obtaining any loans from the bank. Should it be part
    of the player's starting inventory or the multiworld item pool?
    """
    display_name = 'Bank Loan Approval'

class TruckContractItemBrand(Choice):
    """
    A Truck Contract is required before buying any trucks. There is an individual Contract per
    truck brand.

    The brand selected below will be part of the player's starting inventory (unless a different
    option is selected for truck_contract_brand_item_location). All others will be part of the
    multiworld item pool (unless a different option is selected for truck_contract_off_brand_item_location).
    """
    display_name = 'Truck Contract Brand'
    option_none = 0
    default = option_all = 1

for i, m in enumerate(truck_makes_list, 2):
    setattr(TruckContractItemBrand, f'option_{snake_case(m)}', i)

class TruckContractBrandItemLocation(KeyItemChoice):
    """
    Whether the Truck Contract for the make selected in truck_contract_item_brand should start in
    the player's inventory or the multiworld item pool.
    """
    display_name = 'Truck Contract On-Brand Location'

class TruckContractOffBrandItemLocation(KeyItemChoice):
    """
    Whether all other Truck Contracts, besides the make selected in truck_contract_item_brand,
    should start in the player's inventory or the multiworld item pool.

    It is not recommended that this setting be set more leniently than truck_contract_brand_item_location.
    Nonetheless, it is allowed.
    """
    display_name = 'Truck Contract Off-Brand Location'

class TrailerContractItem(KeyItemChoice):
    """
    A Trailer Contract is required before buying any trailers. Should it be part of the player's
    starting inventory or the multiworld item pool?
    """
    display_name = 'Trailer Contract Item'

class QuickTravelTicketItem(_KeyItemChoiceWithDisable):
    """
    A Quick Travel Ticket is required before quick traveling to any undiscovered city (through its
    DLC opening or through Convoy). Should it be part of the player's starting inventory or
    multiworld item pool?

    It can also be disabled outright, such that quick traveling is never in logic, so long as all
    the enabled DLCs are connected to each other and to the base game. Otherwise, this will be set
    to in_starting_inventory.
    """
    display_name = 'Quick Travel Ticket Item'

class _PercentOption(Range):
    range_start = 1
    range_end = 100
    default = 100

class ChecksPercentOfStateCount(_PercentOption):
    """
    What percentage of available countries should contain checks? Note that the other countries
    will still have keys, which must be obtained before driving in those countries.
    """
    display_name = 'Percentage of Countries with Checks'

class ChecksMaxStateCount(NamedRange):
    """
    What is the maximum number of countries that should contain checks? Note that the other
    countries will still have keys, which must be obtained before driving in those countries.

    The default for this option is the number of countries that currently exist (with all DLC).
    Increasing this value has no effect besides future-proofing your yaml.
    """
    display_name = 'Maximum Number of Countries with Checks'
    range_start = 1
    range_end = 100
    special_range_names = {'unlimited': 0}
    default = len(state_list)

class ChecksPercent(_PercentOption):
    """
    What percentage of all checks should be enabled?
    """
    display_name = 'Percentage of Checks'

class ChecksMaxPerStateCount(NamedRange):
    """
    What is the maximum number of checks that should appear per country? Companies are considered
    country-less and are not affected by this option.
    """
    display_name = 'Maximum Checks per Country'
    range_start = 1
    range_end = 1000
    special_range_names = {'unlimited': 0}
    default = 1000

class CompanyChecksCount(NamedRange):
    """
    What is the number of companies that should appear as checks?

    The default for this option is the number of companies that currently exist (with all DLC).
    Increasing this value has no effect besides future-proofing your yaml.
    """
    display_name = 'Maximum Company Checks'
    range_start = 1
    range_end = 1000
    special_range_names = {'unlimited': 0}
    default = len(company_list)

class MaxChecksCount(NamedRange):
    """
    What is the maximum number of checks that should be included across all categories?

    The default for this option is the number of checks that currently exist (with all DLC and all
    types enabled). Increasing this value has no effect besides future-proofing your yaml.
    """
    display_name = 'Maximum Checks Count'
    range_start = 1
    range_end = 10000
    special_range_names = {'unlimited': 0}
    default = len(company_list) + len(city_dict) + len(photo_trophies_dict) + len(viewpoints_dict) + 36

def define_options(options: dict[str, Type[Option[Any]]]) -> dict[str, Type[Option[Any]]]:
    options["starting_location"] = StartingLocation
    options["delivery_tokens_available"] = DeliveryTokensAvailable
    options["delivery_tokens_required"] = DeliveryTokensRequired
    options["secret_deliveries_available"] = SecretDeliveriesAvailable
    options["secret_deliveries_required"] = SecretDeliveriesRequired
    options["secret_delivery_instruction_parts"] = SecretDeliveryInstructionParts
    options["dlcs_available"] = DLCsAvailableOption
    options["states_available"] = StatesAvailableOption
    options["enable_city_checks"] = EnableCityChecks
    options["enable_company_checks"] = EnableCompanyChecks
    options["enable_photosanity"] = EnablePhotosanity
    options["enable_viewpointsanity"] = EnableViewpointsanity
    options["player_level_checks"] = PlayerLevelChecks
    options["skill_items_on_levels"] = SkillItemsOnLevels
    options["skill_items_scattered"] = SkillItemsScattered
    options["bank_loan_approval_item"] = BankLoanApprovalItem
    options["truck_contract_item_brand"] = TruckContractItemBrand
    options["truck_contract_brand_item_location"] = TruckContractBrandItemLocation
    options["truck_contract_off_brand_item_location"] = TruckContractOffBrandItemLocation
    options["trailer_contract_item"] = TrailerContractItem
    options["quick_travel_ticket_item"] = QuickTravelTicketItem
    options["checks_percent_of_state_count"] = ChecksPercentOfStateCount
    options["checks_max_state_count"] = ChecksMaxStateCount
    options["checks_percent"] = ChecksPercent
    options["checks_max_per_state_count"] = ChecksMaxPerStateCount
    options["company_checks_count"] = CompanyChecksCount
    options["max_checks_count"] = MaxChecksCount
    return options

def group_options(groups: dict[str, list[Type[Option[Any]]]]) -> dict[str, list[Type[Option[Any]]]]:
    groups['Delivery Tokens'] = [
        DeliveryTokensAvailable,
        DeliveryTokensRequired
    ]

    groups['Secret Deliveries'] = [
        SecretDeliveriesAvailable,
        SecretDeliveriesRequired,
        SecretDeliveryInstructionParts
    ]

    groups['Check Types Available'] = [
        EnableCityChecks,
        EnableCompanyChecks,
        EnablePhotosanity,
        EnableViewpointsanity
    ]

    groups['Level and Skill Checks'] = [
        PlayerLevelChecks,
        SkillItemsOnLevels,
        SkillItemsScattered
    ]

    groups['Items Available'] = [
        BankLoanApprovalItem,
        TruckContractItemBrand,
        TruckContractBrandItemLocation,
        TruckContractOffBrandItemLocation,
        TrailerContractItem,
        QuickTravelTicketItem
    ]

    groups['Checks Reduction'] = [
        ChecksPercentOfStateCount,
        ChecksMaxStateCount,
        ChecksPercent,
        ChecksMaxPerStateCount,
        CompanyChecksCount,
        MaxChecksCount
    ]
