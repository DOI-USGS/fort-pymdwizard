from __future__ import print_function
import unittest

import sys
sys.path.append(r"../..")
import pymdwizard

class pymdwizardTest(unittest.TestCase):

    def setUp(self):
        self.something = [1, 2, 3, 4]
        
    def test_pymdwizard_1(self):
        self.assertTrue(3 in self.something)

    def test_pymdwizard_2(self):
        with self.assertRaises(ZeroDivisionError):
            #this should fail!
            print(1/0)


if __name__ == '__main__':
    unittest.main()
