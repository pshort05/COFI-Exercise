#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
#
#                               COFI_coding_exercise.py     by Paul Short
#                                                           paul@jpkweb.com
#                                                           using Python v3.6
#                               Unit Tests
#
# ----------------------------------------------------------------------------------------------------------------------
import pycurl, json
import pprint
from io import BytesIO
import unittest

from COFI_coding_exercise import getAllTransactions

class test_getAllTransactions(unittest.TestCase):

    # Verify that all the transactions are loaded and the first item contains "no-error"
    def testPrintAllRecords(self):
        jsonData = getAllTransactions()
        self.assertEqual( 'no-error', jsonData["error"] )