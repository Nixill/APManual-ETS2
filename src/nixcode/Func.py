from typing import Iterable, Any, TypeVar
from unicodedata import normalize

T = TypeVar('T')

def index_and(input: Iterable[T]) -> Iterable[tuple[int, T]]:
    index = 0
    for item in input:
        yield (index, item)
        index += 1

def _snake_case_i(input: str) -> Iterable[str]:
    output = False
    space = False
    for c in normalize('NFKD', input.lower()):
        if c.isalpha() and c.isascii():
            if space:
                yield '_'
                space = False
            yield c
            output = True
        elif c in ' _-':
            if output: space = True

def snake_case(input: str) -> str:
    return ''.join(_snake_case_i(input))
