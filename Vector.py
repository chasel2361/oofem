# -*- coding: utf-8 -*-
"""author: 周光武、簡子琦"""
from math import isclose, asin, acos
# from .Point import Point
from Point import Point

class Vector:
    """
    Vector object.
    Return a vector object with coordinate X, Y and Z by two point objects.

    Parameters
    ----------
    p1 : {Starting point of vector, Point object}
    p2 : {Ending point of vector, Point object}

    Returns
    -------
    out: Vector
        Vector object with three coordinate.

    """
    def __init__(self, p1:Point, p2:Point):
        self._x = p2.x - p1.x
        self._y = p2.y - p1.y
        self._z = p2.z - p1.z
    
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        self._x = value
    
    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        self._y = value
    
    @property
    def z(self):
        return self._z
    @z.setter
    def z(self, value):
        self._z = value
    
    @property
    def value(self):
        return [self.x, self.y, self.z]
    
    @property
    def length(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    """direction不精確，要想一個合理的名稱"""
    @property
    def direction(self):
        l = self.length
        assert l > 0, 'Vector length can\'t be zero!'
        x = self.x/l
        y = self.y/l
        z = self.z/l
        return Vector(Point(), Point(x, y, z))
    
    def normalize(self):
        l = self.length
        self.x /= l
        self.y /= l
        self.z /= l
    
    def dot(self, v):
        return self.x * v.x + self.y * v.y + self.z * v.z
    
    def cross(self, v):
        i = self.y * v.z - self.z * v.y
        j = self.z * v.x - self.x * v.z
        k = self.x * v.y - self.y * v.x
        return Vector(Point(0, 0, 0), Point(i, j, k))

    def rotation(self, v):
        cross = self.cross(v).length
        l = self.length * v.length
        if isclose(cross, l, rel_tol = 1e-15):
            cross = l
        return asin(cross/l)

    def __add__(self, vector):
        p = Point(self.x + vector.x, self.y + vector.y, self.z + vector.z)
        return Vector(Point(), p)
    
    def __iadd__(self, vector):
        self.x += vector.x
        self.y += vector.y
        self.z += vector.z
        return self
    
    def __sub__(self, vector):
        p = Point(self.x - vector.x, self.y - vector.y, self.z - vector.z)
        return Vector(Point(), p)
    
    def __isub__(self, vector):
        self.x -= vector.x
        self.y -= vector.y
        self.z -= vector.z
        return self
    
    def __mul__(self, constant):
        p = Point(self.x * constant, self.y * constant, self.z * constant)
        return Vector(Point(), p)
    
    def __imul__(self, constant):
        self.x *= constant
        self.y *= constant
        self.z *= constant
        return self
    
    def __truediv__(self, constant):
        p = Point(self.x / constant, self.y / constant, self.z * constant)
        return Vector(Point(), p)
    
    def __itruediv__(self, constant):
        self.x /= constant
        self.y /= constant
        self.z /= constant
        return self