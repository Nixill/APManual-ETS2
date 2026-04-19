# Option definitions
from typing import Any
from worlds.AutoWorld import World
from Options import Option, FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange, OptionGroup, PerGameCommonOptions, OptionSet
from .Func import snake_case
from .CsvData import state_list, dlc_list

class StartingLocation(Choice):
    """
    Which country should the player start in?

    If this is set to a country that's not loaded in a DLC, it will be reset to a random country.

    If the country selected has its checks disabled, those will be re-enabled.
    """
    display_name = 'Difficulty'
    rich_text_doc = True

for i, s in zip(range(len(state_list)), state_list):
    setattr(StartingLocation, f'option_{snake_case(s)}', )

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
    valid_keys = dlc_list + ['All'] - ['Base Game']
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

class _KeyItemChoice(Choice):
    rich_text_doc = True
    option_find_item = 1
    option_find_item_early = 2
    default = option_start_with_item = 3

class _ItemRequiringSanity(_KeyItemChoice):
    rich_text_doc = True
    default = option_disabled = 0

class EnablePhotosanity(_ItemRequiringSanity):
    """
    Whether or not photo trophies are checks. If so, the check is performed when the picture of the
    named monument is taken. The Camera item is required before you can take photos; it can be part
    of the multiworld item pool or part of the player's starting inventory.
    """
    display_name = 'Enable Photosanity'

class EnableViewpointsanity(_ItemRequiringSanity):
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

class SkillCheckScattering(Choice):
    """
    How should player skill points be handled?
    - **`disabled`**: Do not scatter skill categories. When the player levels up, they have free
      rein to decide where to spend their skill points.
    - **`condensed_limited`**: Add an extra location to every level-up check, which contains a
      random skill category. The player must spend the skill point of that level on that category.
      Once player level checks run out, the player has free rein to decide where to spend remaining
      skill points. (If `player_level_checks` = 0, this functions identically to `disabled`.)
    - **`condensed_spread`**: Add an extra location to every level-up check, which contains a
      random skill category. The remaining skill categories are spread throughout the multiworld.
      Upon leveling up, the player must choose an available skill category, if any, to spend their
      skill point on. If none are available, the player must wait to receive one before spending
      it. (If `player_level_checks` = 0, this functions identically to `spread`.)
    - **`spread`**: Scatter skill points throughout the multiworld. Upon leveling up, the player
      must choose an available skill category, if any, to spend their skill point on. If none are
      available, the player must wait to receive one before spending it.
    """
    rich_text_doc = True
    default = option_disabled = 0
    option_condensed_limited = 1
    option_condensed_spread = 2
    option_spread = 3

class BankLoanApprovalItem(_KeyItemChoice):
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

