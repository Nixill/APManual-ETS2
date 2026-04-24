from typing import Any

from worlds.AutoWorld import World

from ..Helpers import remove_specific_item
from ..Items import ManualItem, item_name_to_item

from .ChecksReduction import get_additional_state_keys
from .Func import snake_case
from .Options import starting_state
from .OptionDefs import KeyItemChoice

early_item_count: int = 0

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
