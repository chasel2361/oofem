# -*- coding: utf-8 -*-
"""author: 周光武、簡子琦"""
from Node import Node
from scipy.sparse import dok_matrix

class OneNodeSpring2D():
    """
    Abstract object of 2D one node spring element in X-Y plane.

    Parameters
    ----------
    id : {Element id, int}
    node1 : {Node to place spring, Node obj}
    material : {Spring material, Material obj}
    mass : {Spring mass, float}
    inertia : {Spring inertia, float}

    Returns
    -------
    out : OneNodeSpring2D obj

    """
    def __init__(self, id, node1, material, mass, inertia):
        self._id = id
        self._node1 = node1
        self._material = material
        self._stiffness = material.elastic_stiffness
        self._mass = mass
        self._inertia = inertia
        self._dofs = [node1.dof(0), node1.dof(1), node1.dof(5)]
    
    @property
    def id(self):
        return self._id
    
    @property
    def node1(self):
        return self._node1
    
    @property
    def material(self):
        return self._material
    
    @property
    def stiffness(self):
        return self._stiffness
    
    @property
    def mass(self):
        return self._mass
    
    @property
    def inertia(self):
        return self._inertia
    
    @property
    def dofs(self):
        return self._dofs
    
    @property
    def lumped_mass(self):
        mass = dok_matrix((3, 1))
        m = self.mass
        i = self.inertia
        mass[0, 0], mass[1, 0] = m, m
        mass[2, 0] = i
        return mass

    def dof(self, index):
        return self._dofs[index]
    
    def assemble_force(self, dof_type, pos_type, force):
        local_force = self.get_internal_force(dof_type, pos_type)
        for i, dof in enumerate(self.dofs):
            dof.assemble_force(force, local_force[i])
    
    def assemble_damp_force(self, dof_type, pos_type, force):
        return
    
    def get_internal_force(self, dof_type, pos_type):
        dofs = dok_matrix((3, 1))
        
        K = self.get_global_stiffness()
        for i, dof in enumerate(self.dofs):
            dofs[i, 0] = getattr(dof, dof_type)

        force = K * dofs
        return force
    
    def get_global_stiffness(self):
        return []
    
    def commit(self):
        return 
    
    def set_try_disp(self):
        return 
    
    def __repr__(self):
        return (f'{self.__class__.__name__} '
                f'node={self.node1.pos.value},')
    

class OneNodeAxialSpring2D(OneNodeSpring2D):
    """
    One node axial spring element in X-Y plane.

    Parameters
    ----------
    id : {element id, int}
    node1 : {node to place spring, Node obj}
    material : {spring material, Material obj}
    mass : {spring mass, float}
    inertia : {spring inertia, float}

    Returns
    -------
    out : OneNodeAxialSpring2D obj

    """
    
    def get_global_stiffness(self):
        K = dok_matrix((3, 3))
        K[0, 0] = self.stiffness
        return K

class OneNodeShearSpring2D(OneNodeSpring2D):
    """
    One node shear spring element in X-Y plane.

    Parameters
    ----------
    id : {element id, int}
    node1 : {node to place spring, Node obj}
    material : {spring material, Material obj}
    mass : {spring mass, float}
    inertia : {spring inertia, float}

    Returns
    -------
    out : OneNodeShearSpring2D obj

    """
    
    def get_global_stiffness(self):
        K = dok_matrix((3, 3))
        K[1, 1] = self.stiffness
        return K

class OneNodeRotationSpring2D(OneNodeSpring2D):
    """
    One node rotation spring element in X-Y plane.

    Parameters
    ----------
    id : {element id, int}
    node1 : {node to place spring, Node obj}
    material : {spring material, Material obj}
    mass : {spring mass, float}
    inertia : {spring inertia, float}

    Returns
    -------
    out : OneNodeRotationSpring2D obj

    """
    
    def get_global_stiffness(self):
        K = dok_matrix((3, 3))
        K[2, 2] = self.stiffness
        return K