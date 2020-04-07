# -*- coding: utf-8 -*-
"""author: 周光武、簡子琦"""
class Section:
    """
    Section object to be assigned to linear element.

    Parameters
    ----------
    id : {section id, int}
    l_density : {linear density , float}
    E : {elasticity modulus, float}
    G : {shear modulus, float}
    A : {cross section area, float}
    I_y : {second moment of area in axis-y, float}
    I_z : {second moment of area in axis-z, float}
    J : {polar moment of inertia, float}
    
    """
    def __init__(self, id, l_density, E, G, A, I_y, I_z, J,):
        self.id = id
        self.l_density = l_density
        self.E = E
        self.G = G
        self.Area = A
        self.I_y = I_y
        self.I_z = I_z
        self.J = J
    
    def __repr__(self):
        return (f'\n{self.__class__.__name__} '
                f'id = {self.id}; '
                f'density = {self.l_density:6.3f}; '
                f'E = {self.E:10.4e}; '
                f'G = {self.G:10.4e}; '
                f'Area = {self.Area:10.4e}; '
                f'Iy = {self.I_y:10.4e}; '
                f'Iz = {self.I_z:10.4e}; '
                f'J = {self.J:10.4e}')