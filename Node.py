# -*- coding: utf-8 -*-
"""author: 周光武、簡子琦"""
from Vector import Vector
from Point import Point
from Dof import ActiveDof, BoundaryDof

class Node:
    """
    Node object to be assigned to elements

    Parameters
    ----------
    id : {element id, int}
    p : {node coordinate, Point obj}

    Returns
    -------
    out : Node obj

    """
    def __init__(self, id , p):
        self._id = id
        self._pos = p
        self._dofs = [ActiveDof() for n in range(6)] 
    
    @property
    def id(self):
        return self._id
    
    @property
    def dofs(self):
        return self._dofs
    
    @property
    def pos(self):
        return self._get_pos('d')
        
    @property
    def pos_last(self):
        return self._get_pos('d_last')
    
    @property
    def pos_try(self):
        return self._get_pos('d_try')
    
    @property
    def pos_try_last(self):
        return self._get_pos('d_try_last')
    
    @property
    def pos_origin(self):
        return self._pos
    
###
# 找時間改成restrain(type)
    def restrain_dof(self, i):
        """
        Restrain specific dof in Node.

        Parameters
        ----------
        i : {number of dof, int}

        """
        self.dofs[i] = BoundaryDof()
        
    def restrain(self):
        """
        Restrain all dofs in Node.

        """
        dofs = self.dofs
        for i in range(6):
            dofs[i] = BoundaryDof()
###
    
    def assign_eq_number(self, eq_number):
        """
        Assign equation number to every ActiveDof in Node.

        Parameters
        ----------
        eq_number : {equation number to be assign, int}

        """
        for dof in self._dofs:
            if dof.is_restrained == True:
                continue
            else:
                dof.eq_number = eq_number
                eq_number += 1

        return eq_number
    
    def dof(self, index):
        """
        Get value of specific dof in Node.

        Parameters
        ----------
        index : {index of dof, int}

        Returns
        -------
        out : float
        """
        return self._dofs[index]

    def modify_dof(self, index, dof):
        """
        Modify specific dof.

        Parameters
        ----------
        index : {index of dof, int}
        dof : {new dof, dof obj}

        """
        self._dofs[index] = dof
        
    def integrate(self, integrator):
        """
        Integrate the dof value in Node.

        Parameters
        ----------
        integrator : {time integrator, integrator obj}

        """
        for dof in self.dofs:
            dof.integrate(integrator)
            
    def inc_d_try(self, delta_d):
        """
        Increase delta_d into d_try.

        Parameters
        ----------
        delta_d : {increment of d_try, float}

        """
        for dof in self.dofs:
            dof.inc_d_try(delta_d)
    
    def commit(self):
        """
        Commit all dofs value.
        
        """
        for dof in self.dofs:
            dof.commit()
        
        
    def _get_pos(self, d_type):
        dofs = self.dofs
        pos = self._pos
        return pos + Point(getattr(dofs[0], d_type), getattr(dofs[1], d_type), getattr(dofs[2], d_type))

    def _get_dof(self, dof, d_type):
        for d in self.dofs:
            d._get_dof(dof, d_type)

    def __repr__(self):
        dof = self.dof
        return (f'\n{self.__class__.__name__} '
                f'id = {self.id}; '
                f'pos = {self.pos.value}\n'
                f'dofs = {dof(0), dof(1), dof(2)}\n       {dof(3), dof(4), dof(5)}')