# -*- coding: utf-8 -*-

from . import const


def parse_array(i, tokens):
    t = tokens[i]
    if t != const.OPENBRACKET:
        raise Exception('Excpected bracket array starts')

    i += 1
    array = []

    t = tokens[i]
    if t == const.CLOSEBRACKET:
        return i + 1, array

    try:
        while i < len(tokens):
            i, json = _parse(i, tokens)
            array.append(json)

            t = tokens[i]
            if t == const.CLOSEBRACKET:
                return i + 1, array

            if t != const.COMMA:
                raise Exception('Expected comma after object in array')

            i += 1
    except IndexError:
        pass

    raise Exception('Expected bracket end of array')


def parse_object(i, tokens):
    t = tokens[i]
    if t != const.OPENBRACE:
        raise Exception('Excpected bracket array starts')

    i += 1
    obj = {}

    t = tokens[i]
    if t == const.CLOSEBRACE:
        return i + 1, obj

    try:
        while i < len(tokens):
            key = tokens[i]
            if type(key) is not str:
                raise Exception(f'Excepted string key, got: {key}')
            i += 1
            colon = tokens[i]
            if colon != const.COLON:
                raise Exception('Excepted colon after key in object')
            i += 1

            i, json = _parse(i, tokens)
            obj[key] = json

            t = tokens[i]
            if t == const.CLOSEBRACE:
                return i, obj

            if t != const.COMMA:
                raise Exception('Excepted comma after pair in object')

            i += 1
    except IndexError:
        pass

    raise Exception('Expected brace end of object')


def _parse(i, tokens):
    t = tokens[i]

    if t == const.OPENBRACKET:
        return parse_array(i, tokens)

    if t == const.OPENBRACE:
        return parse_object(i, tokens)

    return i + 1, tokens[i]


def parse(tokens):
    if tokens[0] != const.OPENBRACE:
        raise Exception('must be start with brace')

    return _parse(0, tokens)[1]
