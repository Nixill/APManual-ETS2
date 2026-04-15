from typing import Iterable
from unicodedata import normalize

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
