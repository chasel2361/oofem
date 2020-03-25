# -*- coding: utf-8 -*-
"""author: 周光武、簡子琦"""
from .Frame2D import Frame2D, Vector, Point, Node
from numpy import matrix, zeros
from math import isclose

class Frame3D(Frame2D):
    """
    Abstract object of 3D-linear element.
    
    Parameters
    ----------
    id : {element id, int}
    node1 : {starting node, Node obj}
    node2 : {ending node, Node obj}
    section : {section property of element, Section obj}
    rayleigh : {rayleigh damping property a1, float}
    ref_x : {X coordinate of reference vector}
    ref_y : {Y coordinate of reference vector}
    ref_z : {Z coordinate of reference vector}

    Returns
    -------
    out: Frame3D

    """
    def __init__(self, id, node1, node2, section, rayleigh, ref_x, ref_y, ref_z):
        super().__init__(id, node1, node2, section, rayleigh)
        refvector = Vector(Point(), Point(ref_x, ref_y, ref_z))
        refvector.normalize()
        self._refvector = refvector
    
    @property
    def refvector(self):
        return self._refvector


    def rotation(self, matrix, pos_type):
        axis_1 = self._get_axial_vector(pos_type)
        axis_1.normalize()
        axis_2 = self.refvector.cross(axis_1)
        if axis_2.length < 1e-4:
            raise ValueError
        axis_2.normalize()
        axis_3 = axis_1.cross(axis_2)

        matrix[0, 0] = axis_1.x
        matrix[0, 1] = axis_1.y
        matrix[0, 2] = axis_1.z
        matrix[1, 0] = axis_2.x
        matrix[1, 1] = axis_2.y
        matrix[1, 2] = axis_2.z
        matrix[2, 0] = axis_3.x
        matrix[2, 1] = axis_3.y
        matrix[2, 2] = axis_3.z
    
    def rotation_t(self, matrix, pos_type):
        axis_1 = self._get_axial_vector(pos_type)
        axis_1.normalize()
        axis_2 = self.refvector.cross(axis_1)
        if axis_2.length < 1e-4:
            raise ValueError
        axis_2.normalize()
        axis_3 = axis_1.cross(axis_2)

        matrix[0, 0] = axis_1.x
        matrix[1, 0] = axis_1.y
        matrix[2, 0] = axis_1.z
        matrix[0, 1] = axis_2.x
        matrix[1, 1] = axis_2.y
        matrix[2, 1] = axis_2.z
        matrix[0, 2] = axis_3.x
        matrix[1, 2] = axis_3.y
        matrix[2, 2] = axis_3.z
        
    def orient_to_local(self, variable, pos_type):
        rot = matrix(zeros((3, 3)))
        self._orientation(rot, variable, pos_type, self.rotation)
    
    def orient_to_global(self, variable, pos_type):
        rot = matrix(zeros((3, 3)))
        self._orientation(rot, variable, pos_type, self.rotation_t)

    def _orientation(self, ga, variable, pos_type, rot_method):
        rot_method(ga, pos_type)
        v = ga * matrix(variable).T
        for i in range(3):
            variable[i] = v[i, 0]
    
