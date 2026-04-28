from dataclasses import dataclass
from random import Random

@dataclass(frozen=True)
class DLC:
    name: str
    date: int
    is_main_map: bool = True

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

@dataclass(frozen=True)
class SecretDeliveryLetter:
    text: str
    signatures: list[str]
    signature_chance: float

    def create(self, source: str, destination: str, randomizer: Random):
        text = self.text.replace('{source}', source).replace('{destination}', destination)

        if randomizer.random() < self.signature_chance:
            text += f'\n\n  - {randomizer.choice(self.signatures)}'

        return text
