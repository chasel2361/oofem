import unittest
from Vector import Vector
from Point import Point

class VectorTest(unittest.TestCase):
    def setUp(self):
        p1 = Point()
        p2 = Point(1, 1, 1)
        p3 = Point(-1, -1, 1)

        self.v1 = Vector(p1, p2)
        self.v2 = Vector(p1, p3)
    
    def tearDown(self):
        self.v1 = None
        self.v2 = None
    
    def test_value(self):
        true = self.assertTrue

        true(self.v1.value, [1, 1, 1])
        true(self.v2.value, [-1, -1, 1])
    
    def test_length(self):
        true = self.assertTrue

        l1 = self.v1.length
        l2 = self.v2.length

        true(l1, 3**0.5)
        true(l2, l1)
    
    def test_direction(self):
        true = self.assertTrue

        d1 = self.v1.direction
        d2 = self.v2.direction
        ansv = 3**0.5
        ans1 = Vector(Point(), Point(ansv, ansv, ansv))
        ans2 = Vector(Point(), Point(-ansv, -ansv, ansv))

        true(d1.value, ans1.value)
        true(d2.value, ans2.value)
    
    def test_normalize(self):
        true = self.assertTrue

        self.v1.normalize
        self.v2.normalize
        ansv = 3**0.5
        ans1 = Vector(Point(), Point(ansv, ansv, ansv))
        ans2 = Vector(Point(), Point(-ansv, -ansv, ansv))

        true(self.v1.value, ans1.value)
        true(self.v2.value, ans2.value)
    
    def test_dot(self):
        true = self.assertTrue

        dot1 = self.v1.dot(self.v2)
        dot2 = self.v2.dot(self.v1)
        true(dot1, 1)
        true(dot1, dot2)
    
    def test_cross(self):
        true = self.assertTrue

        cross1 = self.v1.cross(self.v2)
        cross2 = self.v2.cross(self.v1)
        ans1 = Vector(Point(), Point(2, -2, 0))
        ans2 = Vector(Point(), Point(-2, 2, 0))
        true(cross1, ans1.value)
        true(cross2, ans2.value)

    def test_rotation(self):
        deg = self.v1.rotation(self.v2)
        self.assertTrue(deg, 70.52877936550934)
    
    def test_add(self):
        v = self.v1 + self.v2
        self.assertTrue(v.value, [0, 0, 2])
    
    def test_sub(self):
        v = self.v1 - self.v2
        self.assertTrue(v.value, [2, 2, 0])
    
    def test_mul(self):
        true = self.assertTrue

        v3 = self.v1 * 2
        v4 = self.v2 * -2
        true(v3.value, [2, 2, 2])
        true(v4.value, [2, 2, -2])
    
    def test_div(self):
        true = self.assertTrue

        v3 = self.v1 / 0.5
        v4 = self.v2 / -0.5
        true(v3.value, [2, 2, 2])
        true(v4.value, [2, 2, -2])
    
    def test_iadd(self):
        self.v1 += self.v2
        self.assertTrue(self.v1, [0, 0, 2])
    
    def test_isub(self):
        self.v1 -= self.v2
        self.assertTrue(self.v1, [2, 2, 0])
    
    def test_imul(self):
        true = self.assertTrue

        self.v1 *= 2
        self.v2 *= -2
        true(self.v1.value, [2, 2, 2])
        true(self.v2.value, [2, 2, -2])
    
    def test_idiv(self):
        true = self.assertTrue

        self.v1 /= 0.5
        self.v2 /= -0.5
        true(self.v1.value, [2, 2, 2])
        true(self.v2.value, [2, 2, -2])