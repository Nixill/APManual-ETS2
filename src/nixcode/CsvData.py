from dataclasses import dataclass
from collections import defaultdict
from warnings import deprecated

from .Func import snake_case
from ..Helpers import load_data_csv

#region DLCs
def get_dlc(name: str) -> str:
    return name or 'Base Game'

def dlc_of(line: dict[str, str], key: str = 'DLC') -> str:
    return line[key] or 'Base Game'

dlc_list: list[str] = [dlc_of(line) for line in load_data_csv('csv', 'dlcs.csv')]
#endregion

#region Regions
@dataclass(frozen=True)
class Region:
    state: str
    dlc: str

def region_of(line: dict[str, str], state_key: str = 'State', dlc_key: str = 'DLC'):
    return Region(line[state_key], line[dlc_key])

_region_list_csv: list[dict[str, str]] = load_data_csv('csv', 'regions.csv')

region_list: list[Region] = [Region(line['State'], dlc_of(line)) for line in _region_list_csv]
state_dlcs_dict: dict[str, list[str]] = {}
dlc_states_dict: dict[str, list[str]] = {}

for r in region_list:
    state_dlcs_dict[r.state].append(r.dlc)
    dlc_states_dict[r.dlc].append(r.state)
#endregion

@dataclass(frozen=True)
class CheckLocation:
    check_name: str
    region: Region
    ferry_required: bool

    def rename(self, new_name: str):
        return CheckLocation(new_name, self.region, self.ferry_required)

#region Cities
city_dict: dict[str, CheckLocation] = {
    line['Name']: CheckLocation(line['Name'],
                                region_of(line),
                                bool(line['FerryRequired']))
    for line in load_data_csv('csv', 'cities.csv')}
#endregion

#region City Aliases
city_aliases_dict: dict[str, str] = {line['LocalName']: line['City'] for line in load_data_csv('csv', 'city-aliases.csv')}

def get_city(name: str) -> CheckLocation:
    if name in city_dict:
        return city_dict[name]
    if name in city_aliases_dict:
        return city_dict[city_aliases_dict[name]]
    raise KeyError()
#endregion

#region Companies
company_list: list[str] = [line['Company'] for line in load_data_csv('csv', 'companies.csv')]
#endregion

#region Company Locations
company_locations_dict: defaultdict[str, list[CheckLocation]] = defaultdict(list)

for line in load_data_csv('csv', 'company-locations.csv'):
    company_locations_dict[line['Company']].append(CheckLocation(line['Company'],
                                                                 region_of(line),
                                                                 bool(line['FerryRequired'])))
#endregion

#region Connections
connections_dict: defaultdict[Region, dict[Region, bool]] = defaultdict(dict)

for line in load_data_csv('csv', 'connections.csv'):
    left_region = region_of(line, 'Left', 'LeftDLC')
    right_region = region_of(line, 'Right', 'RightDLC')
    ferry_required = bool(line['FerryRequired'])
    connections_dict[left_region][right_region] = ferry_required
    connections_dict[right_region][left_region] = ferry_required

land_connections_dict = {key: {k for k, v in value.items() if not v} for key, value in connections_dict.items()}
ferry_connections_dict = {key: {k for k, v in value.items() if v} for key, value in connections_dict.items()}
#endregion

#region DLC Aliases
dlc_aliases_dict: dict[str, str] = {dlc.lower(): dlc for dlc in dlc_list} \
    + {line['Alias']: dlc_of(line) for line in load_data_csv('csv', 'dlc-aliases.csv')}
#endregion

#region DLC Connections
dlc_connections: defaultdict[str, list[str]] = defaultdict(list)

_dlc_connections_csv: list[dict[str, str]] = load_data_csv('csv', 'dlc-connections.csv')

for line in _dlc_connections_csv:
    left_dlc = dlc_of(line, 'DLC1')
    right_dlc = dlc_of(line, 'DLC2')

    dlc_connections[left_dlc].append(right_dlc)
    dlc_connections[right_dlc].append(left_dlc)
#endregion

#region Game Info
game_info_dict: dict[str, str] = {line['Key']: line['Value'] for line in load_data_csv('csv', 'game-info.csv')}

class GameInfo:
    name: str = game_info_dict['game']
    creator: str = game_info_dict['creator']
    filler_item_name: str = game_info_dict['filler_item']
#endregion

#region Photo Trophies
photo_trophies_dict: dict[str, CheckLocation] = {
    line['Trophy']: CheckLocation(line['Trophy'],
                                  region_of(line),
                                  line['FerryRequired'])
    for line in load_data_csv('csv', 'photo-trophies.csv')}
#endregion

#region Quick Travel
quick_travel_list: list[Region] = [Region(line['State'], dlc_of(line))]
#endregion

#region States
state_list: list[str] = [line['State'] for line in load_data_csv('csv', 'states.csv')]
#endregion

#region Terminology
terminology_dict: dict[str, str] = {line['Term']: line['Use'] for line in load_data_csv('csv', 'terminology.csv')}

def get_term(key: str) -> str:
    if key.lower() not in terminology_dict: return key
    value = terminology_dict[key.lower()]
    if key.islower(): return value
    if key.isupper(): return value.upper()
    if key.istitle(): return value.title()
    return value
#endregion

#region Truck Dealers
# Note that this code loads the "by city" list and generates the list of check locations from that.
# The "truck-dealers.csv" file is ignored.
truck_dealers_by_city_dict: defaultdict[str, list[str]] = defaultdict(list)
truck_dealer_checks_dict: defaultdict[str, list[CheckLocation]] = defaultdict(list)

for line in load_data_csv('csv', 'truck-dealers-by-city.csv'):
    truck_dealers_by_city_dict[line['Make']] = get_city(line['City']).check_name
    truck_dealer_checks_dict[line['Make']] = get_city(line['City']).rename(line['Make'])
#endregion

#region Truck Makes
truck_makes_list: list[str] = [line['Make'] for line in load_data_csv('csv', 'truck-makes.csv')]
#endregion

#region Trucks
@dataclass(frozen=True)
class TruckModel:
    make: str
    model: str
    required_dlc: str

truck_models_list: list[TruckModel] = [TruckModel(line['Make'], line['Model'], dlc_of(line)) for line in load_data_csv('csv', 'trucks.csv')]
#endregion

#region Viewpoints
viewpoints_dict: dict[str, CheckLocation] = {
    line['Viewpoint']: CheckLocation(line['Viewpoint'],
                                     region_of(line),
                                     line['FerryRequired'])
    for line in load_data_csv('csv', 'viewpoints.csv')}
#endregion
