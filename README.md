# Euro Truck Simulator 2
Manual APworld for use with Euro Truck Simulator 2, for use with the [Archipelago Multiworld Randomizer](https://archipelago.gg/) and its [Manual Project](https://github.com/ManualForArchipelago/Manual).

# What you need
To play the Euro Truck Simulator 2 archipelago, you will need:
1. [Euro Truck Simulator 2](https://store.steampowered.com/app/227300). DLCs are not required, but may be used.
2. The latest [Euro Truck Simulator 2 APWorld](https://github.com/Nixill/APManual-ETS2/releases/latest) and the latest [Manual Client](https://github.com/ManualForArchipelago/Manual/releases/latest).
3. Start a new save file. Don't select the starting city just yet.
4. If you're using the Secret Deliveries win condition, you should also get [APManualViewer](https://github.com/Nixill/APManualReader/releases/latest).

# Setup
Download and install the apworld to your Archipelago launcher. Either generate YAML options and edit by hand, or use the options editor. [Options are explained below.](#options) Then generate the world, and connect to it with the Manual Client.

You **must** edit the options if you wish to play with DLC territories. Under default settings, only the base game is included.

If using the Secret Deliveries win condition, you'll also need to download this game's patch file. For rooms hosted on archipelago.gg, there will be a "Download patch file..." option on your player's slot row. For rooms hosted locally, it will be in the generated zip. Open either the patch file or the generated zip in [APManualViewer](https://github.com/Nixill/APManualReader/releases/latest), select your player slot name if necessary, and you will see the listing of secret delivery files. **DO NOT LOOK AT THEM YET!**

Create a new save file in Euro Truck Simulator. If using a predetermined starting country (under default options, Germany), 

When you start playing, look at your inventory. You will start with at least one country's Key, and must start your save file in a country for which you have a key.

# Playing
Depending on which checks you have enabled in the options, you may perform (claim) them in the following ways:

1. CITY checks: You may perform the check when the "[City name] discovered" popup appears. The starting city, if it is a check, may be claimed immediately.
2. COMPANY checks: It is recommended that you claim a check when you complete a delivery to or from the company in question. *(You may also use "drive onto the company's depot" as the check trigger.)*
3. PHOTO TROPHY checks: You may not perform these checks without the **Camera** item. Once you have it, you perform the check by lining up the photo trophy so that its name is visible in the photo mode. Taking the picture is not necessary.
4. VIEWPOINT checks: You may not perform these checks without the **TV** item. Once you have it, you perform the check by beginning to watch the viewpoint cutscene. You may mark the check during the cutscene, but don't skip the cutscene!
5. PLAYER LEVEL checks: You may perform this check as soon as the number on the left side of the experience bar is at least the number in question. (If a level isn't in logic at the time it's achieved, you may perform the check once it is.)

Without receiving items, you may not perform specific actions. Specifically,
| You may not...                                        | ... without the...                          |
| :---------------------------------------------------- | :------------------------------------------ |
| Drive in another country                              | (that country) Key                          |
| Purchase a truck, new or used                         | (that truck brand) Trucks Purchase Contract |
| Read the instructions of a secret delivery            | Piece of Secret Delivery #(x) Instructions  |
| Spend your skill points on level up                   | Skill Point - (details)                     |
| Use a ferry (the Channel Tunnel train does not count) | Ferry Ticket                                |
| Take photos for Photo Trophy checks                   | Camera                                      |
| Watch viewpoints for Viewpoint checks                 | TV                                          |
| Take out a loan from the bank                         | Bank Loan Approval                          |
| Purchase a trailer, new or used                       | Trailer Contract                            |
| Quick Travel to an undiscovered city                  | Quick Travel Ticket                         |

# Victory
There are three goal conditions:

## Delivery Tokens Collected (default)
"Delivery Token"s are items scattered throughout the multiworld. A certain number exist, and a certain subset of them is required to win. Once you've collected the required number, you may simply click the victory button to goal.

## Secret Deliveries Completed
"Piece of Secret Delivery #(x) Instructions"es are items scattered throughout the multiworld. A certain number of secret deliveries exist. Once you've collected all the pieces for a given delivery, you may open the file corresponding to that delivery to view its instructions. After that, drive with a trailer from any depot in the source city to any depot in the destination city - without quick traveling or taking another job - to mark off the secret delivery as completed. Once you've completed the required number, you may click the victory button to goal.

## Player Level Checks Completed
To achieve this victory condition, you must simply complete every "Player Level Up" check for which an "External" button exists, then click the victory button to goal.

# Death Link
This version of the Euro Truck Simulator 2 APWorld supports Death Link. If you opt in:
- When **receiving** a deathlink, roll a die. If you don't roll a 1, skip the rest of these instructions. Open the menu to get your truck towed to view the nearest service station. You may then choose to either get towed there (costing you money and additional in-game time) or drive there (costing you real-life time). *(If you do not have a die, you may track amnesty yourself, or just act as if you always rolled a 1.)*
- When you complete a delivery with at least 5% cargo damage or late, or you experience an engine malfunction, **send** a deathlink. Then follow the instructions above as if you received one and rolled a 1.

# Options
The options of this APWorld are documented [here](/docs/Options.md).

# Credits
This was heavily inspired by [dopinpt's version](https://github.com/dopinpt/ETS2Manual). I was originally going to just pull request that version, but ended up just starting over instead. I've kept the default settings of this Manual almost identical to theirs, with the only change being the number of delivery tokens that exist in the multiworld (25 instead of 20, though you still need 20 to win).
