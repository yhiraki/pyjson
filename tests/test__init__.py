#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import pyjson


class TestModule(unittest.TestCase):
    def test_loads(self):
        tests = [
            ('{}', {}),
            ('{"a":1}', {
                'a': 1
            }),
            ('{"a":[]}', {
                'a': []
            }),
            ('{"a":[1,2,3]}', {
                'a': [1, 2, 3]
            }),
            ('{"a":{"b":1}}', {
                'a': {
                    'b': 1
                }
            }),
            ('{"a":[{"b":1}]}', {
                'a': [{
                    'b': 1
                }]
            }),
            ('{"a":[1,{"b":1},3]}', {
                'a': [1, {
                    'b': 1
                }, 3]
            }),
            ('{"a":    1}', {
                'a': 1
            }),
            ('{"1": "a"}', {
                '1': 'a'
            }),
            ('{",": ","}', {
                ',': ','
            }),

            # TODO: pass the test
            # ('{":": "{"}', {
            #     ':': '{'
            # }),
        ]
        for test, expected in tests:
            self.assertEqual(pyjson.loads(test), expected)

    def test_loads_fail_not_start_with_brace(self):
        tests = [
            '[]',
            '1',
            '}',
        ]
        for test in tests:
            with self.assertRaisesRegex(Exception, 'start with brace'):
                self.assertEqual(pyjson.loads(test))


if __name__ == '__main__':
    unittest.main()
