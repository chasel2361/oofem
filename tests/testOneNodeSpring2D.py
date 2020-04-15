# -*- coding: utf-8 -*-
"""author: 周光武、簡子琦"""
import unittest

from OneNodeSpring2D import OneNodeAxialSpring2D, OneNodeShearSpring2D, OneNodeRotationSpring2D
from Node import Node, Point
from Material import Material
from math import isclose
from numpy import array

class OneNodeAxialSpring2DTest(unittest.TestCase):
    def setUp(self):
        n = Node(1, Point())
        m = Material(1, 10, 10, 100)
        self.spring = OneNodeAxialSpring2D(1, n, m, 0, 0)
    
    def tearDown(self):
        self.spring = None
    
    def test_get_internal_force(self):
        sp = self.spring
        true = self.assertTrue
        dofs = sp.node1.dofs

        dofs[0].d_try = 1.5
        q = sp.get_internal_force('d_try', '')
        a = array([[15.0], [0.0], [0.0]])
        for i in range(3):
            true(isclose(q[i, 0], a[i, 0]))
        
        dofs[1].d_try = 7
        q = sp.get_internal_force('d_try', '')
        a = array([[15.0], [0.0], [0.0]])
        for i in range(3):
            true(isclose(q[i, 0], a[i, 0]))
        
        dofs[5].d_try = 3.2
        q = sp.get_internal_force('d_try', '')
        a = array([[15.0], [0.0], [0.0]])
        for i in range(3):
            true(isclose(q[i, 0], a[i, 0]))
        
        dofs[0].d_try = -2.6
        q = sp.get_internal_force('d_try', '')
        a = array([[-26.0], [0.0], [0.0]])
        for i in range(3):
            true(isclose(q[i, 0], a[i, 0]))
    
class OneNodeShearSpring2DTest(unittest.TestCase):
    def setUp(self):
        n = Node(1, Point())
        m = Material(1, 10, 10, 100)
        self.spring = OneNodeShearSpring2D(1, n, m, 0, 0)
    
    def tearDown(self):
        self.spring = None
    
    def test_get_internal_force(self):
        sp = self.spring
        true = self.assertTrue
        dofs = sp.node1.dofs

        dofs[0].d_try = 1.5
        q = sp.get_internal_force('d_try', '')
        a = array([[0.0], [0.0], [0.0]])
        for i in range(3):
            true(isclose(q[i, 0], a[i, 0]))
        
        dofs[1].d_try = 7.0
        q = sp.get_internal_force('d_try', '')
        a = array([[0.0], [70.0], [0.0]])
        for i in range(3):
            true(isclose(q[i, 0], a[i, 0]))
        
        dofs[5].d_try = 3.2
        q = sp.get_internal_force('d_try', '')
        a = array([[0.0], [70.0], [0.0]])
        for i in range(3):
            true(isclose(q[i, 0], a[i, 0]))
        
        dofs[1].d_try = -2.6
        q = sp.get_internal_force('d_try', '')
        a = array([[0.0], [-26.0], [0.0]])
        for i in range(3):
            true(isclose(q[i, 0], a[i, 0]))

class OneNodeRotationSpring2DTest(unittest.TestCase):
    def setUp(self):
        n = Node(1, Point())
        m = Material(1, 10, 10, 100)
        self.spring = OneNodeRotationSpring2D(1, n, m, 0, 0)
    
    def tearDown(self):
        self.spring = None
    
    def test_get_internal_force(self):
        sp = self.spring
        true = self.assertTrue
        dofs = sp.node1.dofs

        dofs[0].d_try = 1.5
        q = sp.get_internal_force('d_try', '')
        a = array([[0.0], [0.0], [0.0]])
        for i in range(3):
            true(isclose(q[i, 0], a[i, 0]))
        
        dofs[1].d_try = 7.0
        q = sp.get_internal_force('d_try', '')
        a = array([[0.0], [0.0], [0.0]])
        for i in range(3):
            true(isclose(q[i, 0], a[i, 0]))
        
        dofs[5].d_try = 3.2
        q = sp.get_internal_force('d_try', '')
        a = array([[0.0], [0.0], [32.0]])
        for i in range(3):
            true(isclose(q[i, 0], a[i, 0]))
        
        dofs[5].d_try = -2.6
        q = sp.get_internal_force('d_try', '')
        a = array([[0.0], [0.0], [-26.0]])
        for i in range(3):
            true(isclose(q[i, 0], a[i, 0]))

if __name__ == '__main__':
    unittest.main()