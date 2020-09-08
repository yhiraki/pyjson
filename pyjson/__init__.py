VERSION = '0.0.1'

from .lexer import lex
from .parser import parse


def load(fp):
    return loads(fp.read())


def loads(s: str):
    tokens = lex(s)
    return parse(tokens)
