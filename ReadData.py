from Assembly import *
from Node import *
from Section import Section
from Material import *
from Beam2D import *
from TwoNodeSpring2D import *
from TwoNodeModifiedCloughSpring2D import *
from TimeSeries import *
import pandas as pd

def ReadData(assembly, filename):
    metadata = pd.read_excel(filename, sheet_name = None)
    node_data = metadata.get('Node')
    section_data = metadata.get('Section')
    material_data = metadata.get('Material')
    degrade_force_material_data = metadata.get('DegradeForceMaterial')
    beam_data = metadata.get('Beam')
    axial_sp_data = metadata.get('AxialSpring')
    shear_sp_data = metadata.get('ShearSpring')
    rot_sp_data = metadata.get('RotSpring')
    seismic_data = metadata.get('Seismic')

    # write node data
    node_id = list(node_data['id'])
    node_x = list(node_data['x'])
    node_y = list(node_data['y'])
    node_z = list(node_data['z'])
    restrain_x = list(node_data['restrain_x'])
    restrain_y = list(node_data['restrain_y'])
    restrain_z = list(node_data['restrain_z'])
    restrain_rx = list(node_data['restrain_rx'])
    restrain_ry = list(node_data['restrain_ry'])
    restrain_rz = list(node_data['restrain_rz'])

    for (i, x, y, z) in zip(node_id, node_x, node_y, node_z):
        n = Node(i, Point(x, y, z))
        assembly.add_node(n)
    
    nodes = assembly.nodes
    for j, (n, x, y, z, rx, ry, rz) in enumerate(zip(nodes, restrain_x, restrain_y, restrain_z, restrain_rx, restrain_ry, restrain_rz)):
        for i ,dof in enumerate([x, y, z, rx, ry, rz]):
            if dof == 1:
                n.restrain_dof(i)
    
    
    assembly.assign_eq_number()


    # write section data
    sect_id = list(section_data['id'])
    density = list(section_data['density'])
    E = list(section_data['E'])
    G = list(section_data['G'])
    Area = list(section_data['Area'])
    Iy = list(section_data['Iy'])
    Iz = list(section_data['Iz'])
    J = list(section_data['J'])

    for (i, d, e, g, a, iy, iz, j) in zip(sect_id, density, E, G, Area, Iy, Iz, J):
        sect = Section(i, d, e, g, a, iy, iz, j)
        assembly.add_section(sect)
    
    # write material data
    mat_id = list(material_data['id'])
    mat_k1 = list(material_data['k1'])
    mat_k2 = list(material_data['k2'])
    mat_uy = list(material_data['uy'])

    for (i, k1, k2, uy) in zip(mat_id, mat_k1, mat_k2, mat_uy):
        mat = BilinearMaterial(i, k1, k2, uy)
        assembly.add_material(mat)
    
    # write degrading force material data
    defmat_id = list(degrade_force_material_data['id'])
    defmat_k1 = list(degrade_force_material_data['k1'])
    defmat_uy = list(degrade_force_material_data['uy'])
    defmat_ud = list(degrade_force_material_data['ud'])
    defmat_fd = list(degrade_force_material_data['fd'])

    for (i, k1, uy, ud, f) in zip(defmat_id, defmat_k1, defmat_uy, defmat_ud, defmat_fd):
        mat = DegradingStrengthMaterial(i, k1, uy, ud, f)
        assembly.add_material(mat)


    # write beam data
    beam_id = list(beam_data['id'])
    node1 = list(beam_data['node1'])
    node2 = list(beam_data['node2'])
    section = list(beam_data['section'])
    rayleigh = list(beam_data['rayleigh'])
    # ref_x = list(beam_data['ref_x'])
    # ref_y = list(beam_data['ref_y'])
    # ref_z = list(beam_data['ref_z'])

    node = assembly.node
    sect = assembly.section
    for (i, n1, n2, s, r) in zip(beam_id, node1, node2, section, rayleigh):
        e = Beam2D(i, node(n1), node(n2), sect(s), r)
        assembly.add_element(e)
    
    # write axial spring data
    asp_id = list(axial_sp_data['id'])
    asp_n1 = list(axial_sp_data['node1'])
    asp_n2 = list(axial_sp_data['node2'])
    asp_mat = list(axial_sp_data['material'])
    asp_mass = list(axial_sp_data['mass'])
    asp_inertia = list(axial_sp_data['inertia'])
    # ref_x = list(axial_sp_data['ref_x'])
    # ref_y = list(axial_sp_data['ref_y'])
    # ref_z = list(axial_sp_data['ref_z'])

    material = assembly.material
    for (i, n1, n2, mat, mass, inertia) in zip(asp_id, asp_n1, asp_n2, asp_mat, asp_mass, asp_inertia):
        asp = TwoNodeAxialSpring2D(i, node(n1), node(n2), material(mat), mass, inertia)
        assembly.add_element(asp)
    
    # write shear spring data
    ssp_id = list(shear_sp_data['id'])
    ssp_n1 = list(shear_sp_data['node1'])
    ssp_n2 = list(shear_sp_data['node2'])
    ssp_mat = list(shear_sp_data['material'])
    ssp_mass = list(shear_sp_data['mass'])
    ssp_inertia = list(shear_sp_data['inertia'])
    # ref_x = list(shear_sp_data['ref_x'])
    # ref_y = list(shear_sp_data['ref_y'])
    # ref_z = list(shear_sp_data['ref_z'])
    shear_loc_ration = list(shear_sp_data['shear_loc_ratio'])

    for (i, n1, n2, mat, mass, inertia, loc) in zip(ssp_id, ssp_n1, ssp_n2, ssp_mat, ssp_mass, ssp_inertia, shear_loc_ration):
        ssp = TwoNodeShearSpring2D(i, node(n1), node(n2), material(mat), mass, inertia, loc)
        assembly.add_element(ssp)
    
    # write rotation spring data
    rsp_id = list(rot_sp_data['id'])
    rsp_n1 = list(rot_sp_data['node1'])
    rsp_n2 = list(rot_sp_data['node2'])
    rsp_mat = list(rot_sp_data['material'])
    rsp_mass = list(rot_sp_data['mass'])
    rsp_inertia = list(rot_sp_data['inertia'])
    # ref_x = list(rot_sp_data['ref_x'])
    # ref_y = list(rot_sp_data['ref_y'])
    # ref_z = list(rot_sp_data['ref_z'])

    for (i, n1, n2, mat, mass, inertia) in zip(rsp_id, rsp_n1, rsp_n2, rsp_mat, rsp_mass, rsp_inertia):
        rsp = TwoNodeModifiedCloughRotationSpring2D(i, node(n1), node(n2), material(mat), mass, inertia)
        assembly.add_element(rsp)
    
    # declare seismic time series
    time = list(seismic_data['time'])
    acceleration = list(seismic_data['acceleration'])
    t0 = time[0]
    dt = time[1] - t0
    seismic = TimeSeries(t0, dt, acceleration)
    assembly.seismics.append(seismic)

    


# assembly = Assembly(None)

# ReadData(assembly, 'FEMA_3FL.xlsx')
# for n in assembly.nodes:
#     pos = n.pos
#     print('%6d %10.4f %10.4f %10.4f' %(n.id, pos.x, pos.y, pos.z))

# for sect in assembly.sections:
#     print('%3d %6.3f %10.2e %12.5e %12.5e %12.5e %12.5e %12.5e' % (sect.id, sect.linear_density, sect.E, sect.G, sect.Area, sect.I_y, sect.I_z, sect.J))

# for e in assembly.elements:
#     print(e)
