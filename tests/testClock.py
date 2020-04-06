# -*- coding: utf-8 -*-
"""author: 周光武、簡子琦"""
import unittest
from Clock import Clock

class ClockTest(unittest.TestCase):
    def setUp(self):
        self.clock = Clock(0.01, [0.0, 1.0, 2.0])

    def tearDown(self):
        self.clock = None
    
    def test_forward(self):
        true = self.assertTrue
        clock = self.clock
        clock.current_time = 0.5
        clock.forward()

        true(clock.current_time == 0.51)
    
    def test_is_end(self):
        clock = self.clock
        clock.current_time = 1.99
        self.assertFalse(clock.is_end)
        clock.forward()
        self.assertTrue(clock.is_end)



if __name__ == '__main__':
    unittest.main()