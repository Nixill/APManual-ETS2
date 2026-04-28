(Note: The options are not grouped in the yaml or options creator because option groups are broken. The intended groups are used in this documentation. You may download a grouped YAML template in the releases.)

# Starting location
## `starting_location`
What country do you start in? You may have AP choose randomly from multiple countries, or add `random` to completely randomize.

Note that if a country you don't have the DLC for is selected, it will be re-rolled to a country within your selected DLCs.

Also note that if you roll a country for which checks aren't enabled, that country's checks will be enabled.

If the selected country doesn't have enough checks to accommodate all needed early items, additional adjacent countries will be added at random.

# Delivery tokens
## `delivery_tokens_available`
How many delivery tokens are available across the multiworld?

## `delivery_tokens_required`
How many delivery tokens must you collect to achieve your goal?

This cannot exceed `delivery_tokens_available`; this option's value will be reduced if necessary.

# Secret Deliveries
## `secret_deliveries_available`
How many secret deliveries are there available to be made?

## `secret_deliveries_required`
How many secret deliveries must be performed to achieve your goal?

This cannot exceed `secret_deliveries_available`; this option's value will be reduced if necessary.

## `secret_delivery_instruction_parts`
Number of separate parts to the instructions of each Secret Delivery.

All parts must be found before reading that delivery.

## `secret_delivery_country_border_limit`
Maximum number of country borders a secret delivery may cross.

Note that this restricts the route with the *fewest possible* crossings, even if the fastest path takes more. For example, Russia is reachable from Portugal in five border crossings with ferries (Portugal → Spain → France → Germany → ferry to Finland → Russia) but a land route with nine border crossings is faster (Portugal → Spain → France → Germany → Poland → Kaliningrad → Lithuania → Latvia → Estonia → Russia).

Due to Luxembourg, Kosovo, and Kaliningrad, this must be at least one.

# DLC availability
## `dlcs_available`
Which DLCs are available for the playthrough?

A disabled DLC doesn't contribute any checks or items to the multiworld. However, companies are checked separately as they can be present in multiple DLCs; a company that is in any enabled DLC may be a check.

Valid values are any of the following DLCs. Names are case insensitive. You may prefix the name with a `<` to also include any DLC above it in the list, or use "All" for all of the following DLCs:

| DLC                   | Aliases                                       |
| :-------------------- | :-------------------------------------------- |
| Going East!           | "east" or "going east"                        |
| Scandinavia           | "scandic"                                     |
| Vive la France !      | "vive la france", "vive la france!", "france" |
| Italia                | "italy"                                       |
| Beyond the Baltic Sea | "baltic sea"                                  |
| Road to the Black Sea | "black sea"                                   |
| Iberia                |                                               |
| West Balkans          | "balkan"                                      |
| Greece                |                                               |
| Nordic Horizons       | "nordic"                                      |

Additionally, the following DLCs are not included in "all" because they're less well known to actually contain map expansions, but you can use "really all" if you have them:

| DLC                     | Aliases      |
| :---------------------- | :----------- |
| Krone Trailer Pack      | "krone"      |
| Feldbinder Trailer Pack | "feldbinder" |

# `states_available`
("states" as in nation-states, in Euro Truck's case)

A disabled country does not contribute any locations to the multiworld. However, its Key will still exist, and you still need to find it before driving in that country. Companies will be present as checks if they have locations in any enabled country.

Valid values are any country's name (as below), any DLC's name as above (or "Base Game") to include all countries in that DLC, or "All" for everything. Note that for countries split across multiple DLCs, specifying any of them includes the whole country.

If this list is empty, "All" is implied.

| Country names          |
| :--------------------- |
| Albania                |
| Austria                |
| Belgium                |
| Bosnia and Herzegovina |
| Bulgaria               |
| Croatia                |
| Czech Republic         |
| Denmark                |
| Estonia                |
| Finland                |
| France                 |
| Germany                |
| Greece                 |
| Hungary                |
| Italy                  |
| Kaliningrad            |
| Kosovo                 |
| Latvia                 |
| Lithuania              |
| Luxembourg             |
| Montenegro             |
| Netherlands            |
| North Macedonia        |
| Norway                 |
| Poland                 |
| Portugal               |
| Romania                |
| Russia                 |
| Serbia                 |
| Slovakia               |
| Slovenia               |
| Spain                  |
| Sweden                 |
| Switzerland            |
| Turkiye                |
| United Kingdom         |

# Checks settings
## `enable_citysanity`
Whether or not cities are checks.

## `enable_companysanity`
Whether or not companies are checks.

## `enable_photosanity`
Whether or not photo trophies are checks.

Photo trophy checks require the Camera item to be performed, so the values of this setting are:
- **`find_item`**: Enable photosanity, and place the Camera somewhere in the multiworld. Good luck finding it!
- **`find_item_with_hint`**: Enable photosanity, and place the Camera somewhere in the multiworld. Start the game with a hint for its location.
- **`find_item_early`**: Enable photosanity, and place the Camera somewhere in an immediately accessible check in Euro Truck Simulator 2. Shouldn't take too long to find!
- **`find_item_early_with_hint`**: Enable photosanity, and place the Camera somewhere in an immediately accessible check in Euro Truck Simulator 2. Start the game with a hint for its location.
- **`start_with_item`**: Enable photosanity, and place the Camera in your starting inventory. You may perform photosanity checks immediately.
- **`disabled`**: Disable photosanity. Do not place the Camera item anywhere.

## `enable_viewpointsanity`
Whether or not viewpoints are checks.

Viewpoint checks require the TV item to be performed, so the values of this setting are the same as for [photosanity](#enable_photosanity).

# Player Level Checks
## `player_level_checks`
How many player levels should be checks? All levels from 1 to the specified number will be included. This number controls External checks that can have any multiworld item placed on them.

If the goal is set to "Player Level Reached", this number must be at least 5, and will be incremented if necessary.

## `skill_items_on_levels` and `skill_items_scattered`
Whether the 36 player skills should be items to find.

If both options are disabled, you'll start with the skill items.

If `skill_items_on_levels` is enabled and `skill_items_scattered` is disabled, the skills will be randomly assigned to player levels 1-36, even if `player_level_checks` is less than 36.

If `skill_items_scattered` is enabled and `skill_items_on_levels` is disabled, the skills will be spread throughout the multiworld item pool.

If both options are enabled, the skills will be randomly assigned to player levels 1 through `player_level_checks`, and the remaining skills spread throughout the multiworld item pool (including, possibly, on "External" player level checks).

## `player_level_logical_lock_factor`
This option attempts to prevent early grinding of player levels by keeping player levels out of logic until a certain number of territories are reachable. Higher numbers mean later levels require more map (where 100 means the entire map must be accessible before the final level in `player_level_checks` is accessible). Earlier levels require proportionally less map, and level 1 is immediately in logic.

If you level up faster than you unlock territory for level logic, you may cheat the level checks (either using `/send` or by pressing F1 to disable the protection against accidental clicks) or simply wait for the level to be in logic and then clear it immediately.

When using `skill_items_on_checks` and a `player_level_checks` that is less than 36, all levels beyond `player_level_checks` are accessible at the same time as the final level of `player_level_checks`.

# Item Granting Options
## `ferry_ticket_item`, `bank_loan_approval_item`, `trailer_contract_item`, and `quick_travel_item`
<span id="ferry_ticket_item"></span>

These items are required before performing the associated actions. These options indicate where the items are found, with the following values:
- **`find_item`**: Place the item somewhere in the multiworld. Good luck finding it!
- **`find_item_with_hint`**: Place the item somewhere in the multiworld. Start the game with a hint for its location.
- **`find_item_early`**: Place the item somewhere in an immediately accessible check in Euro Truck Simulator 2. Shouldn't take too long to find!
- **`find_item_early_with_hint`**: Place the item somewhere in an immediately accessible check in Euro Truck Simulator 2. Start the game with a hint for its location.
- **`start_with_item`**: Place the item in your starting inventory. You may use it immediately.
- **`disabled` (Quick Travel Ticket only)**: Do not include the item whatsoever. You cannot use it at any point.

Note that the requirement to have the item before using it cannot be disabled. However, if you want to remove the requirement to **find** the item, you may simply use the `start_with_item` option.

The items are needed for:
- The **Ferry Ticket** is needed to use any ferries. If you don't start with it, you may not start your game on an island (except for the mainland United Kingdom). The Channel Tunnel does not count as a ferry, so you may always travel between the UK and France (once you have both Keys).
- The **Bank Loan Approval** is needed before you can obtain any loans from the bank.
- The **Trailer Contract** is needed to purchase any trailers, whether new or used.
- The **Quick Travel Ticket** is needed before you may quick travel to an undiscovered city. If enabled, it counts as a logical connection to new countries. It is ***not*** needed to quick travel to any previously discovered city, or to be towed to a service station.

## `truck_contract_item_brand`, `truck_contract_brand_item_location`, and `truck_contract_off_brand_item_location`
A **(Brand) Trucks Purchase Contract** is needed before you may buy any trucks, new or used, of that brand. The `truck_contract_item_brand` option selects which brand of truck contract is set by the `truck_contract_brand_item_location` option. All other brands are instead set by the `truck_contract_off_brand_item_location` option.

The latter two options have the same meaning as in the section above.

# Checks Reduction Options
The options here are used to reduce the number of checks available for a reduction in overwhelm. These options are evaluated in this order - for example, with `checks_percent_of_state_count`, 50% of countries get removed, then if there's still more than `checks_max_state_count`, more are removed until the maximum is satisfied.

## `checks_percent_of_state_count`
What percentage of available countries should contain checks? The countries eliminated by this option will still have keys that you must acquire before driving in them.

## `checks_max_state_count`
How many countries should contain checks? The countries eliminated by this option will still have keys that you must acquire before driving in them.

## `checks_percent`
What percentage of all checks should be available?

## `checks_max_per_state_count`
How many checks should be available in each country? This doesn't count companies or player levels.

## `company_checks_count`
How many company checks should be available?

## `max_checks_count`
How many checks should be available total? This includes companies, but not player levels.

# Other options
## `goal`
Goals are described on the [main readme](../README.md#victory).

## `death_link`
Death Link is described on the [main readme](../README.md#death-link).
