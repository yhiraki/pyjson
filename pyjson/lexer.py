# -*- coding: utf-8 -*-

JSON_QUOTE = '"'
JSON_COLON = ':'
JSON_COMMA = ','

JSON_OPENBRACE = '{'
JSON_CLOSEBRACE = '}'
JSON_OPENBRACKET = '['
JSON_CLOSEBRACKET = ']'

JSON_WHITESPACE = ' \t\b\n\r'

JSON_TRUE = 'true'
JSON_FALSE = 'false'
JSON_NULL = 'null'

JSON_SYNTAX = (
    JSON_OPENBRACE,
    JSON_CLOSEBRACE,
    JSON_OPENBRACKET,
    JSON_CLOSEBRACKET,
    JSON_COLON,
    JSON_COMMA,
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
    if string[i] != JSON_QUOTE:
        return i, None

    ret = ''
    j = i + 1
    while j < len(string) and string[j] != JSON_QUOTE:

        if string[j] == '\\':
            j += 1
            if j >= len(string):
                raise
            c = JSON_ESCAPED.get(string[j])
            if not c:
                raise Exception(f'Unexpected escape charactor \\{string[j]}')

            if c == 'u':
                j += 1
                k = j + 4
                if k >= len(string):
                    raise Exception(
                        f'Unexpected escape charactor \\{string[j:j+4]}')
                try:
                    h = int(string[j:j + 4], 16)
                except ValueError as e:
                    raise Exception(
                        f'Unexpected unicode charactor \\u{string[j:j + 4]}'
                    ) from e
                ret += chr(h)
                j = k
                continue

            ret += c
            j += 1
            continue

        ret += string[j]
        j += 1

    if j >= len(string) or string[j] != JSON_QUOTE:
        raise Exception('Expected end-of-string quote')

    return j + 1, ret


def lex_number(i, string):
    numbers = [str(i) for i in range(10)]
    symbols = ['.']
    number_chars = numbers + symbols

    is_float = False

    j = i
    while j < len(string) and string[j] in number_chars:
        if string[j] == '.':
            if is_float:
                raise Exception('invalid float')
            is_float = True
        j += 1

    if j == i:
        return j, None

    json_number = string[i:j]

    if is_float:
        if len(json_number) == 1:
            raise Exception('invalid float')
        return j, float(json_number)

    return j, int(json_number)


def lex_bool(i, string):
    if string[i] not in (JSON_TRUE[0], JSON_FALSE[0]):
        return i, None

    for b, ret in ((JSON_TRUE, True), (JSON_FALSE, False)):
        len_b = len(b)
        if string[i:i + len_b] == b:
            return i + len_b, ret

    return i, None


def lex_null(i, string):
    if string[i] not in JSON_NULL[0]:
        return i, None

    for b, ret in ((JSON_NULL, None), ):
        len_b = len(b)
        if string[i:i + len_b] == b:
            return i + len_b, ret


def skip_whitespace(i, string):
    while i < len(string) and string[i] in JSON_WHITESPACE:
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
