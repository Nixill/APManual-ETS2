from dataclasses import dataclass

@dataclass(frozen=True)
class Region:
    state: str
    dlc: str

@dataclass(frozen=True)
class CheckLocation:
    check_name: str
    region: Region
    ferry_required: bool

    def rename(self, new_name: str):
        return CheckLocation(new_name, self.region, self.ferry_required)

@dataclass(frozen=True)
class TruckModel:
    make: str
    model: str
    required_dlc: str

@dataclass(frozen=True)
class GameInfo:
    name: str
    creator: str
    filler_item_name: str
