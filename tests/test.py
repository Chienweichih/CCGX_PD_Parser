# -*- coding: utf-8 -*-

from .context import usb_pd

import unittest

class TestCCLog(unittest.TestCase):
    def test_csv(self):
        self.assertIsNone(usb_pd.csvReader("test.csv", ""))

    def test_csv_goodcrc(self):
        self.assertIsNone(usb_pd.csvReader("test.csv", "GoodCRC"))

if __name__ == '__main__':
    unittest.main()