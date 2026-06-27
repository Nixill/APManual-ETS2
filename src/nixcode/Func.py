from inspect import stack
from random import Random
from typing import Callable, Iterable, Any, Optional, Sequence, TypeVar
from unicodedata import normalize

ENABLE_DBGPRINT = False
DBGPRINT_FUNCTIONS = [
    # 'implement_checks_reduction',
    # 'perform_final_grants',
    # 'start_with_item',
    # 'are_dlcs_connected',
]

def dbgprint(msg: Callable[[], str]) -> None:
    """
    Prints a given message with function info if it's an allowlisted function.
    """
    if not ENABLE_DBGPRINT: return
    stk = stack()
    if len(stk) < 2: return
    if stk[1].function in DBGPRINT_FUNCTIONS:
        print(f'[Manual_EuroTruckSimulator2_Nixill / {stk[1].function} @ {stk[1].lineno}] {msg()}')

T = TypeVar('T')

def fullprint(msg: str):
    """
    Prints the message, prefixing it with "Euro Truck Simulator 2: "
    """
    print(f'[Manual_EuroTruckSimulator2_Nixill] {msg}')

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

CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_-'
def random_string(random: Random) -> str:
    bytes = random.randbytes(15)
    out = ''
    for i in range(0, 15, 3):
        char1 = bytes[i] % 64
        char2 = bytes[i] // 64 + (bytes[i+1] % 16 * 4)
        char3 = bytes[i+1] // 16 + (bytes[i+2] % 4 * 16)
        char4 = bytes[i+2] // 4
        out += f'{CHARS[char1]}{CHARS[char2]}{CHARS[char3]}{CHARS[char4]}'
    return out

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
