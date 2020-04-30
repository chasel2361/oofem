# -*- coding: utf-8 -*-
"""author: 周光武、簡子琦"""
# from .Frame2D import Frame2D
from Frame2D import Frame2D
from scipy.sparse import dok_matrix

class Beam2D(Frame2D):
    """
    Beam element in X-Y plane.

    Parameters
    ----------
    id : {Element index, int}
    node1 : {Starting node, Node obj}
    node2 : {Ending node, Node obj}
    section : {Section property of element, Section obj}
    rayleigh : {Rayleigh damping property a1, float}

    Returns
    -------
    out : Beam2D element obj

    """
    def __init__(self, id, node1, node2, section, rayleigh):
        super().__init__(id, node1, node2, section, rayleigh)
        self._dofs = [node1.dof(0), node1.dof(1), node1.dof(5),
                      node2.dof(0), node2.dof(1), node2.dof(5),]
    
    @property
    def lumped_mass(self):
        m = dok_matrix((6, 6))
        section = self.section
        mass = self.length_origin * section.l_density / 2
        inertia = mass * section.I_z / section.Area
        m[0, 0], m[1, 1], m[3, 3], m[4, 4] = mass, mass, mass, mass
        m[2, 2], m[5, 5] = inertia, inertia
        return m
    
    def get_internal_force(self, dof_type, pos_type):
        dofs = dok_matrix((6, 1))
        for i, dof in enumerate(self.dofs):
            dofs[i, 0] = getattr(dof, dof_type)
        k = self.get_global_stiffness(pos_type)
        force = k * dofs
        return force
    
    # def get_damp_force(self, dof_type, pos_type):
    #     dofs = [getattr(dof, dof_type) for dof in self.dofs]
    #     l0 = self.length_origin

    #     self.orient_to_local(dofs, pos_type)
    #     dv1 = dofs[3] - dofs[0]
    #     rig_rot = (dofs[4] - dofs[1]) / l0
    #     rot_a = dofs[2] - rig_rot
    #     rot_b = dofs[5] - rig_rot

    #     force = self._get_local_damp_force(dv1, rot_a, rot_b)
        
    #     self.orient_to_global(force, pos_type)
    #     return force
    
    # def assemble_force(self, dof_type, pos_type, force):
    #     local_force = self.get_internal_force(dof_type, pos_type)
    #     for i, dof in enumerate(self.dofs):
    #         dof.assemble_force(force, local_force[i])
    
    # def assemble_damp_force(self, dof_type, pos_type, force):
    #     local_force = self.get_damp_force(dof_type, pos_type)
    #     for i, dof in enumerate(self.dofs):
    #         dof.assemble_force(force, local_force[i])
    
    # def assemble_lower_K(self, K):
    #     k = self.get_global_stiffness()
    #     dofs = self.dofs
    #     for i in range(6):
    #         for j in range(i):
    #             K[dofs[i].eq_number, dofs[j].eq_number] += k[i][j]


    
    # def _get_local_damp_force(self, dv1, rot_a, rot_b):
    #     a1 =  self.rayleigh
    #     return [a1 * f for f in self._get_local_force(dv1, rot_a, rot_b)]
    
    def get_local_stiffness(self):
        section = self.section
        E = section.E
        A = section.Area
        Iz = section.I_z
        L0 = self.length_origin

        A1 = E*A/L0
        A2 = 12*E*Iz/L0**3
        A3 = 6*E*Iz/L0**2
        A4 = 4*E*Iz/L0
        A5 = 2*E*Iz/L0

        k = dok_matrix((6, 6))
        k[0, 0], k[3, 3] = A1, A1
        k[0, 3], k[3, 0] = -A1, -A1
        k[1, 1], k[4, 4] = A2, A2
        k[1, 4], k[4, 1] = -A2, -A2
        k[2, 4], k[4, 2], k[4, 5], k[5, 4] = A3, A3, A3, A3
        k[1, 2], k[2, 1], k[1, 5], k[5, 1] = -A3, -A3, -A3, -A3
        k[2, 2], k[5, 5] = A4, A4
        k[2, 5], k[5, 2] = A5, A5

        return k