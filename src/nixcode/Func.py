from typing import Iterable, Any, Optional, Sequence, TypeVar
from unicodedata import normalize

ENABLE_NIXPRINT = False

T = TypeVar('T')

def nixprint(msg: Optional[str] = None) -> None:
    """
    Prints the message. It's an external method just for ease of turning off.
    """
    if ENABLE_NIXPRINT:
        if msg:
            # pass
            print(msg)
        else:
            # pass
            print()

def get_case_key(input: dict[str, T], match: str) -> T:
    """
    Returns a value associated with a case-insensitive key.
    """
    match = match.lower()
    for a in input.keys():
        if match == a.lower(): return input[a]
    raise KeyError(match)

def get_case_key_opt(input: dict[str, T], match: str) -> Optional[T]:
    """
    Returns a value associated with a case-insensitive key.
    """
    match = match.lower()
    for a in input.keys():
        if match == a.lower(): return input[a]
    return None

def in_case(input: Iterable[str], match: str) -> bool:
    """
    Returns whether a value is in a list of strings, case-insensitive.
    """
    match = match.lower()
    for a in input:
        if match == a.lower(): return True
    return False

def get_case(input: Iterable[str], match: str) -> str:
    """
    Returns the original value from a list of strings given a case-insensitive match.
    """
    match = match.lower()
    for a in input:
        if match == a.lower(): return a
    raise KeyError(match)

def get_case_opt(input: Iterable[str], match: str) -> Optional[str]:
    """
    Returns the original value from a list of strings given a case-insensitive match.
    """
    match = match.lower()
    for a in input:
        if match == a.lower(): return a
    return None

def ensure_removed(input: list[T], match: T) -> None:
    """
    Ensures that the given element is not in the list (removes it if necessary, but does not error if not).
    """
    if match in input: input.remove(match)

def pop_iter(input: Sequence[T]) -> Iterable[T]:
    while input:
        yield input.pop()

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
