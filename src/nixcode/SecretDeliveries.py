from random import Random
from typing import Any
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState, Item

from .DataClasses import CheckLocation, SecretDeliveryLetter
from .CsvData import city_dict, connections_dict, secret_delivery_list

def get_secret_deliveries(world: World) -> list[str]:
    if world.options.goal != getattr(world.options.goal, 'option_All Secret Deliveries Completed'):
        return []
    delivery_count = world.options.secret_deliveries_available.value
    return [get_secret_delivery(world) for _ in range(delivery_count)]

def get_secret_delivery(world: World) -> str:
    dlcs: set[str] = world.options.dlcs_available.value
    cities: set[CheckLocation] = [c for c in city_dict.values() if c.region.dlc in dlcs]

    randomizer: Random = world.random
    source_city_check: CheckLocation = randomizer.choice(cities)
    source_city_name = source_city_check.check_name
    source_city_state = source_city_check.region.state

    states: set[str] = {source_city_state}
    neighbors: set[str] = set[str]()

    for lst in [v.keys() for k, v in connections_dict.items() if k.state == source_city_state and k.dlc in dlcs]:
        neighbors.update(s.state for s in lst if s.dlc in dlcs)
        neighbors.difference_update(states)

    count = 0
    max_borders = world.options.secret_delivery_country_border_limit.value
    while neighbors and count < max_borders:
        count += 1
        states.update(neighbors)
        neighbors.clear()
        for lst in [v.keys() for k, v in connections_dict.items() if k.state in states and k.dlc in dlcs]:
            neighbors.update(s.state for s in lst if s.dlc in dlcs)
            neighbors.difference_update(states)

    dest_cities = [c.check_name for c in cities if c.region.state in states]

    if dest_cities:
        dest_city_name = randomizer.choice(dest_cities)
    else:
        dest_city_name = randomizer.choice({c.check_name for c in cities})

    letter = randomizer.choice(secret_delivery_list)
    text = letter.create(source_city_name, dest_city_name, randomizer)
    return text
