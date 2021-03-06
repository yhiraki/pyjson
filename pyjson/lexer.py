# -*- coding: utf-8 -*-

from . import const

JSON_SYNTAX = (
    const.OPENBRACE,
    const.CLOSEBRACE,
    const.OPENBRACKET,
    const.CLOSEBRACKET,
    const.COLON,
    const.COMMA,
)

JSON_ESCAPED = {
    '"': '"',
    '\\': '\\',
    '/': '/',
    'b': '\b',
    'f': '\f',
    'n': '\n',
    'r': '\r',
    't': '\t',
    'u': 'u'
}


def lex_string(i, string):
    if string[i] != const.QUOTE:
        return i, None

    ret = ''
    j = i + 1
    while j < len(string) and string[j] != const.QUOTE:

        if string[j] == '\\':
            j += 1
            if j >= len(string):
                raise
            c = JSON_ESCAPED.get(string[j])
            if not c:
                raise Exception(f'Invalid escape charactor \\{string[j]}')

            if c == 'u':
                j += 1
                k = j + 4
                if k >= len(string):
                    raise Exception(
                        f'Invalid escape charactor \\{string[j:j+4]}')
                try:
                    h = int(string[j:j + 4], 16)
                except ValueError as e:
                    raise Exception(
                        f'Invalid unicode charactor \\u{string[j:j + 4]}'
                    ) from e
                ret += chr(h)
                j = k
                continue

            ret += c
            j += 1
            continue

        ret += string[j]
        j += 1

    if j >= len(string) or string[j] != const.QUOTE:
        raise Exception('Expected end-of-string quote')

    return j + 1, ret


def lex_number(i, string):
    numbers = [str(i) for i in range(10)]
    symbols = ['.', 'e', '-', '+']
    number_chars = numbers + symbols

    if string[i] not in (numbers + ['-']):
        return i, None

    is_float = False

    j = i
    while j < len(string) and string[j] in number_chars:
        if string[j] in ['.', 'e']:
            if is_float:
                raise Exception('Invalid float')
            is_float = True
        if string[j] in ['-', '+']:
            if j != i and not string[j - 1] == 'e':
                if is_float:
                    raise Exception('Invalid float')
                raise Exception('Invalid int')
        j += 1

    if j == i:
        return j, None

    json_number = string[i:j]

    if is_float:
        if string[-1] in ['.', 'e']:
            raise Exception('Invalid float')
        return j, float(json_number)

    if len(string) > 1 and string[0] == '0':
        raise Exception('Invalid int')

    return j, int(json_number)


def lex_bool(i, string):
    if string[i] not in (const.TRUE[0], const.FALSE[0]):
        return i, None

    for b, ret in ((const.TRUE, True), (const.FALSE, False)):
        len_b = len(b)
        if string[i:i + len_b] == b:
            return i + len_b, ret

    return i, None


def lex_null(i, string):
    if string[i] not in const.NULL[0]:
        return i, None

    for b, ret in ((const.NULL, None), ):
        len_b = len(b)
        if string[i:i + len_b] == b:
            return i + len_b, ret


def skip_whitespace(i, string):
    while i < len(string) and string[i] in const.WHITESPACE:
        i += 1
    return i


def lex(string):
    tokens = []

    i = 0
    while i < len(string):
        lexers = (
            lex_string,
            lex_number,
            lex_bool,
            lex_null,
        )
        lexed = False
        for lexer in lexers:
            j, value = lexer(i, string)
            if i < j:
                tokens.append(value)
                i = j
                lexed = True
                break
        if lexed:
            continue

        j = skip_whitespace(i, string)
        if i < j:
            i = j
            continue

        if string[i] in JSON_SYNTAX:
            tokens.append(string[i])
            i += 1
            continue

        raise Exception(f'Unexpected charactor: {string[i]}')
    return tokens
