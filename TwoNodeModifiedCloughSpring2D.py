# -*- coding: utf-8 -*-
"""author: 周光武、簡子琦"""
from TwoNodeSpring2D import TwoNodeSpring2D, dok_matrix

class TwoNodeModifiedCloughSpring2D(TwoNodeSpring2D):
    """
    Abstrace object of two node spring element which follow 
    the rule of Modified-Clough Behavior in inelastic stage 
    in X-Y plane.

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
    out : TwoNodeModifiedCloughSpring obj

    """
    def __init__(self, id, node1, node2, material, mass, inertia): #shear_location_ratio = 0.0):
        super().__init__(id, node1, node2, material, mass, inertia)
        
        self._dofs = [node1.dof(0), node1.dof(1), node1.dof(5),
                      node2.dof(0), node2.dof(1), node2.dof(5)]
        
        uy = material.yield_disp
        fy = material.degrade_force
        k1 = material.elastic_stiffness

        self._disp = 0.0
        self._last_disp = 0.0
        self._try_disp = 0.0
        self._try_last_disp = 0.0
        self._try_extreme_disp = [-uy, uy]
        self._extreme_disp = [-uy, uy]
        self._try_nonforce_disp = [0.0, 0.0]
        self._nonforce_disp = [0.0, 0.0]
        self._try_inner_peak_disp = 0.0
        self._inner_peak_disp = 0.0

        self._force = 0.0        
        self._last_force = 0.0
        self._try_force = 0.0
        self._try_last_force = 0.0
        self._try_extreme_force = [-fy, fy]
        self._extreme_force = [-fy, fy]
        self._try_inner_peak_force = 0.0
        self._inner_peak_force = 0.0
        
        self._elastic_stiffness = k1
        self._post_yield_stiffness = material.inelastic_stiffness
        self._unloading_stiffness = k1

        self._phase = 2
        self._stage_index = 1
        self._try_stage_index = 1

        self._stage = {
            1: lambda x: self.stage_elastic(x),
            2: lambda x: self.stage_beyond_yield(x),
            3: lambda x: self.stage_unloading_from_yield(x),
            4: lambda x: self.stage_reloading_toward_yield(x),
            5: lambda x: self.stage_unloading_from_inner_peak(x),
        }

        self._dict_force = {
            'd': self.force,
            'd_last': self.last_force,
            'd_try': self.try_force,
            'd_try_last': self.try_last_force,
        }
    
    def set_try_disp(self):
        self.try_extreme_disp
        return

    def get_internal_force(self, dof_type, pos_type):
        return
    
    def get_local_stiffness(self):
        return []    

    def get_global_stiffness(self, pos_type):
        stiffness = self.get_local_stiffness()
        self.transform_to_global(stiffness, 'pos_origin')
        return stiffness
    
    
    @property
    def disp(self):
        return self._disp
    @disp.setter
    def disp(self, disp):
        self._disp = disp
    
    @property
    def last_disp(self):
        return self._last_disp
    @last_disp.setter
    def last_disp(self, disp):
        self._last_disp = disp
    
    @property
    def try_disp(self):
        return self._try_disp
    @try_disp.setter
    def try_disp(self, disp):
        self._try_disp = disp
    
    @property
    def try_last_disp(self):
        return self._try_last_disp
    @try_last_disp.setter
    def try_last_disp(self, disp):
        self._try_last_disp = disp
    
    @property
    def try_extreme_disp(self):
        return self._try_extreme_disp
    def update_try_extreme_disp(self, phase, disp):
        self._try_extreme_disp[phase-1] = disp
    def reset_try_extreme_disp(self, phase):
        self._try_extreme_disp[phase-1] = self.get_extreme_disp(phase)
    
    @property
    def extreme_disp(self):
        return self._extreme_disp
    def update_extreme_disp(self, phase, disp):
        self._extreme_disp[phase-1] = disp
    
    @property
    def try_nonforce_disp(self):
        return self._try_nonforce_disp
    def update_try_nonforce_disp(self, phase, disp):
        self._try_nonforce_disp[phase-1] = disp
    def reset_try_nonforce_disp(self, phase):
        self._try_nonforce_disp[phase-1] = self.get_nonforce_disp(phase)

    @property
    def nonforce_disp(self):
        return self._nonforce_disp
    def update_nonforce_disp(self, phase, disp):
        self._nonforce_disp[phase-1] = disp
    
    @property
    def try_inner_peak_disp(self):
        return self._try_inner_peak_disp
    @try_inner_peak_disp.setter
    def try_inner_peak_disp(self, disp):
        self._try_inner_peak_disp = disp

    @property
    def inner_peak_disp(self):
        return self._inner_peak_disp
    @inner_peak_disp.setter
    def inner_peak_disp(self, disp):
        self._inner_peak_disp = disp
    
    @property
    def force(self):
        return self._force
    @force.setter
    def force(self, force):
        self._force = force
    
    @property
    def last_force(self):
        return self._last_force
    @last_force.setter
    def last_force(self, force):
        self._last_force = force
    
    @property
    def try_force(self):
        return self._try_force
    @try_force.setter
    def try_force(self, force):
        self._try_force = force
    
    @property
    def try_last_force(self):
        return self._try_last_force
    @try_last_force.setter
    def try_last_force(self, force):
        self._try_last_force = force
    
    @property
    def try_extreme_force(self):
        return self._try_extreme_force
    def update_try_extreme_force(self, phase, force):
        self._try_extreme_force[phase-1] = force
    def reset_try_extreme_force(self, phase):
        self._try_extreme_force[phase-1] = self.get_extreme_force(phase)
    
    @property
    def extreme_force(self):
        return self._extreme_force    
    def update_extreme_force(self, phase, force):
        self._extreme_force[phase-1] = force
    
    @property
    def try_inner_peak_force(self):
        return self._try_inner_peak_force
    @try_inner_peak_force.setter
    def try_inner_peak_force(self, force):
        self._try_inner_peak_force = force

    @property
    def inner_peak_force(self):
        return self._inner_peak_force
    @inner_peak_force.setter
    def inner_peak_force(self, force):
        self._inner_peak_force = force
    
    @property
    def elastic_stiffness(self):
        return self._elastic_stiffness
    
    @property
    def post_yield_stiffness(self):
        return self._post_yield_stiffness
    @post_yield_stiffness.setter
    def post_yield_stiffness(self, stiffness):
        self._post_yield_stiffness = stiffness

    @property
    def unloading_stiffness(self):
        return self._unloading_stiffness

    @property
    def phase(self):
        return self._phase
    @phase.setter
    def phase(self, phase):
        self._phase = phase
    
    @property
    def stage_index(self):
        return self._stage_index
    @stage_index.setter
    def stage_index(self, index):
        self._stage_index = index
    
    @property
    def try_stage_index(self):
        return self._try_stage_index
    @try_stage_index.setter
    def try_stage_index(self, index):
        self._try_stage_index = index
    
    @property
    def sign(self):
        return 2.0*self.phase - 3
    
    @property
    def stage(self):
        return self._stage
    
    @property
    def dict_force(self):
        return self._dict_force
    
    def get_try_extreme_disp(self, phase):
        return self.try_extreme_disp[phase-1]

    def get_extreme_disp(self, phase):
        return self.extreme_disp[phase-1]
    
    def get_try_nonforce_disp(self, phase):
        return self.try_nonforce_disp[phase-1]
    
    def get_nonforce_disp(self, phase):
        return self.nonforce_disp[phase-1]
    
    def get_try_extreme_force(self, phase):
        return self.try_extreme_force[phase-1]

    def get_extreme_force(self, phase):
        return self.extreme_force[phase-1]
    
    def get_try_reloading_stiffness(self, phase):
        return self.get_try_extreme_force(phase) / (self.get_try_extreme_disp(phase) - self.get_try_nonforce_disp(3 - phase))
    
    def get_reloading_stiffness(self, phase):
        return self.get_extreme_force(phase) / (self.get_extreme_disp(phase) - self.get_nonforce_disp(3 - phase))
    
    def change_phase(self):
        self.phase = 3 - self.phase

    def commit(self):
        phase = self.phase
        try_disp = self.try_disp
        try_force = self.try_force
        force = self.force
        self.last_disp = self.disp
        self.last_force = force
        self.disp = try_disp
        self.force = try_force
        self.inner_peak_disp = self.try_inner_peak_disp
        self.inner_peak_force = self.try_inner_peak_force
        self.update_extreme_disp(phase, self.get_try_extreme_disp(phase))
        self.update_extreme_force(phase, self.get_try_extreme_force(phase))
        self.update_nonforce_disp(phase, self.get_try_nonforce_disp(phase))
        self.dict_force['d'] = try_force
        self.dict_force['d_last'] = force
        self.stage_index = self.try_stage_index
    

    def update_try_variable(self, disp, force):
        try_force = self.try_force
        self.try_last_disp = self.try_disp
        self.try_last_force = try_force
        self.try_disp = disp
        self.try_force = force
        self.dict_force['d_try'] = force
        self.dict_force['d_try_last'] = try_force
        

    def stage_elastic(self, disp):
        m = self.material
        
        if disp < 0:
            self.phase = 1
        else:
            self.phase = 2

        # 當前轉角 >= 降伏轉角 (進入塑性階段)
        if m.yield_disp <= abs(disp):            
            self.try_stage_index = 2
            self.stage_beyond_yield(disp)

        # 仍在彈性階段
        else:
            force = self.elastic_stiffness * disp
            self.update_try_variable(disp, force)
            # return force
    
    def stage_beyond_yield(self, disp):
        last_disp = self.disp
        phase = self.phase
        sign = self.sign

        self.reset_try_extreme_disp(phase)
        self.reset_try_extreme_force(phase)
        self.reset_try_nonforce_disp(phase)

        # 當前轉角 < 前步轉角 (卸載)
        if (disp - last_disp)*sign < 0:

            # 更新當前方向極值座標
            extreme_disp = last_disp
            extreme_force = self.force
            self.update_try_extreme_disp(phase, extreme_disp)
            self.update_try_extreme_force(phase, extreme_force)
            
            # 計算力為零轉角
            nonforce_disp = extreme_disp - extreme_force/self.unloading_stiffness
            self.update_try_nonforce_disp(phase, nonforce_disp)


            # 力為零轉角 < 當前轉角(沒有卸過頭)
            if (self.get_try_nonforce_disp(phase) - disp)*sign < 0:
                self.try_stage_index = 3
                self.stage_unloading_from_yield(disp)

            # (卸過頭)
            else:
                self.unload_toward_another_phase(disp)

        # (加載)
        else:
            m = self.material
            force = sign * m.get_yield_force(disp) + (disp - sign * m.yield_disp) * self.post_yield_stiffness
            self.update_try_variable(disp, force)
            # return force
    
    def stage_unloading_from_yield(self, disp):
        phase = self.phase
        sign = self.sign

        # 力為零轉角 < 當前轉角 (沒有卸過頭)
        if (self.get_try_nonforce_disp(phase) - disp)*sign < 0:
            
            # 極值轉角 <= 當前轉角 (降伏)
            if (self.get_try_extreme_disp(phase) - disp)*sign <= 0:
                self.try_stage_index = 2
                self.stage_beyond_yield(disp)
            
            # (未降伏)
            else:
                force = self.get_try_extreme_force(phase) - (self.get_try_extreme_disp(phase) - disp) * self.unloading_stiffness
                self.update_try_variable(disp, force)
                # return force
        
        # (卸過頭)
        else:
            self.unload_toward_another_phase(disp)

    def stage_reloading_toward_yield(self, disp):
        phase = self.phase
        sign = self.sign

        self.reset_try_nonforce_disp(phase)
        self.try_inner_peak_disp = self.inner_peak_disp
        self.try_inner_peak_force = self.inner_peak_force

        # 卸載
        if (disp - self.disp) * sign < 0:

            # 更新內部頂點座標
            self.try_inner_peak_disp = self.disp
            self.try_inner_peak_force = self.force
            nonforce_disp = self.try_inner_peak_disp - self.try_inner_peak_force/self.unloading_stiffness
            self.update_try_nonforce_disp(self.phase, nonforce_disp)

            # 力為零轉角 < 當前轉角 (沒有卸過頭)
            if (self.get_try_nonforce_disp(phase) - disp) * sign < 0:
                self.try_stage_index = 5
                self.stage_unloading_from_inner_peak(disp)

            # (卸過頭)
            else:
                self.unload_toward_another_phase(disp)

        # 加載
        else:

            # 極值轉角 < 當前轉角 (降伏)
            if (self.get_try_extreme_disp(phase) - disp)*sign < 0:
                self.try_stage_index = 2
                self.stage_beyond_yield(disp)
            
            # (未降伏)
            else:
                force = self.get_try_reloading_stiffness(phase) * (disp - self.get_try_nonforce_disp(3 - phase))
                self.update_try_variable(disp, force)
    
    def stage_unloading_from_inner_peak(self, disp):
        phase = self.phase
        sign = self.sign

        # 力為零轉角 < 當前轉角 (沒有卸過頭)
        if (self.get_try_nonforce_disp(phase) - disp) * sign < 0:

            # inner peak 轉角 <= 當前轉角
            if (self.try_inner_peak_disp - disp)*sign <= 0:

                # 極值轉角 < 當前轉角 (降伏)
                if (self.get_try_extreme_disp(phase) - disp)*sign <= 0:
                    self.try_stage_index = 2
                    self.stage_beyond_yield(disp)
                
                # (未降伏)
                else:
                    self.try_stage_index = 4
                    self.stage_reloading_toward_yield(disp)
            
            else:
                force = self.try_inner_peak_force - (self.try_inner_peak_disp - disp)*self.unloading_stiffness
                self.update_try_variable(disp, force)
                # return force

        # (卸過頭)
        else:
            self.unload_toward_another_phase(disp)

    def unload_toward_another_phase(self, disp):
        # 改變phase
        self.change_phase()
        phase = self.phase

        # 極值轉角 < 當前轉角 (降伏)
        if (self.get_try_extreme_disp(phase) - disp)*self.sign < 0:
            self.try_stage_index = 2
            self.stage_beyond_yield(disp)
            
        # (未降伏)
        else:
            self.try_stage_index = 4
            self.stage_reloading_toward_yield(disp)
    
    # def __repr__(self):
    #     return (f'\n{self.__class__.__name__} '
    #             f'id = {self.id}; '
    #             f'node1 = {self.node1.pos.value}; '
    #             f'node2 = {self.node2.pos.value}; '
    #             f'material = {self.material}')
    

class TwoNodeModifiedCloughAxialSpring2D(TwoNodeModifiedCloughSpring2D):
    def __init__(self, id, node1, node2, material, mass, inertia, ref_x, ref_y, ref_z, shear_location_ratio = 0.0):
        super().__init__(id, node1, node2, material, mass, inertia, ref_x, ref_y, ref_z)
    
    def set_try_disp(self):
        dofs = [getattr(dof, 'd_try') for dof in self.dofs]
        self.orient_to_local(dofs, 'pos_try')
        elongation = dofs[6] - dofs[0]

        stage_index = self.stage_index
        self.stage[stage_index](elongation)
    
    def get_internal_force(self, dof_type, pos_type):
        dofs = [getattr(dof, dof_type) for dof in self.dofs]
        self.orient_to_local(dofs, pos_type)

        force = self.dict_force[dof_type]
        f_1_a = -force
        f_1_b = force
        force = [f_1_a, 0.0, 0.0, 0.0, 0.0, 0.0, f_1_b, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.orient_to_global(force, pos_type)
        return force
    
    def get_global_stiffness(self):
        index = self.stage_index
        if index == 1 or index == 3 or index == 5:
            k = self.elastic_stiffness
        if self.stage_index == 2:
            k = self.post_yield_stiffness
        if self.stage_index == 4:
            k = self.get_reloading_stiffness(self.phase)
        return [
            [k  , 0.0, 0.0, -k , 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [-k , 0.0, 0.0, k  , 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        ]


###跑出來的圖有點怪怪，可能是shear_disp的關係
class TwoNodeModifiedCloughShearSpring2D(TwoNodeModifiedCloughSpring2D):
    def __init__(self, id, node1, node2, material, mass, inertia, ref_x, ref_y, ref_z, shear_location_ratio = 0.0):
        super().__init__(id, node1, node2, material, mass, inertia, ref_x, ref_y, ref_z)
    
    def set_try_disp(self):
        l0 = self.length_origin
        shear_location = self.shear_location_ratio * l0
        dofs = [getattr(dof, 'd_try') for dof in self.dofs]
        self.orient_to_local(dofs, 'pos_try')
        shear_disp = dofs[7] - dofs[1] - shear_location*dofs[11] - (l0 - shear_location)*dofs[5]

        stage_index = self.stage_index
        self.stage[stage_index](shear_disp)
    
    def get_internal_force(self, dof_type, pos_type):
        l0 = self.length_origin
        shear_location = self.shear_location_ratio * l0

        force = self.dict_force[dof_type]
        f_2_a = -force
        f_2_b = force
        ms_b = -shear_location * f_2_b
        ms_a = (l0 - shear_location) * f_2_a
        force = [0.0, f_2_a, 0.0, 0.0, 0.0, ms_a, 0.0, f_2_b, 0.0, 0.0, 0.0, ms_b]
        self.orient_to_global(force, pos_type)
        return force
    
    def get_global_stiffness(self):
        index = self.stage_index
        l0 = self.length_origin
        ls = self.shear_location_ratio * l0
        l0s = l0 - ls
        if index == 1 or index == 3 or index == 5:
            k = self.elastic_stiffness
        if self.stage_index == 2:
            k = self.post_yield_stiffness
        if self.stage_index == 4:
            k = self.get_reloading_stiffness(self.phase)
        
        return [
            [0.0, 0.0,      0.0,        0.0, 0.0,       0.0],
            [0.0, k  ,      k*l0s,      0.0, -k,        k*ls],
            [0.0, k*l0s,    k*l0s**2,   0.0, -k*l0s,    k*ls*l0s],
            [0.0, 0.0,      0.0,        0.0, 0.0,       0.0],
            [0.0, -k ,      -k*l0s,     0.0, k  ,       -k*ls],
            [0.0, k*ls,     k*ls*l0s,   0.0, -k*ls,     k*ls**2]
        ]

class TwoNodeModifiedCloughRotationSpring2D(TwoNodeModifiedCloughSpring2D):
    """
    Two node rotation spring element which follows 
    the rule of Modified-Clough behavior in inelastic stage 
    in X-Y plane.
    """
    
    def set_try_disp(self):
        dofs = [getattr(dof, 'd_try') for dof in self.dofs]
        self.orient_to_local(dofs, 'pos_try')
        disp = dofs[5] - dofs[0]

        stage_index = self.try_stage_index
        self.stage[stage_index](disp)
    
    def get_internal_force(self, dof_type, pos_type):
        force = dok_matrix((6, 1))
        m = self.dict_force[dof_type]
        inf = [0.0, 0.0, -m, 0.0, 0.0, m]
        self.orient_to_global(inf, pos_type)
        for i, f in enumerate(inf):
            force[i, 0] = f
        return force
    
    def get_local_stiffness(self):
        stiffness = dok_matrix((6, 6))
        index = self.stage_index
        if index == 1 or index == 3 or index == 5:
            k = self.elastic_stiffness
        if self.stage_index == 2:
            k = self.post_yield_stiffness
        if self.stage_index == 4:
            k = self.get_reloading_stiffness(self.phase)
        stiffness[2, 2], stiffness[5, 5] = k, k
        stiffness[2, 5], stiffness[5, 2] = -k, -k
        return stiffness