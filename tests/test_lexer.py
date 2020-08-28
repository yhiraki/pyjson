# -*- coding: utf-8 -*-

import unittest

from pyjson import lexer

from contextlib import contextmanager


@contextmanager
def raise_with_message(test, expect):
    try:
        yield
    except Exception as e:
        raise Exception(f'test: {test}, expected: {expect}') from e


class TestLexString(unittest.TestCase):
    def test_lex_string(self):
        tests = [
            ('"a"', (3, 'a')),
            ('true', (0, None)),
        ]
        for test, expect in tests:
            with raise_with_message(test, expect):
                self.assertEqual(lexer.lex_string(0, test), expect)

    def test_lex_escaped(self):
        tests = [
            (r'"\"a"', (5, '"a')),
            (r'"\u3042"', (8, 'あ')),
            (r'"\\"', (4, '\\')),
            (r'"\t"', (4, '\t')),
        ]
        for test, expect in tests:
            with raise_with_message(test, expect):
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
    def test_lex_int(self):
        tests = [
            ('1', (1, 1)),
            ('-1', (2, -1)),
            ('-10', (3, -10)),
            ('10', (2, 10)),
            ('a', (0, None)),
            ('+1', (0, None)),
        ]
        for test, expect in tests:
            with raise_with_message(test, expect):
                self.assertEqual(lexer.lex_number(0, test), expect)

    def test_lex_float(self):
        tests = [
            ('1.0', (3, 1.0)),
            ('-1.0', (4, -1.0)),
            ('0.1', (3, 0.1)),
            ('-0.1', (4, -0.1)),
            ('.', (0, None)),
            ('.1', (0, None)),
        ]
        for test, expect in tests:
            with raise_with_message(test, expect):
                self.assertEqual(lexer.lex_number(0, test), expect)

    def test_lex_exp(self):
        tests = [
            ('1e3', (3, 1000.0)),
            ('10e3', (4, 10000.0)),
            ('1e-3', (4, 0.001)),
            ('10e-3', (5, 0.01)),
            ('e10', (0, None)),
        ]
        for test, expect in tests:
            with raise_with_message(test, expect):
                self.assertEqual(lexer.lex_number(0, test), expect)

    def test_lex_fail_invalid_exp(self):
        tests = [
            '1ee3',
            '1e3e',
            '1e',
        ]
        for test in tests:
            with self.assertRaisesRegex(Exception, 'Invalid float'):
                lexer.lex_number(0, test)

    def test_lex_fail_invalid_float(self):
        tests = [
            '1.1.1',
            '1..1',
            '1.',
        ]
        for test in tests:
            with self.assertRaisesRegex(Exception, 'Invalid float'):
                lexer.lex_number(0, test)

    def test_lex_fail_invalid_int(self):
        tests = [
            '01',
            '1-e3',
            '1+1',
        ]
        for test in tests:
            with self.assertRaisesRegex(Exception, 'Invalid int'):
                lexer.lex_number(0, test)


class TestLexBool(unittest.TestCase):
    def test_lex_bool(self):
        tests = [
            ('true', (4, True)),
            ('false', (5, False)),
            ('e', (0, None)),
        ]
        for test, expect in tests:
            with raise_with_message(test, expect):
                self.assertEqual(lexer.lex_bool(0, test), expect)


class TestLexNull(unittest.TestCase):
    def test_lex_null(self):
        tests = [
            ('null', (4, None)),
            ('a', (0, None)),
        ]
        for test, expect in tests:
            with raise_with_message(test, expect):
                self.assertEqual(lexer.lex_null(0, test), expect)


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
            ('{"hoge": true}', ['{', 'hoge', ':', True, '}']),
            ('{"hoge": null}', ['{', 'hoge', ':', None, '}']),
            ('{"hoge": "fuga", "piyo": 1}',
             ['{', 'hoge', ':', 'fuga', ',', 'piyo', ':', 1, '}']),
        ]
        for test, expect in tests:
            with raise_with_message(test, expect):
                self.assertEqual(lexer.lex(test), expect)


if __name__ == '__main__':
    unittest.main()
