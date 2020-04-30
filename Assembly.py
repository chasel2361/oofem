from bisect import *
from scipy.sparse import dok_matrix


class Assembly:    
    def __init__(self, integrator): 
        self._integrator = integrator
        self._nodes = []
        self._elements = []
        self._sections = []
        self._materials = []
        self._seismics = []
        self._eq_number = 0

    
    @property
    def integrator(self):
        return self._integrator
    
    @property
    def nodes(self):
        return self._nodes
       
    @property
    def elements(self):
        return self._elements
    
    @property
    def sections(self):
        return self._sections

    @property
    def materials(self):
        return self._materials
    
    @property
    def seismics(self):
        return self._seismics
    
    @property
    def eq_number(self):
        return self._eq_number
    

    @property
    def lumped_mass(self):
        neq = self.eq_number
        mass_list = [dok_matrix((neq, neq)), [0] * neq]
        
        for e in self.elements:
            e_lumped = e.lumped_mass
            for i, dof in enumerate(e.dofs):
                if not dof.is_restrained:
                    dofeq = dof.eq_number
                    mass_list[0][dofeq, dofeq] += e_lumped[i, i]
        for n in self.nodes:
            dof_index = 0
            for i, dof in enumerate(n.dofs):
                if not dof.is_restrained:
                    mass_list[1][dof.eq_number] = dof_index
                dof_index += 1
        return mass_list
    

    def assign_eq_number(self):
        self._eq_number = 0
        
        for n in self.nodes:
            self._eq_number = n.assign_eq_number(self._eq_number)
    
    
    def node(self, id):
        nodes = self.nodes
        i = bisect_left(KeyifyList(nodes, lambda node: node.id), id)
        if i == len(nodes) or id != nodes[i].id:
            return None
        else:
            return nodes[i]

    def add_node(self, n):
        if n == None:
            return

        nodes = self.nodes
        id = n.id
        i = bisect_left(KeyifyList(nodes, lambda node: node.id), id)
        if i == len(nodes) or id != nodes[i].id:
            nodes.insert(i, n)
            return
    
    def element(self, id):
        elements = self.elements
        i = bisect_left(KeyifyList(elements, lambda element: element.id), id)
        if i == len(elements) or id != elements[i].id:
            return None
        else:
            return elements[i]
    
    def add_element(self, e):
        if e == None:
            return

        elements = self.elements
        id = e.id
        i = bisect_left(KeyifyList(elements, lambda element: element.id), id)
        if i == len(elements) or id != elements[i].id:
            elements.insert(i, e)
            return
    
    def section(self, id):
        sections = self.sections
        i = bisect_left(KeyifyList(sections, lambda section: section.id), id)
        if i == len(sections) or id != sections[i].id:
            return None
        else:
            return sections[i]
    
    def add_section(self, s):
        if s == None:
            return

        sections = self.sections
        id = s.id
        i = bisect_left(KeyifyList(sections, lambda section: section.id), id)
        if i == len(sections) or id != sections[i].id:
            sections.insert(i, s)
            return
    
    def material(self, id):
        materials = self.materials
        i = bisect_left(KeyifyList(materials, lambda material: material.id), id)
        if i == len(materials) or id != materials[i].id:
            return None
        else:
            return materials[i]
    
    def add_material(self, s):
        if s == None:
            return

        materials = self.materials
        id = s.id
        i = bisect_left(KeyifyList(materials, lambda material: material.id), id)
        if i == len(materials) or id != materials[i].id:
            materials.insert(i, s)
            return
    
    def get_internal_force(self, dof_type, pos_type):
        force_list = dok_matrix((self.eq_number, 1))

        for e in self.elements:
            e.assemble_force(dof_type, pos_type, force_list)
        return force_list
    
    def get_damp_force(self, dof_type, pos_type):
        force_list = dok_matrix((self.eq_number, 1))

        for e in self.elements:
            e.assemble_damp_force(dof_type, pos_type, force_list)
        return force_list
    
    def get_diagonal_stiffness(self, pos_type):
        stiffness_list = [0.0] * self.eq_number

        for e in self.elements:
            e.assemble_diagonal_stiffness(pos_type, stiffness_list)
        return stiffness_list
    
    # def K(self, k):
    #     for e in self.elements:
    #         e.assemble_lower_K(k)
    #     neq = self.eq_number
    #     for i in range(neq):
    #         for j in range(i + 1, neq):
    #             k[i, j] = k[j, i]
    
    def assemble_K(self, pos_type):
        neq = self.eq_number
        K = dok_matrix((neq, neq))
        for e in self.elements:
            dofs = e.dofs
            k = e.get_global_stiffness(pos_type)
            for i in range(len(dofs)):
                eq_num_i = dofs[i].eq_number
                if not eq_num_i == None:
                    for j in range(i+1):
                    # for j in range(len(dofs)):
                        eq_num_j = dofs[j].eq_number
                        if not eq_num_j == None:
                            if eq_num_i < eq_num_j:
                                K[eq_num_j, eq_num_i] += k[i, j]
                            else:
                                K[eq_num_i, eq_num_j] += k[i, j]
        neq = self.eq_number
        for i in range(neq):
            for j in range(i+1, neq):
                K[i, j] = K[j, i]
        return K
    
    # def assemble_internal_force(self, dof_type):
    #     neq = self.eq_number
    #     F = dok_matrix((neq, 1))
    #     for e in self.elements:
    #         dofs = e.dofs
    #         f = e.formal_get_internal_force(dof_type)
    #         for i in range(len(dofs)):
    #             eq_num_i = dofs[i].eq_number
    #             if not eq_num_i == None:
    #                 F[eq_num_i, 0] += f[i, 0]
    #     return F
    
    # def assemble_secant_stiffness(self):
    #     neq = self.eq_number
    #     K = dok_matrix((neq, neq))
    #     for e in self.elements:
    #         dofs = e.dofs
    #         k = e.get_secant_stiffness()
    #         for i in range(len(dofs)):
    #             eq_num_i = dofs[i].eq_number
    #             if not eq_num_i == None:
    #                 K[eq_num_i, eq_num_i] += k[i, i]
    #     return K

    
    def set_try_disp(self):
        for e in self.elements:
            e.set_try_disp()
    
    def get_dof(self, dof_type):
        neq = self.eq_number
        dof = dok_matrix((neq, 1))

        for n in self.nodes:
            n._get_dof(dof, dof_type)
        return dof

    def integrate(self, integrator):
        for n in self.nodes:
            n.integrate(integrator)
    
    def inc_d_try(self, delta_d):
        for n in self.nodes:
            n.inc_d_try(delta_d)
    
    def commit(self):
        for e in self.elements:
            e.commit()
        for n in self.nodes:
            n.commit()

    



class KeyifyList(object):
    def __init__(self, list, key_lambda):
        self.list = list
        self.key_lambda = key_lambda

    def __len__(self):
        return len(self.list)

    def __getitem__(self, i):
        return self.key_lambda(self.list[i])
