# -*- coding: utf-8 -*-
"""author: 周光武、簡子琦"""

class Point:
    """
    Point object.
    Return a point object with coordinate-X, Y and Z.

    Parameters
    ----------
    x : {coordinate-X of the point, float}
    y : {coordinate-Y of the point, float}
    z : {coordinate-Z of the point, float}

    Returns
    -------
    out: Point
        Point object with three coordinate.

    """
    def __init__(self, x:float = 0.0, y:float = 0.0, z:float = 0.0):
        self._x = x
        self._y = y
        self._z = z
    
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


    def __add__(self, pt):
        return Point(self.x + pt.x, self.y + pt.y, self.z + pt.z)
    
    def __iadd__(self, pt):
        self.x += pt.x
        self.y += pt.y
        self.z += pt.z
        return self
    
    def __sub__(self, pt):
        return Point(self.x - pt.x, self.y - pt.y, self.z - pt.z)
    
    def __isub__(self, pt):
        self.x -= pt.x
        self.y -= pt.y
        self.z -= pt.z
        return self
    
    def __mul__(self, constant):
        return Point(self.x * constant, self.y * constant, self.z * constant)
    
    def __imul__(self, constant):
        self.x *= constant
        self.y *= constant
        self.z *= constant
        return self
    
    def __truediv__(self, constant):
        return Point(self.x / constant, self.y / constant, self.z / constant)
    
    def __itruediv__(self, constant):
        self.x /= constant
        self.y /= constant
        self.z /= constant
        return self