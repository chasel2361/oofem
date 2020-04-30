from ReadData import *
from Assembly import *
from Integrator import Newmark
from Secant import multiply
from Clock import *
from scipy.sparse import linalg
import LeeMethod as LM
from OutputCheck import *

# def K_sec(assembly):
#     force = assembly.assemble_internal_force('d')
#     last_force = assembly.assemble_internal_force('d_last')
#     u = assembly.get_dof('d')
#     last_u = assembly.get_dof('d_last')
#     disp = [[0.0]]*neq
#     last_disp = [[0.0]]*neq
#     for i, (d, dl) in enumerate(zip(u, last_u)):
#         disp[i][0] = d
#         last_disp[i][0] = dl
#     disp = dok_matrix(disp)
#     last_disp = dok_matrix(last_disp)

#     A = force - last_force
#     B = disp - last_disp

#     ans = dok_matrix((len(u), 1))
#     for i in range(len(u)):
#         if isclose(B[i, 0], 0):
#             ans[i, 0] = 0.0
#         else:
#             ans[i, 0] = A[i, 0] / B[i, 0]
#     return ans

def div(A, B):
    assert isclose(A.shape[0], B.shape[0])
        # raise "Can't calculate for shape!"
    ans = dok_matrix((A.shape[0], 1))
    for i in range(A.shape[0]):
        if isclose(B[i, i], 0):
            ans[i, 0] = 0.0
        else:
            ans[i, 0] = A[i, 0] / B[i, i]
    return ans

def K_effective(newmark, mass, stiffness):
    b1 = newmark.b1
    K = b1 * mass + stiffness
    return K

dt = 0.01
clock = Clock(dt, [0, 2])
newmark = Newmark(dt)
assembly = Assembly(newmark)

ReadData(assembly, '1FL.xlsx')
neq = assembly.eq_number
output_check(assembly, 'formal_1FL_check.txt')

with open('formal_1FL.txt', 'w') as p:
    p.write('%8s %7s %12s' % ('time', 'iter', 'ux_top'))

tol = 1e-4
# f = TimeSeries(0, 1, [0, 100, 100])
seismic = assembly.seismics[0]
# ef = dok_matrix([[f.at(clock.current_time)/2], [0], [0], [0], [0], [0]])

while not clock.is_end:
    ef = LM.force_ex(assembly, seismic.at(clock.current_time))
    P = assembly.get_internal_force('d', 'pos_origin')
    a = assembly.get_dof('a')
    m = assembly.lumped_mass[0]
    inerf = m * a
    R = ef - inerf - P
    stiffness = assembly.assemble_K('pos_origin')
    K_eff = K_effective(newmark, m, stiffness)
    conv = linalg.norm(R)

    while True:
        
        delu = linalg.spsolve(K_eff, R)
        delu = delu.reshape((neq, 1))
        # delu = delu.tolist()

        if conv < tol:
            assembly.commit()
            u = assembly.get_dof('d')
            # k_sec = K_sec(assembly)
            with open('formal_1FL.txt', 'a') as p:
                p.write('\n%8.5f %7d %12.4e' % (clock.current_time, newmark.iteration, u[6]))
            print('time = %5.3f, u_top =  %12.4e' % (clock.current_time, u[6]))
            # print('K_sec\n', k_sec)
            clock.forward()
            newmark.iteration = 0
            break
        
        else:
            assembly.inc_d_try(delu)
            assembly.set_try_disp()
            assembly.integrate(newmark)

            P = assembly.get_internal_force('d_try', 'pos_origin')
            a = assembly.get_dof('a_try')
            m = assembly.lumped_mass[0]
            inerf = m * a
            R = ef - inerf - P

            stiffness = assembly.assemble_K('pos_origin')
            K_eff = K_effective(newmark, m, stiffness)

            conv = linalg.norm(R)
            newmark.iteration += 1

    
# print('\nProcessing time %6.2f' % (time.clock() - t0))
print('Done!!        ｡:.ﾟヽ(*´∀`)ﾉﾟ.:｡')