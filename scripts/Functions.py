from typing import Callable, TypeVar, Iterable
from collections import defaultdict

# python 3.11 compat
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')
O = TypeVar('O')

def group(seq: Iterable[T],
          key_selector: Callable[[T], K],
          value_selector: Callable[[T], V] = lambda c: c,
          list_selector: Callable[[K, list[V]], O] = lambda _, l: l) -> dict[K, O]:
  lists = defaultdict(list)
  for item in seq:
    key = key_selector(item)
    val = value_selector(item)
    lists[key].append(val)
  out = {}
  for key, val in lists.items():
    out[key] = list_selector(key, val)
  return out
