from csv import DictReader
from os import getcwd

from DataClasses import Check, CompanyName, DLCConnection, Region, Connection, Truck

if (getcwd().endswith('scripts')):
  _prefix: str = '../'
else:
  _prefix: str = ''

def csv_path(filename: str) -> str: return f'{_prefix}src/data/csv/{filename}.csv'
def csv_contents(filename: str) -> DictReader:
  with open(csv_path(filename), 'r', newline='', encoding='utf8') as file:
    return [row for row in DictReader(file)]

cities: dict[str, Check] = {d['City']: Check(
  name=d['City'],
  region=Region(
    state_name=d['State'],
    dlc_name=d['DLC'] or 'Base Game'
  ),
  ferry_required=bool(d['FerryRequired'])
) for d in csv_contents('cities')}

city_aliases: dict[str, str] = {d['LocalName']: d['City']
                                for d in csv_contents('city-aliases')}

companies: set[str] = {d['Company'] for d in csv_contents('companies')}

company_locations: list[Check] = [Check(
  name=d['Company'],
  region=Region(
    state_name=d['State'],
    dlc_name=d['DLC'] or 'Base Game'
  ),
  ferry_required=bool(d['FerryRequired'])
) for d in csv_contents('company-locations')]

company_names: list[CompanyName] = [CompanyName(
  latin_name=d['Latin'],
  cyrillic_name=d['Cyrillic'] or None,
  greek_name=d['Greek'] or None
) for d in csv_contents('company-names')]

connections: list[Connection] = [Connection(
  region_1=Region(
    state_name=d['Left'],
    dlc_name=d['LeftDLC'] or 'Base Game'
  ),
  region_2=Region(
    state_name=d['Right'],
    dlc_name=d['RightDLC'] or 'Base Game'
  ),
  ferry_required=bool(d['IsFerry'])
) for d in csv_contents('connections')]

dlcs: set[str] = {d['DLC'] or 'Base Game' for d in csv_contents('dlcs')}

dlc_connections: list[DLCConnection] = [DLCConnection(
  dlc_1=d['DLC1'] or 'Base Game',
  dlc_2=d['DLC2'] or 'Base Game'
) for d in csv_contents('dlc-connections')]

game_info: dict[str, str] = {d['Key']: d['Value'] for d in csv_contents('game-info')}

photo_trophies: dict[str, Check] = {d['Trophy']: Check(
  name=d['Trophy'],
  region=Region(
    state_name=d['State'],
    dlc_name=d['DLC'] or 'Base Game'
  ),
  ferry_required=bool(d['FerryRequired'])
) for d in csv_contents('photo-trophies')}

quick_travel: list[Region] = [Region(
  state_name=d['State'],
  dlc_name=d['DLC'] or 'Base Game'
) for d in csv_contents('quick-travel')]

regions: list[Region] = [Region(
  state_name=d['State'],
  dlc_name=d['DLC'] or 'Base Game'
) for d in csv_contents('regions')]

states: set[str] = {d['State'] for d in csv_contents('states')}

terminology: dict[str, str] = {d['Term']: d['Use'] for d in csv_contents('terminology')}

trucks: list[Truck] = [Truck(
  make=d['Make'],
  model=d['Model'],
  dlc=d['DLC'] or 'Base Game'
) for d in csv_contents('trucks')]

truck_dealers: list[Check] = [Check(
  name=d['Make'],
  region=Region(
    state_name=d['State'],
    dlc_name=d['DLC'] or 'Base Game'
  ),
  ferry_required=bool(d['FerryRequired'])
) for d in csv_contents('truck-dealers')]

truck_dealers_by_city: dict[str, str] = {d['City']: d['Make'] for d in csv_contents('truck-dealers-by-city')}

truck_makes: set[str] = {d['Make'] for d in csv_contents('truck-makes')}

viewpoints: dict[str, Check] = {d['Viewpoint']: Check(
  name=d['Viewpoint'],
  region=Region(
    state_name=d['State'],
    dlc_name=d['DLC'] or 'Base Game'
  ),
  ferry_required=bool(d['FerryRequired']),
  hidden_path=bool(d['HiddenPath'])
) for d in csv_contents('viewpoints')}
