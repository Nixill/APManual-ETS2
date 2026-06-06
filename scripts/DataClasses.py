# Assumes run from repository root!
from dataclasses import dataclass
from csv import DictReader

#region Type defs
@dataclass(frozen=True)
class Region:
  state_name: str
  dlc_name: str

  def __str__(self):
    return f'{self.state_name} {self.dlc_name}'

@dataclass(frozen=True)
class Check:
  name: str
  region: Region
  ferry_required: bool
  hidden_path: bool = True

@dataclass(frozen=True)
class Connection:
  region_1: Region
  region_2: Region
  ferry_required: bool

@dataclass(frozen=True)
class DLCConnection:
  dlc_1: str
  dlc_2: str

@dataclass(frozen=True)
class CompanyName:
  latin_name: str
  cyrillic_name: str | None = None
  greek_name: str | None = None

@dataclass(frozen=True)
class Truck:
  make: str
  model: str
  dlc: str
#endregion
