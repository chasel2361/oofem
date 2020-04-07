# -*- coding: utf-8 -*-
"""author: 周光武、簡子琦"""
from Point import Point
from Vector import Vector
from Node import Node
from math import isclose
from numpy import matrix

class Frame2D:
    """
    Abstract object of 2D-linear element in X-Y plane.
    
    Parameters
    ----------
    id : {element id, int}
    node1 : {starting node, Node obj}
    node2 : {ending node, Node obj}
    section : {section property of element, Section obj}
    rayleigh : {rayleigh damping property a1, float}

    Returns
    -------
    out : Frame2D element obj

    """
    def __init__(self, id, node1, node2, section, rayleigh):
        self._id = id
        self._node1 = node1
        self._node2 = node2
        self._section = section
        self._rayleigh = rayleigh
        self._dofs = [node1.dof(0), node1.dof(1), node1.dof(5),
                      node2.dof(0), node2.dof(1), node2.dof(5),]
    
    @property
    def id(self):
        return self._id
    
    @property
    def dofs(self):
        return self._dofs
    
    @property
    def node1(self):
        return self._node1
    @node1.setter
    def node1(self, n):
        # assert type(n) == type(Node)
        self._node1 = n
    
    @property
    def node2(self):
        return self._node2
    @node2.setter
    def node2(self, n):
        # assert type(n) == type(Node)
        self._node2 = n
    
    @property
    def section(self):
        return self._section
    @section.setter
    def section(self, s):
        # assert type(m) = type(section)
        self._section = s
    
    @property
    def rayleigh(self):
        return self._rayleigh
    
    @property
    def length_origin(self):
        return self.get_length('pos_origin')
    
    def get_internal_force(self, dof_type, pos_type):
        return []
    
    def dof(self, index):
        return self._dofs[index]

    def get_length(self, pos_type):
        return self._get_axial_vector(pos_type).length
    
    def set_try_disp(self):
        return
    
    def commit(self):
        return 
    
    def orient_to_local(self, variable, pos_type):
        axial_vector = self._get_axial_vector(pos_type)
        x = axial_vector.x
        y = axial_vector.y
        l = axial_vector.length
        c, s = x/l, y/l

        v = [n for n in variable]

        variable[0] = v[0]*c + v[1]*s
        variable[1] = -v[0]*s + v[1]*c
        variable[3] = v[3]*c + v[4]*s
        variable[4] = -v[3]*s + v[4]*c
    
    def orient_to_global(self, variable, pos_type):
        axial_vector = self._get_axial_vector(pos_type)
        x = axial_vector.x
        y = axial_vector.y
        l = axial_vector.length
        c, s = x/l, y/l

        v = [n for n in variable]

        variable[0] = v[0]*c - v[1]*s
        variable[1] = v[0]*s + v[1]*c
        variable[3] = v[3]*c - v[4]*s
        variable[4] = v[3]*s + v[4]*c
    
    def transform_to_global(self, stiffness, pos_type):
        axial_vector = self._get_axial_vector(pos_type)
        x = axial_vector.x
        y = axial_vector.y
        l = axial_vector.length
        c, s = x/l, y/l
        k = matrix(stiffness)

        T = matrix([
            [c,   s,   0.0, 0.0, 0.0, 0.0],
            [-s,  c,   0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, c,   s,   0.0],
            [0.0, 0.0, 0.0, -s,  c,   0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
        ])

        K = T.T*k*T
        for i in range(6):
            for j in range(6):
                stiffness[i][j] = K[i,j]
    
    def _get_axial_vector(self, pos_type):
        return Vector(getattr(self.node1, pos_type), getattr(self.node2, pos_type))

    def _get_elongation(self, pos_type):
        l0 = self.length_origin
        l = self.get_length(pos_type)
        return (l**2 - l0**2)/(l + l0)
    
    def assemble_force(self, dof_type, pos_type, force):
        local_force = self.get_internal_force(dof_type, pos_type)
        for i, dof in enumerate(self.dofs):
            dof.assemble_force(force, local_force[i])


    def __repr__(self):
        return (f'\n{self.__class__.__name__} '
                f'id = {self.id}; '
                f'node1 = {self.node1.pos.value}; '
                f'node2 = {self.node2.pos.value},')