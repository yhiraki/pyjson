# -*- coding: utf-8 -*-

import unittest
from pyjson import parser


class TestParseArray(unittest.TestCase):
    def test_parse(self):
        tests = [
            (['[', ']'], []),
            (['[', 1, ']'], [1]),
            (['[', 1, ',', 2, ']'], [1, 2]),
            (['[', 1, ',', 'hoge', ']'], [1, 'hoge']),
        ]
        for test, expect in tests:
            self.assertEqual(parser.parse_array(0, test)[1], expect)

    def test_parse_fail_no_comma(self):
        tests = [
            ['[', 1, 1],
            ['[', ',', 1],
        ]
        for test in tests:
            with self.assertRaisesRegex(Exception, 'Expected comma'):
                parser.parse_array(0, test)

    def test_parse_fail_no_end_bracket(self):
        tests = [
            ['[', 1, ',', 1],
        ]
        for test in tests:
            with self.assertRaisesRegex(Exception, 'Expected bracket'):
                parser.parse_array(0, test)


class TestParseObject(unittest.TestCase):
    def test_parse(self):
        tests = [
            (['{', '}'], {}),
            (['{', 'a', ':', 1, '}'], {
                'a': 1
            }),
            (['{', 'a', ':', 'b', '}'], {
                'a': 'b'
            }),
            (['{', 'a', ':', 1, ',', 'b', ':', 2, '}'], {
                'a': 1,
                'b': 2
            }),
        ]
        for test, expect in tests:
            self.assertEqual(parser.parse_object(0, test)[1], expect)

    def test_parse_fail_key_not_string(self):
        tests = [
            ['{', 1],
        ]
        for test in tests:
            with self.assertRaisesRegex(Exception, 'Excepted string key'):
                parser.parse_object(0, test)

    def test_parse_fail_no_colon(self):
        tests = [
            ['{', 'a', 1, '}'],
        ]
        for test in tests:
            with self.assertRaisesRegex(Exception, 'Excepted colon'):
                parser.parse_object(0, test)

    def test_parse_fail_no_comma(self):
        tests = [
            ['{', 'a', 1],
        ]
        for test in tests:
            with self.assertRaisesRegex(Exception, 'Excepted colon'):
                parser.parse_object(0, test)

    def test_parse_fail_no_end_brace(self):
        tests = [
            ['{', 'a', ':', 1],
        ]
        for test in tests:
            with self.assertRaisesRegex(Exception, 'Expected brace'):
                parser.parse_object(0, test)


class TestParse(unittest.TestCase):
    def test_parse(self):
        tests = [
            (['{', 'a', ':', '[', ']', '}'], {
                'a': []
            }),
            (['{', 'a', ':', '{', '}', '}'], {
                'a': {}
            }),
            (['{', 'a', ':', '{', 'b', ':', 1, '}', '}'], {
                'a': {
                    'b': 1
                }
            }),
        ]
        for test, expected in tests:
            self.assertEqual(parser.parse(test), expected)


if __name__ == '__main__':
    unittest.main()
