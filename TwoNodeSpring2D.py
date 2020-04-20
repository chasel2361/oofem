# -*- coding: utf-8 -*-
"""author: 周光武、簡子琦"""
from OneNodeSpring2D import OneNodeSpring2D
from Vector import Point, Vector
from numpy import matrix, zeros
from scipy.sparse import dok_matrix

class TwoNodeSpring2D(OneNodeSpring2D):
    """
    Abstract object of two node spring element in X-Y plane.

    Parameters
    ----------
    id : {Element index, int}
    node1 : {Starting Node, Node obj}
    node2 : {Ending Node, Node obj}
    material : {Spring material, Material obj}
    mass : {Spring mass, float}
    inertia : {Spring inertia, float}

    Returns
    -------
    out : TwoNodeSpring obj
    """
    def __init__(self, id, node1, node2, material, mass, inertia):
        super().__init__(id, node1, material, mass, inertia)
        self._node2 = node2
        self._dofs = [node1.dof(0), node1.dof(1), node1.dof(5),
                      node2.dof(0), node2.dof(1), node2.dof(5)]
    
    @property
    def node2(self):
        return self._node2
    
    @property
    def length_origin(self):
        return self.get_length('pos_origin')
    
    @property
    def lumped_mass(self):
        mass = dok_matrix((6, 1))
        m = self.mass
        i = self.inertia
        mass[0, 0], mass[1, 0], mass[3, 0], mass[4, 0] = m, m, m, m
        mass[2, 0], mass[5, 0] =  i, i
        return mass
    
    def get_length(self, pos_type):
        return self._get_axial_vector(pos_type).length

    def get_local_stiffness(self):
        return []

    def get_global_stiffness(self):
        K = self.get_local_stiffness()
        self.transform_to_global(K, 'pos_origin')
        return K
    
    def get_internal_force(self, dof_type, pos_type):
        dofs = dok_matrix((6, 1))
        
        K = self.get_global_stiffness()
        for i, dof in enumerate(self.dofs):
            dofs[i, 0] = getattr(dof, dof_type)

        force = K * dofs
        return force

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
        
        k = stiffness

        T = dok_matrix((6, 6))
        T[0, 0], T[1, 1], T[3, 3], T[4, 4] = c, c, c, c
        T[2, 2], T[5, 5] = 1, 1
        T[0, 1], T[3, 4] = s, s
        T[1, 0], T[4, 3] = -s, -s

        K = T.T*k*T
        for i in range(6):
            for j in range(6):
                stiffness[i, j] = K[i, j]
    
    def _get_axial_vector(self, pos_type):
        return Vector(getattr(self.node1, pos_type), getattr(self.node2, pos_type))


    def __repr__(self):
        return (f'\n{self.__class__.__name__} '
                f'id = {self.id}; '
                f'node1 = {self.node1.pos.value}; '
                f'node2 = {self.node2.pos.value}; '
                f'{self.material};')
    

class TwoNodeAxialSpring2D(TwoNodeSpring2D):
    
    def get_local_stiffness(self):
        k = dok_matrix((6, 6))
        stiffness = self.stiffness
        k[0, 0], k[3, 3] = stiffness, stiffness
        k[0, 3], k[3, 0] = -stiffness, -stiffness
        return k
        

class TwoNodeShearSpring2D(TwoNodeSpring2D):    
    """
    stiffness need to be fixed
    """
    
    
    """
    Two node shear spring element object in X-Y plane.

    Parameters
    ----------
    id : {Element index, int}
    node1 : {Starting Node, Node obj}
    node2 : {Ending Node, Node obj}
    material : {Spring material, Material obj}
    mass : {Spring mass, float}
    inertia : {Spring inertia, float}
    loc_ratio : {Shear location ratio, float}

    Returns
    -------
    out : TwoNodeAxialSpring obj
    
    """
    def __init__(self, id, node1, node2, material, mass, inertia, loc_ratio = 0.0):
        super().__init__(id, node1, node2, material, mass, inertia)
        self._shear_location_ratio = loc_ratio
    
    @property
    def shear_location_ratio(self):
        return self._shear_location_ratio
    
    def get_local_stiffness(self):
        stiffness = dok_matrix((6, 6))
        k = self.stiffness
        l0 = self.length_origin
        ls = self.shear_location_ratio * l0
        l0s = l0 - ls

        A1 = k
        A2 = l0s * k
        A3 = ls * k
        A4 = ls * l0s * k
        A5 = l0s**2 * k
        A6 = ls**2 * k
        stiffness[1, 1], stiffness[4, 4] = A1, A1
        stiffness[1, 4], stiffness[4, 1]= -A1, -A1
        stiffness[1, 2], stiffness[2, 1] = A2, A2
        stiffness[2, 4], stiffness[4, 2] = -A2, -A2
        stiffness[1, 5], stiffness[5, 1] = A3, A3
        stiffness[4, 5], stiffness[5, 4] = -A3, -A3
        stiffness[2, 5], stiffness[5, 2] = A4, A4
        stiffness[2, 2] = A5
        stiffness[5, 5] = A6
        return stiffness


class TwoNodeRotationSpring2D(TwoNodeSpring2D):

    def get_local_stiffness(self):
        k = dok_matrix((6, 6))
        stiffness = self.stiffness
        k[2, 2], k[5, 5] = stiffness, stiffness
        k[2, 5], k[5, 2] = -stiffness, -stiffness
        return k