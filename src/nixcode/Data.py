from dataclasses import dataclass
from collections import defaultdict

from .Func import snake_case
from ..Helpers import load_data_csv

#region DLC Connections
dlc_connections: defaultdict[str, list[str]] = defaultdict(list)

_dlc_connections_csv: list[dict[str, str]] = load_data_csv("csv", "dlc-connections.csv")

for line in _dlc_connections_csv:
    left_dlc = snake_case(line['DLC1'] or 'Base Game')
    right_dlc = snake_case(line['DLC2'] or 'Base Game')

    dlc_connections[left_dlc].append(right_dlc)
    dlc_connections[right_dlc].append(left_dlc)
#endregion

#region Regions
@dataclass(frozen=True)
class Region:
    state: str
    dlc: str

_region_list_csv: list[dict[str, str]] = load_data_csv("csv", "regions.csv")

region_list: list[Region] = [Region(line["State"], line["DLC"]) for line in _region_list_csv]
state_dlcs_dict: dict[str, list[str]] = {}
dlc_states_dict: dict[str, list[str]] = {}

for r in region_list:
    state_dlcs_dict[r.state].append(r.dlc)
    dlc_states_dict[r.dlc].append(r.state)
#endregion
