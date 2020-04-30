# -*- coding: utf-8 -*-
"""author: 周光武、簡子琦"""
from math import isclose

class LinearMaterial:
    """
    LinearMaterial object to be assigned to elements.

    Parameters
    ----------
    id : {Material index, int}
    k : {Elastic stiffness, float}

    Returns
    -------
    out : LinearMaterial obj
    """
    def __init__(self, id, k):
        self._id = id
        self._elastic_stiffness = k
    
    @property
    def id(self):
        return self._id
    
    @property
    def elastic_stiffness(self):
        return self._elastic_stiffness

class BilinearMaterial(LinearMaterial):
    """
    BilinearMaterial object to be assigned to elements.

    Parameters
    ----------
    id : {Material index, int}
    k_e : {Elastic stiffness, float}
    k_i : {Inelastic stiffness, float}
    d_y : {yield displacement, float}

    Returns
    -------
    out : BilinearMaterial obj

    """
    def __init__(self, id, k_e, k_i, d_y):
        super().__init__(id, k_e)
        self._inelastic_stiffness = k_i
        self._yield_disp = d_y
        self._yield_force = d_y * k_e
        self._is_yielding = False
    
    @property
    def inelastic_stiffness(self):
        return self._inelastic_stiffness
    
    @property
    def yield_disp(self):
        return self._yield_disp
    
    @property
    def yield_force(self):
        return self._yield_force
    @yield_force.setter
    def yield_force(self, force):
        self._yield_force = force
    
    @property
    def degrade_disp(self):
        return self._yield_disp

    @property
    def degrade_force(self):
        return self._yield_force
    
    @property
    def is_yielding(self):
        return self._is_yielding
    @is_yielding.setter
    def is_yielding(self, boolean):
        self._is_yielding = boolean
    
    def get_yield_force(self, disp):
        return self.yield_force
    
    def yielding(self):
        self.is_yielding = True
    
    def __repr__(self):
        return (f'\n{self.__class__.__name__} '
                f'id = {self.id}; '
                f'k1 = {self.elastic_stiffness:11.5e}; '
                f'k2 = {self.inelastic_stiffness:11.5e}; '
                f'uy = {self.yield_disp:6.3f}')

class DegradingStrengthMaterial(BilinearMaterial):
    """
    Material object which will degradie strength.

    Parameters
    ----------
    id : {Material id, int}
    k_e : {Elastic stiffness, float}
    d_y : {Yield displacement, float}
    d_d : {Degrading displacement, float}
    f_d : {Strength after degrading, float}

    """
    def __init__(self, id, k_e, d_y, d_d, f_d):
        super().__init__(id, k_e)
        self._yield_disp = d_y
        self._degrade_disp = d_d
        self._degrade_force = f_d
        self._is_degrade = False

    @property
    def degrade_disp(self):
        return self._degrade_disp
    
    @property
    def degrade_force(self):
        return self._degrade_force
    
    @property
    def is_degrade(self):
        return self._is_degrade
    @is_degrade.setter
    def is_degrade(self, boolen):
        self._is_degrade = boolen
    
    def degrade(self):
        self.is_degrade = True

    def get_yield_force(self, disp):
        if abs(disp) > self.degrade_disp:
            self.degrade()
        if not self.is_degrade:
            return self.yield_force        
        return self.degrade_force
    
    def __repr__(self):
        return (f'\n{self.__class__.__name__} '
                f'id = {self.id}; '
                f'k1 = {self.elastic_stiffness:11.5e}; '
                f'uy = {self.yield_disp:9.3e}; '
                f'ud = {self.degrade_disp:5.3f}; '
                f'fd = {self.degrade_force:8.3f},')
