import unittest
from TwoNodeModifiedCloughSpring2D import TwoNodeModifiedCloughSpring2D, TwoNodeModifiedCloughAxialSpring2D, TwoNodeModifiedCloughShearSpring2D, TwoNodeModifiedCloughRotationSpring2D
from Material import BilinearMaterial
from Node import Node, Point
from math import isclose
from numpy import array


class TwoNodeModifiedCloughSpring2DTest(unittest.TestCase):
    def setUp(self):
        n1 = Node(1, Point(1, 0, 0))
        n2 = Node(2, Point())
        material = BilinearMaterial(1, 2000, 100, 2)
        self.spring = TwoNodeModifiedCloughSpring2D(1, n1, n2, material, 0, 0)
    
    def tearDown(self):
        self.spring = None
    
    def test_extreme_disp_io(self):
        true = self.assertTrue
        sp = self.spring
        true(isclose(sp.get_extreme_disp(1), -2))
        true(isclose(sp.get_extreme_disp(2), 2))

        sp.update_extreme_disp(1, -3)
        sp.update_extreme_disp(2, 5)

        true(isclose(sp.get_extreme_disp(1), -3))
        true(isclose(sp.get_extreme_disp(2), 5))
    
    def test_nonforce_disp_io(self):
        true = self.assertTrue
        sp = self.spring
        true(isclose(sp.get_nonforce_disp(1), 0))
        true(isclose(sp.get_nonforce_disp(2), 0))

        sp.update_nonforce_disp(1, -3)
        sp.update_nonforce_disp(2, 5)

        true(isclose(sp.get_nonforce_disp(1), -3))
        true(isclose(sp.get_nonforce_disp(2), 5))
    
    def test_extreme_force_io(self):
        true = self.assertTrue
        sp = self.spring
        true(isclose(sp.get_extreme_force(1), -4000))
        true(isclose(sp.get_extreme_force(2), 4000))

        sp.update_extreme_force(1, -5000)
        sp.update_extreme_force(2, 6000)

        true(isclose(sp.get_extreme_force(1), -5000))
        true(isclose(sp.get_extreme_force(2), 6000))
    
    def test_reloading_stiffness(self):
        true = self.assertTrue
        sp = self.spring
        true(isclose(sp.get_reloading_stiffness(1), 2000))
        true(isclose(sp.get_reloading_stiffness(2), 2000))

        sp.update_extreme_disp(1, -4)
        sp.update_extreme_force(1, -5000)
        sp.update_nonforce_disp(1, -2)

        sp.update_extreme_disp(2, 3)
        sp.update_extreme_force(2, 4500)
        sp.update_nonforce_disp(2, 1)

        true(isclose(sp.get_reloading_stiffness(1), 1000))
        true(isclose(sp.get_reloading_stiffness(2), 900))
    
    def test_change_phase(self):
        true = self.assertTrue
        sp = self.spring

        true(isclose(sp.phase, 2))
        sp.change_phase()
        true(isclose(sp.phase, 1))
        sp.change_phase()
        true(isclose(sp.phase, 2))

    def test_stage_elastic(self):
        true = self.assertTrue
        sp = self.spring

        sp.stage_elastic(1)
        true(isclose(sp.dict_force['d_try'], 2000))
        sp.stage_elastic(-1)
        true(isclose(sp.dict_force['d_try'], -2000))

        sp.stage_elastic(3)
        true(isclose(sp.try_stage_index, 2))
    
    def test_stage_beyond_yield(self):
        true = self.assertTrue
        sp = self.spring
        get_try_extreme_disp = sp.get_try_extreme_disp
        get_try_extreme_force = sp.get_try_extreme_force
        get_extreme_disp = sp.get_extreme_disp
        get_extreme_force = sp.get_extreme_force

        sp.stage_beyond_yield(3)
        true(isclose(sp.dict_force['d_try'], 4100))
        sp.commit()

        sp.stage_beyond_yield(2)
        phase = sp.phase
        true(isclose(sp.try_stage_index, 3))
        true(isclose(sp.stage_index, 1))
        true(isclose(get_try_extreme_force(phase), 4100))
        true(isclose(get_extreme_force(phase), 4000))
        true(isclose(get_try_extreme_disp(phase), 3))
        true(isclose(get_extreme_disp(phase), 2))
        sp.commit()
        true(isclose(get_extreme_disp(phase), 3))
        true(isclose(get_extreme_force(phase), 4100))
        
        # sp.reset()
        sp.stage_beyond_yield(3)
        sp.commit()
        sp.stage_beyond_yield(-1)
        true(isclose(sp.try_stage_index, 4))
        sp.commit()

        # sp.reset()
        sp.stage_beyond_yield(4)
        true(isclose(sp.try_stage_index, 2))

        # 驗證另一phase
        # sp.reset()
        sp.change_phase()
        phase = sp.phase

        sp.stage_beyond_yield(-3)
        sp.commit()
        true(isclose(sp.dict_force['d_try'], -4100))

        sp.stage_beyond_yield(-2)
        true(isclose(sp.try_stage_index, 3))
        true(isclose(sp.get_try_extreme_disp(phase), -3))
        true(isclose(sp.get_try_extreme_force(phase), -4100))
        sp.commit()
        true(isclose(get_extreme_disp(phase), -3))
        true(isclose(get_extreme_force(phase), -4100))

    def test_stage_unloading_from_yield(self):
        true = self.assertTrue
        sp = self.spring

        sp.stage_elastic(4)
        sp.commit()
        sp.stage_beyond_yield(3)
        true(isclose(sp.dict_force['d_try'], 2200))

        sp.stage_unloading_from_yield(4)
        true(isclose(sp.try_stage_index, 2))

        sp.stage_unloading_from_yield(-1)
        true(isclose(sp.try_stage_index, 4))

class TwoNodeModifiedCloughRotationSpring2DTest(unittest.TestCase):
    def setUp(self):
        n1 = Node(1, Point())
        n2 = Node(2, Point(0, 1, 0))
        n1.restrain()
        material = BilinearMaterial(1, 2000, 100, 2)
        self.spring = TwoNodeModifiedCloughRotationSpring2D(1, n1, n2, material, 1, 1)
    
    def tearDown(self):
        self.spring = None
    
    def check_stiffness(self, spring, value):
        true = self.assertTrue
        q = spring.get_local_stiffness()
        a = array([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, value, 0, 0, -value],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, -value, 0, 0, value]])
        for i in range(6):
            for j in range(6):
                true(isclose(q[i, j], a[i, j]))
    
    def check_force(self, spring, value):
        true = self.assertTrue
        q = spring.get_internal_force('d_try', 'pos_try')
        a = array([0, 0, -value, 0, 0, value])
        for i in range(6):
            true(isclose(q[i, 0], a[i]))
    
    def test_get_local_stiffness(self):
        check = self.check_stiffness
        sp = self.spring
        dofs = sp.node2.dofs

        """stage initial"""
        check(sp, 2000)

        """stage elastic"""
        disp = [1, 0.5, 1.9]
        stiffness = [2000, 2000, 2000]

        """stage beyond yield"""
        disp += [4]
        stiffness += [100]

        """stage unload from yield"""
        disp += [2]
        stiffness += [2000]

        """stage reloading"""
        disp += [0, -1.9]
        stiffness += [1025.6410256410256, 1025.6410256410256]
        
        """stage beyond yield"""
        disp += [-4]
        stiffness += [100]

        """stage unload from yield"""
        disp += [-2]
        stiffness += [2000]
        
        """stage reloading"""
        disp += [0, 4]
        stiffness += [711.864406779661, 711.864406779661]
        
        """stage inner_peak"""
        disp += [2, 3.9]
        stiffness += [2000, 2000]

        """beyond yield stage"""
        disp += [5]
        stiffness += [100]

        for d, k in zip(disp, stiffness):
            dofs[5].d_try = d
            sp.set_try_disp()
            sp.commit()
            check(sp, k)

    def test_get_internal_force(self):
        sp = self.spring
        # true = self.assertTrue
        dofs = sp.node2.dofs
        check = self.check_force

        """stage elastic"""
        disp = [1, 0.5, 1.9]
        force = [2000, 1000, 3800]

        """stage beyond yield"""
        disp += [4]
        force += [4200]

        """stage unload from yield"""
        disp += [2]
        force += [200]

        """stage reloading"""
        disp += [0, -1.9]
        force += [-1948.7179487179485, -3897.435897435897]
        
        """stage beyond yield"""
        disp += [-4]
        force += [-4200]

        """stage unload from yield"""
        disp += [-2]
        force += [-200]
        
        """stage reloading"""
        disp += [0, 4]
        force += [1352.5423728813557, 4200]
        
        """stage inner_peak"""
        disp += [2, 3.9]
        force += [200, 4000]

        """beyond yield stage"""
        disp += [5]
        force += [4300]
        
        for d, f in zip(disp, force):
            dofs[5].d_try = d
            sp.set_try_disp()
            sp.commit()
            check(sp, f)

if __name__ == '__main__':
    unittest.main()