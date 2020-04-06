# -*- coding: utf-8 -*-
"""author: 周光武、簡子琦"""

class Newmark:
    """
    Newmark beta method integrator.

    Parameters
    ----------
    delta_t : {time imcrement, float}
    beta : {beta value, float}
    gamma : {gamma value, float}

    Returns
    -------
    out : Newmark integrator obj

    """
    def __init__(self, delta_t = 0.01, beta = 0.25, gamma = 0.5):
        self._beta = beta
        self._gamma = gamma
        self._delta_t = delta_t  #加上@property        
        self._b1 = 1 / (beta * delta_t**2)
        self._b2 = -1 / (beta * delta_t)
        self._b3 = -(1 / (2 * beta) - 1)
        self._b4 = gamma / (beta * delta_t)
        self._b5 = 1 - gamma / beta
        self._b6 = delta_t * (1 - gamma / (2 * beta))
        
        self._time_step_count = 0
        self._iteration = 0
        
    def integrate(self, dof):
        """
        Integrate the input dof.

        Parameters
        ----------
        dof : {dof to be integrated, dof obj}

        """
        delu = dof.d_try - dof.d
        v = dof.v
        a = dof.a
        dof.a_try = self.b1 * delu + self.b2 * v + self.b3 * a
        dof.v_try = self.b4 * delu + self.b5 * v + self.b6 * a
 
    @property
    def b1(self):
        return self._b1
    
    @property
    def b2(self):
        return self._b2

    @property
    def b3(self):
        return self._b3

    @property
    def b4(self):
        return self._b4

    @property
    def b5(self):
        return self._b5

    @property
    def b6(self):
        return self._b6
    
    @property
    def parameters(self):
        print('b1 = %.2f\nb2 = %.2f\nb3 = %.2f\nb4 = %.2f\nb5 = %.2f\nb6 = %.5f'
              % (self._b1, self._b2, self._b3, self._b4, self._b5, self._b6))
    
    @property
    def time_step_count(self):
        return self._time_step_count
    
    @property
    def iteration(self):
        return self._iteration
    
    @iteration.setter
    def iteration(self, i):
        self._iteration = i
    
    @time_step_count.setter
    def time_step_count(self, i):
        self._time_step_count = i
    
        
    def update_beta(self, b):
        delta_t = self._delta_t
        gamma = self._gamma
        self._update_b1(delta_t, b, gamma)
        self._update_b2(delta_t, b, gamma)
        self._update_b3(delta_t, b, gamma)
    
    def update_gamma(self, g):
        delta_t = self._delta_t
        beta = self._beta
        self._update_b4(delta_t, beta, g)
        self._update_b5(delta_t, beta, g)
        self._update_b6(delta_t, beta, g)
    
    def update_delta_t(self, t):
        beta = self._beta
        gamma = self._gamma
        self._update_b1(t, beta, gamma)
        self._update_b2(t, beta, gamma)
        self._update_b4(t, beta, gamma)
        self._update_b6(t, beta, gamma)


    def _update_b1(self, delta_t, beta, gamma):
        self._b1 = 1 / (beta * delta_t**2)
    
    def _update_b2(self, delta_t, beta, gamma):
        self._b2 = -1 / (beta * delta_t)
        
    def _update_b3(self, delta_t, beta, gamma):
        self._b3 = -(1 / (2 * beta) - 1)
        
    def _update_b4(self, delta_t, beta, gamma):
        self._b4 = gamma / (beta * delta_t)
    
    def _update_b5(self, delta_t, beta, gamma):
        self._b5 = 1 - gamma / beta
        
    def _update_b6(self, delta_t, beta, gamma):
        self._b6 = delta_t * (1 - gamma / (2 * beta))

# if __name__ == "__main__":
#     print(Newmark(0.01).parameters)