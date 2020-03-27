import unittest
from Point import Point

class PointTest(unittest.TestCase):
    def setUp(self):
        self.p1 = Point(1, 2, 3)
        self.p2 = Point(2, 4, 6)
    
    def tearDown(self):
        self.p1 = None
        self.p2 = None
    
    def test_value(self):
        true = self.assertTrue
        
        true(self.p1.value, [1, 2, 3])
        true(self.p2.value, [2, 4, 6])
    
    def test_add(self):
        p = self.p1 + self.p2
        self.assertTrue(p.value, [3, 6, 9])
    
    def test_sub(self):
        p = self.p1 = self.p2
        self.assertTrue(p.value, [-1, -2, -3])
    
    def test_mul(self):
        p = self.p1 * 2
        self.assertTrue(p.value, self.p2.value)
    
    def test_div(self):
        p = self.p2 / 2
        self.assertTrue(p.value, self.p1.value)

    def test_iadd(self):
        self.p1 += self.p2
        self.assertTrue(self.p1.value, [3, 6, 9])
    
    def test_isub(self):
        self.p1 -= self.p2
        self.assertTrue(self.p1.value, [-1, -2, -3])

    def test_imul(self):
        self.p1 *= 2
        self.assertTrue(self.p1.value, self.p2.value)
    
    def test_idiv(self):
        self.p2 /= 2
        self.assertTrue(self.p2.value, self.p1.value)