# -*- coding: utf-8 -*-
"""author: 周光武、簡子琦"""
import unittest

from Frame2D import Frame2D, Node, Point
from Section import Section
from math import isclose, pi

class Frame2DTest(unittest.TestCase):
    def setUp(self):
        n1 = Node(1, Point())
        n2 = Node(2, Point(1, 1))
        material = Section(1, 1, 10000, 0, 100, 1000, 1000, 2000)
        self.frame = Frame2D(1, n1, n2, material, 0)

    def tearDown(self):
        self.frame = None
    
    def test_length(self):
        frame = self.frame
        dofs1 = frame.node1.dofs
        dofs2 = frame.node2.dofs
        true = self.assertTrue

        dofs1[0].d = dofs1[1].d = 1
        dofs1[0].d_last = dofs1[1].d_last = -1
        dofs2[0].d_try = dofs2[1].d_try  = 2
        dofs2[0].d_try_last = 2
        dofs2[1].d_try_last = -2

        true(isclose(frame.get_length('pos_origin'), 2**0.5))
        true(isclose(frame.get_length('pos'), 0.0))
        true(isclose(frame.get_length('pos_last'), 8**0.5))
        true(isclose(frame.get_length('pos_try'), 18**0.5))
        true(isclose(frame.get_length('pos_try_last'), 10**0.5))
    
    def test_elongation(self):
        frame = self.frame
        dofs1 = frame.node1.dofs
        dofs2 = frame.node2.dofs
        true = self.assertTrue

        dofs1[0].d = dofs1[1].d = 1
        dofs1[0].d_last = dofs1[1].d_last = -1
        dofs2[0].d_try = dofs2[1].d_try = 2
        dofs2[0].d_try_last = 2
        dofs2[1].d_try_last = -2

        true(isclose(frame._get_elongation('pos'), -2**0.5))
        true(isclose(frame._get_elongation('pos_last'), 2**0.5))
        true(isclose(frame._get_elongation('pos_try'), 8**0.5))
        true(isclose(frame._get_elongation('pos_try_last'), 10**0.5 - 2**0.5))

    def test_get_axial_vector(self):
        frame = self.frame
        dofs1 = frame.node1.dofs
        dofs2 = frame.node2.dofs
        axial = frame._get_axial_vector
        true = self.assertTrue

        dofs2[0].d = -1
        dofs2[1].d = 0
        dofs1[0].d_last = 0
        dofs1[1].d_last = 1
        dofs1[0].d_try = 1
        dofs2[1].d_try = 0
        
        pos_type = ['pos_origin', 'pos', 'pos_last', 'pos_try', 'pos_try_last']
        question = [axial(pos).value for pos in pos_type]
        
        ans = [[1, 1, 0],
               [0, 1, 0], 
               [1, 0, 0],
               [0, 1, 0],
               [1, 1, 0]]        

        for (que, an) in zip(question, ans):
            for (q, a) in zip(que, an):
                true(isclose(q, a))
    
    # def test_rigid_rotation(self):
    #     frame = self.frame
    #     dofs1 = frame.node1.dofs
    #     dofs2 = frame.node2.dofs
    #     true = self.assertTrue

    #     dofs2[0].d_last = -1
    #     dofs2[1].d_try = -1
    #     dofs1[2].d_try_last = 1

    #     question = []
    #     for pos in ['pos', 'pos_last', 'pos_try', 'pos_try_last']:
    #         question.append(frame._get_rigid_rotation(pos))
        
    #     answer = [0, 0.43520987568, -0.43520987568, 0]

    #     for (q, a) in zip(question, answer):
    #         true(isclose(q, a))
    
    def test_orient_to_local(self):
        frame = self.frame
        true = self.assertTrue
        question = [-1, -1, -1, 1, 1, 1]
        frame.orient_to_local(question, 'pos_origin')
        answer = [-2**0.5, 0, -1, 2**0.5, 0, 1]

        for (q, a) in zip(question, answer):
            true(isclose(q, a))
    
    def test_orient_to_global(self):
        frame = self.frame
        true = self.assertTrue
        question = [-2**0.5, 0, -1, 2**0.5, 0, 1]

        frame.orient_to_global(question, 'pos_origin')
        answer = [-1, -1, -1, 1, 1, 1]

        for (q, a) in zip(question, answer):
            true(isclose(q, a))

    def test_transform_to_global(self):
        n1 = Node(1, Point())
        n2 = Node(2, Point(4, 3))
        frame = Frame2D(1, n1, n2, 0, 0)
        true = self.assertTrue

        question = [
            [2000,  0,      0,      -2000,  0,      0],
            [0,     12,     -6,     0,      -12,    -6],
            [0,     -6,     4,      0,      6,      2],
            [-2000, 0,      0,      2000,   0,      0],
            [0,     -12,    6,      0,      12,     6],
            [0,     -6,     2,      0,      6,      4]
        ]
        frame.transform_to_global(question, 'pos_origin')

        answer = [
            [1284.32,   954.24,     3.6,    -1284.32,   -954.24,    3.6],
            [954.24,    727.68,     -4.8,   -954.24,    -727.68,    -4.8],
            [3.6,       -4.8,       4,      -3.6,       4.8,        2],
            [-1284.32,  -954.24,    -3.6,   1284.32,    954.24,     -3.6],
            [-954.24,   -727.68,    4.8,    954.24,     727.68,     4.8],
            [3.6,       -4.8,       2,      -3.6,       4.8,        4]
        ]
        
        for (que, ans) in zip(question, answer):
            for (q, a) in zip(que, ans):
                true(isclose(q, a))

if __name__ == '__main__':
    unittest.main()