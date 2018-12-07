#!/usr/bin/python
# -*-coding: utf-8 -*-

import unittest
from kanimysql import KaniMySQL


class TestSQLConversion(unittest.TestCase):
    def setUp(self):
        self.connection = KaniMySQL(host='localhost', user='root', passwd='p@ssw0rd')
        self.connection.debug = True

    def testWhere(self):
        where = self.connection._where_parser(where={'id': {'$<': 20}})
        self.assertEqual(where,
                         " WHERE (`id` < 20)")

    def testWhere(self):
        where = self.connection._where_parser(where={'id': {'$NOT': None}})
        self.assertEqual(where,
                         " WHERE (`id` IS NOT NULL)")

if __name__ == '__main__':
    unittest.main()
