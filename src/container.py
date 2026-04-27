import json
import zipfile
from typing import Any

from .hooks.World import create_additional_data_files
from worlds import Files
from worlds.AutoWorld import World

from .Data import region_table, category_table
from .Game import game_name
from .Locations import location_name_to_location
from .Items import item_name_to_item

if hasattr(Files, 'APPlayerContainer'):
    APPlayerContainer = Files.APPlayerContainer
else:
    # Prior to 0.6.2, all containers were player containers.
    APPlayerContainer = Files.APContainer

class APManualFile(APPlayerContainer):
    game = game_name
    patch_file_ending = ".apmanual"
    world: World

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    def add_world(self, world: World):
        self.world = world

    def write_contents(self, opened_zipfile: zipfile.ZipFile):
        super().write_contents(opened_zipfile)
        opened_zipfile.writestr("items.json", json.dumps(item_name_to_item, indent=2))
        opened_zipfile.writestr("locations.json", json.dumps(location_name_to_location, indent=2))
        opened_zipfile.writestr("regions.json", json.dumps(region_table, indent=2))
        opened_zipfile.writestr("categories.json", json.dumps(category_table, indent=2))

        additional_files: dict[str, str] = create_additional_data_files(self.world)

        for filename, text in additional_files.items():
            opened_zipfile.writestr(f"game_data/{filename}", text)

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> dict[str, Any]:
        manifest = super().read_contents(opened_zipfile)
        self.items = json.loads(opened_zipfile.read("items.json"))
        self.locations = json.loads(opened_zipfile.read("locations.json"))
        self.regions = json.loads(opened_zipfile.read("regions.json"))
        return manifest

    def as_dict(self) -> dict[str, Any]:
        data = {}
        data["items"] = self.items
        data["locations"] = self.locations
        data["regions"] = self.regions
        return data
