# -*- coding: utf-8 -*-
"""author: 周光武、簡子琦"""
from Frame2D import Frame2D
from scipy.sparse import dok_matrix

class Truss2D(Frame2D):
    """
    Truss object of 2D-linear element in X-Y plane.

    Parameters
    ----------
    id : {element id, int}
    node1 : {starting node, Node obj}
    node2 : {ending node, Node obj}
    section : {section property of element, Section obj}
    rayleigh : {rayleigh damping property a1, float}

    Returns
    -------
    out : Truss2D element obj

    """
    def __init__(self, id, node1, node2, section, rayleigh):
        super().__init__(id, node1, node2, section, rayleigh)
        self._dofs = [node1.dof(0), node1.dof(1), node2.dof(0), node2.dof(1)]
    
    @property
    def lumped_mass(self):
        mass = dok_matrix((4, 1))
        m = self.length_origin * self.section.l_density / 2
        mass[0, 0], mass[1, 0], mass[2, 0], mass[3, 0] = m, m, m, m
        return mass
    
    def get_internal_force(self, dof_type, pos_type):
        dofs = dok_matrix((4, 1))
        for i, dof in enumerate(self.dofs):
            dofs[i, 0] = getattr(dof, dof_type)
        k = dok_matrix(super().get_global_stiffness(pos_type))
        force = k * dofs
        return  force
    
    def get_local_stiffness(self):
        section = self.section
        E = section.E
        A = section.Area
        L0 = self.length_origin
        k = dok_matrix((2, 2))
        A1 = E*A/L0
        k[0, 0], k[1, 1] = A1, A1
        k[0, 1], k[1, 0] = -A1, -A1
        return k
    
    def get_global_stiffness(self, pos_type):
        K = self.get_local_stiffness()
        self.transform_to_global(K, pos_type)
        return K
    
    def transform_to_global(self, stiffness, pos_type):
        k = dok_matrix((2, 2))
        axial_vector = self._get_axial_vector(pos_type)
        x = axial_vector.x
        y = axial_vector.y
        l = axial_vector.length
        c, s = x/l, y/l
        
        for i in range(2):
            for j in range(2):
                k[i, j] = stiffness[i, j]
                stiffness[i, j] = 0.0
        
        T = dok_matrix((2, 4))
        T[0, 0], T[1, 2] = c, c
        T[0, 1], T[1, 3] = s, s

        K = T.T * k * T
        stiffness.resize((4, 4))
        for i in range(4):
            for j in range(4):
                stiffness[i, j] = K[i, j]
