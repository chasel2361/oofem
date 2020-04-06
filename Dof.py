# -*- coding: utf-8 -*-
"""author: 周光武、簡子琦"""
import warnings

class ActiveDof:    
    def __init__(self):
        self._d = 0.0                      #當前時間步幅相對於未變形位置的絕對變位
        self._d_last = 0.0                 #前一時間步幅相對於未變形位置的絕對位移
        self._d_try = 0.0                #當前迭代步幅相對於未變形位置的絕對位移
        self._d_try_last = 0.0           #前一迭代步幅相對於未變形位置的絕對位移
        self._v = 0.0
        self._v_last = 0.0
        self._v_try = 0.0
        self._v_try_last = 0.0
        self._a = 0.0
        self._a_try = 0.0
        self._eq_number = None       

    @property
    def is_restrained(self):
        return False
    
    @property
    def eq_number(self):
        return self._eq_number

    @property
    def d(self):
        return self._d    
    
    @property
    def d_last(self):
        return self._d_last
    
    @property
    def d_try(self):
        return self._d_try

    @property
    def d_try_last(self):
        return self._d_try_last
        
    @property
    def v(self):
        return self._v
    
    @property
    def v_last(self):
        return self._v_last
    
    @property
    def v_try(self):
        return self._v_try
    
    @property
    def v_try_last(self):
        return self._v_try_last
        
    @property
    def a(self):
        return self._a
    
    @property
    def a_try(self):
        return self._a_try
    
    
    @eq_number.setter
    def eq_number(self, eq):
        if eq < 0:
            return warnings.warn('Can\'t set eq_number as an negative number!', UserWarning)
        else:
            self._eq_number = eq
    
    @d.setter
    def d(self, dis):
        self._d = dis
    
    @d_last.setter
    def d_last(self, dis):
        self._d_last = dis
    
    @d_try.setter
    def d_try(self, dis):
        self._d_try = dis
    
    @d_try_last.setter
    def d_try_last(self, dis):
        self._d_try_last = dis
    
    @v.setter
    def v(self, vel):
        self._v = vel
    
    @v_last.setter
    def v_last(self, vel):
        self._v_last = vel
    
    @v_try.setter
    def v_try(self, vel):
        self._v_try = vel
    
    @v_try_last.setter
    def v_try_last(self, vel):
        self._v_try_last = vel
    
    @a.setter
    def a(self, acc):
        self._a = acc
    
    @a_try.setter
    def a_try(self, acc):
        self._a_try = acc
        
    def inc_d_try(self, delta_d):
        self.d_try_last = self.d_try
        self.d_try += delta_d[self.eq_number]
    
    def commit(self):
        self.d_last = self.d
        self.d = self.d_try
        self.v = self.v_try
        self.a = self.a_try

    def integrate(self, integrator):
        integrator.integrate(self)
        
    def assemble_force(self, force, value):
        if self.eq_number != None:
            force[self.eq_number] += value
    
    def _get_dof(self, dof, d_type):
        dof[self.eq_number] = getattr(self, d_type)

        
    def __repr__(self):
        return (f'{self.__class__.__name__} '
                f'restrain: {self.is_restrained}; '
                f'eq = {self.eq_number}')

"""
先寫一個簡單的、跟時間不相關的來做靜力位移控制
"""
class PrescribedDof:
    def __init__(self, a, v, d):
        self._d = d                      #當前時間步幅相對於未變形位置的絕對變位
        self._v = v
        self._a = a
        self._eq_number = None

    def eq_number(self):
        return self._eq_number
    
    def is_restrained(self):
        return False
    
    @property
    def d(self):
        return self._d
    
    @property
    def d_last(self):
        return self._d
    
    @property
    def d_try(self):
        return self._d
    
    @property
    def d_try_last(self):
        return self._d
    
    @property
    def v(self):
        return self._v
    
    @property
    def v_last(self):
        return self._v
    
    @property
    def v_try(self):
        return self._v
    
    @property
    def v_try_last(self):
        return self._v
    
    @property
    def a(self):
        return self._a
    
    @property
    def a_try(self):
        return self._a

    @d.setter
    def d(self, dis):
        return
    
    @d_last.setter
    def d_last(self, dis):
        return 
    
    @d_try.setter
    def d_try(self, dis):
        return 
    
    @d_try_last.setter
    def d_try_last(self, dis):
        return
    
    @v.setter
    def v(self, vel):
        return 
    
    @v_last.setter
    def v_last(self, vel):
        return
    
    @v_try.setter
    def v_try(self, vel):
        return 
    
    @v_try_last.setter
    def v_try_last(self, vel):
        return 

    @a.setter
    def a(self, acc):
        return 
    
    @a_try.setter
    def a_try(self, acc):
        return 
    
    def assemble_force(self, force, value):
        if self.eq_number != None:
            force[self.eq_number] += value
            
    def inc_d_try(self, delta_d):
        return
    
    def _get_dof(self, dof, d_type):
        dof[self.eq_number] = getattr(self, d_type)
    
    
    # def d(self, time):
    #     # call d at t
    #     return self._d.at(time)
    
    # def v(self, time):
    #     # call v at timestep
    #     return self._v.at(time)
    
    # def a(self, time):
    #     # call a at timestep
    #     return self._a.at(time)

class BoundaryDof:    
    @property
    def is_restrained(self):
        return True
    
    @property
    def eq_number(self):
        return None
    
    @property
    def d(self):
        return 0.0
    
    @property
    def d_last(self):
        return 0.0
    
    @property
    def d_try(self):
        return 0.0
    
    @property
    def d_try_last(self):
        return 0.0
    
    @property
    def v(self):
        return 0.0
    
    @property
    def v_last(self):
        return 0.0
    
    @property
    def v_try(self):
        return 0.0
    
    @property
    def v_try_last(self):
        return 0.0
    
    @property
    def a(self):
        return 0.0
    
    @property
    def a_try(self):
        return 0.0

    @d.setter
    def d(self, dis):
        return
    
    @d_last.setter
    def d_last(self, dis):
        return 
    
    @d_try.setter
    def d_try(self, dis):
        return 
    
    @d_try_last.setter
    def d_try_last(self, dis):
        return
    
    @v.setter
    def v(self, vel):
        return 
    
    @v_last.setter
    def v_last(self, vel):
        return
    
    @v_try.setter
    def v_try(self, vel):
        return 
    
    @v_try_last.setter
    def v_try_last(self, vel):
        return 

    @a.setter
    def a(self, acc):
        return 
    
    @a_try.setter
    def a_try(self, acc):
        return 
        
    def inc_d_try(self, delta_d):
        return
    
    def commit(self):
        return
        
    def integrate(self, integrator):
        return
        
    def assemble_force(self, force, value):
        return
    
    def _get_dof(self, dof, dtype):
        return 
   

    def __repr__(self):
        return (f'{self.__class__.__name__} '
                f'is_restrained: {self.is_restrained}')