# -*- coding: utf-8 -*-

import unittest

from pyjson import lexer


class TestLexString(unittest.TestCase):
    def test_lex_string(self):
        tests = [
            ('"a"', (3, 'a')),
            ('"a"', (3, 'a')),
            ('true', (0, None)),
        ]
        for test, expect in tests:
            self.assertEqual(lexer.lex_string(0, test), expect)

    def test_lex_escaped(self):
        tests = [
            (r'"\"a"', (5, '"a')),
            (r'"\u3042"', (8, 'あ')),
            (r'"\\"', (4, '\\')),
            (r'"\t"', (4, '\t')),
        ]
        for test, expect in tests:
            self.assertEqual(lexer.lex_string(0, test), expect)

    def test_lex_fail_end_of_string_quote(self):
        tests = [
            '"hoge',
            '"',
        ]
        for test in tests:
            with self.assertRaisesRegex(Exception, 'quote'):
                lexer.lex_string(0, test)

    def test_lex_fail_unescaped_charactor(self):
        tests = [
            r'"\h"',
            r'"\a"',
            r'"\u"',
            r'"\u00"',
        ]
        for test in tests:
            with self.assertRaisesRegex(Exception, 'Invalid escape'):
                r = lexer.lex_string(0, test)
                print(r)

    def test_lex_fail_unicode(self):
        tests = [
            r'"\uxxxx"',
        ]
        for test in tests:
            with self.assertRaisesRegex(Exception, 'Invalid unicode'):
                r = lexer.lex_string(0, test)
                print(r)


class TestLexNumber(unittest.TestCase):
    def test_lex_number(self):
        tests = [
            ('1', (1, 1)),
            ('10', (2, 10)),
            ('1.0', (3, 1.0)),
            ('0.1', (3, 0.1)),
            ('.1', (2, 0.1)),
            ('a', (0, None)),
        ]
        for test, expected in tests:
            self.assertEqual(lexer.lex_number(0, test), expected)

    def test_lex_fail_invalid_float(self):
        tests = [
            '1.1.1',
            '1..1',
            '.',
            '..',
        ]
        for test in tests:
            with self.assertRaisesRegex(Exception, 'Invalid float'):
                lexer.lex_number(0, test)


class TestLexBool(unittest.TestCase):
    def test_lex_bool(self):
        tests = [
            ('true', (4, True)),
            ('false', (5, False)),
            ('e', (0, None)),
        ]
        for test, expected in tests:
            self.assertEqual(lexer.lex_bool(0, test), expected)


class TestLexNull(unittest.TestCase):
    def test_lex_null(self):
        tests = [
            ('null', (4, None)),
            ('a', (0, None)),
        ]
        for test, expected in tests:
            self.assertEqual(lexer.lex_null(0, test), expected)


class TestLexer(unittest.TestCase):
    def test_lex_success(self):
        tests = [
            ('{}', ['{', '}']),
            ('[]', ['[', ']']),
            ('{ }', ['{', '}']),
            ('{"hoge"}', ['{', 'hoge', '}']),
            (r'{"\"hoge"}', ['{', '"hoge', '}']),
            (r'{"\u3042"}', ['{', 'あ', '}']),
            ('[{"hoge"}]', ['[', '{', 'hoge', '}', ']']),
            ('{ "hoge" }', ['{', 'hoge', '}']),
            (' {"hoge"} ', ['{', 'hoge', '}']),
            (' {""} ', ['{', '', '}']),
            ('{"hoge": 1}', ['{', 'hoge', ':', 1, '}']),
            ('{"hoge": 1.0}', ['{', 'hoge', ':', 1.0, '}']),
            ('{"hoge": .1}', ['{', 'hoge', ':', 0.1, '}']),
            ('{"hoge": true}', ['{', 'hoge', ':', True, '}']),
            ('{"hoge": null}', ['{', 'hoge', ':', None, '}']),
            ('{"hoge": "fuga", "piyo": 1}',
             ['{', 'hoge', ':', 'fuga', ',', 'piyo', ':', 1, '}']),
        ]
        for test, expected in tests:
            self.assertEqual(lexer.lex(test), expected)


if __name__ == '__main__':
    unittest.main()
