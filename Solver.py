
# class NewtonRaphson():

def IncrementalSection(Assembly, ex_force):
    """
    Solver of system of equation by incremental section method

    Parameter
    ---------
    Assembly : {Assembled component, Assembly obj}
    ex_force : {External force, dok_matrix}

    """

    
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