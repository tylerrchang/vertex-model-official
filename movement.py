import vertex
import copy
import numpy as np
import geometry

def move_vertices(vert_list, data):
    # vert_list_old = copy.deepcopy(vert_list)
    forces = calc_forces(vert_list, data) # returns a list
    for vert, force in zip(vert_list, forces):
        # add force and check for out of bounds
        vert.x = (vert.x - force[0] * data.dt) % data.lx
        vert.y = (vert.y - force[1] * data.dt) % data.ly
    # check for T1 transitions
        # lots of checks 
    # set new parameters
    # 1. polygons need to get updated
    for cell_ in data.cell_list:
        cell_.create_cell_polygon()


def calc_forces(vert_list, data):
    forces = []
    # loop over all vertices and compute force for each
    for v in vert_list:
        force = np.zeros(2)
        # use list of cells that corresponds to each vertex
        comp_cells = data.vert_adjcent_cells[v]

        # loop over each cell in list of cells corresponding to vertex
        # and calc force from each
        for i in range(len(comp_cells)):
            # find shared edges between current cell and two cells that share
            # the center vertex with it
            # ASSUMPTION: each cell only borders 2 other cells that shared the
            #    main vertex
            s1 = geometry.find_shared_edge(comp_cells[i], comp_cells[(i + 1) % len(comp_cells)], v)
            s2 = geometry.find_shared_edge(comp_cells[i], comp_cells[(i + 2) % len(comp_cells)], v)
            # calculate da/dhijk
            # calculate length of shared edge between 2 other cells
            l1 = geometry.distance_formula_boundary_check(s1[0], s1[1], data)
            l2 = geometry.distance_formula_boundary_check(s2[0], s2[1], data)

            # calculate midpoint between two vertices of the shared edge of each
            # of the 2 other cells
            # this is used to help calculate unit vector
            # mp1 = geometry.midpoint_formula_boundary_check(s1[0], s1[1])
            # mp2 = geometry.midpoint_formula_boundary_check(s2[0], s2[1])
            # calculate unit vector pointing away from the center of the cell
            # that is perpendicular with the shared edge
            # the line connecting the center of cells is always perp to edge

            # calculate dp/dhijk
            # calculate the unit vector pointing from the center vertex to the 
            # other vertices making up the shared edges between current cell
            t1 = geometry.unit_vector_boundary_check(v, s1[1], data)
            t2 = geometry.unit_vector_boundary_check(v, s2[1], data)

            # equation from paper
            dp = -1 * (t1 + t2)

            center_vertex_unit_vector = geometry.unit_vector_boundary_check(v, comp_cells[i].center, data)
            n1 = geometry.unit_vector_perp_to_edge(t1, center_vertex_unit_vector, data)
            n2 = geometry.unit_vector_perp_to_edge(t2, center_vertex_unit_vector, data)

            # equation from paper
            da = 1 / 2 * (l1 * n1 + l2 * n2)

            # calculate force from specific cell
            # equation from paper
            de = (
                2 * data.KA * (comp_cells[i].area - data.A0) * da + 
                2 * data.KP * (comp_cells[i].perimeter - data.P0) * dp
                )
            force += de
        forces.append(force)
    return forces

def calc_energy(data):
    """
    Computes the overall energy of the system using defined equation
    """
    total_energy = 0
    for cell in data.cell_list:
        total_energy += data.KA * (cell.area - data.A0) ** 2 + data.KP * \
            (cell.perimeter - data.P0) ** 2
        
    return total_energy


# def move_test(vert_list, data):
#     # vert_list_old = copy.deepcopy(vert_list)
#     forces = np.zeros([len(vert_list), 2])
#     forces[forces == 0] = -2.6 / data.dt  
#     for vert, force in zip(vert_list, forces):
#         # add force and check for out of bounds
#         vert.x = (vert.x - force[0] * data.dt) % data.lx
#         vert.y = (vert.y - force[1] * 0) % data.ly
#     # check for T1 transitions
#         # lots of checks 
#     # set new parameters
#     # 1. polygons need to get updated
#     for cell_ in data.cell_list:
#         cell_.create_cell_polygon()

# def calc_forces_b4(vert_list, data):
#     forces = []
#     # loop over all vertices and compute force for each
#     for v in vert_list:
#         force = np.zeros(2)
#         # use list of cells that corresponds to each vertex
#         comp_cells = data.vert_adjcent_cells[v]
#         # loop over each cell in list of cells corresponding to vertex
#         # and calc force from each
#         for i in range(len(comp_cells)):
#             # find shared edges between current cell and two cells that share
#             # the center vertex with it
#             # ASSUMPTION: each cell only borders 2 other cells that shared the
#             #    main vertex
#             s1 = geometry.find_shared_edge(comp_cells[i], comp_cells[(i + 1) % len(comp_cells)], v)
#             s2 = geometry.find_shared_edge(comp_cells[i], comp_cells[(i + 2) % len(comp_cells)], v)
#             # calculate da/dhijk
#             # calculate length of shared edge between 2 other cells
#             l1 = geometry.distance_formula_boundary_check(s1[0], s1[1], data)
#             l2 = geometry.distance_formula_boundary_check(s2[0], s2[1], data)
#             # calculate midpoint between two vertices of the shared edge of each
#             # of the 2 other cells
#             # this is used to help calculate unit vector
#             # mp1 = geometry.midpoint_formula_boundary_check(s1[0], s1[1])
#             # mp2 = geometry.midpoint_formula_boundary_check(s2[0], s2[1])
#             # calculate unit vector pointing away from the center of the cell
#             # that is perpendicular with the shared edge
#             # the line connecting the center of cells is always perp to edge
#             center_vertex1 = comp_cells[i].center
#             center_vertex1[0] %= data.lx
#             center_vertex1[1] %= data.ly
#             center_vertex2 = comp_cells[(i + 1) % len(comp_cells)].center
#             center_vertex2[0] %= data.lx
#             center_vertex2[1] %= data.ly
#             center_vertex3 = comp_cells[(i + 2) % len(comp_cells)].center
#             center_vertex3[0] %= data.lx
#             center_vertex3[1] %= data.ly
#             n1 = geometry.unit_vector_boundary_check(center_vertex1, center_vertex2, data)
#             n2 = geometry.unit_vector_boundary_check(center_vertex1, center_vertex3, data)
            
#             # equation from paper
#             da = 1 / 2 * (l1 * n1 + l2 * n2)
#             # calculate dp/dhijk
#             # calculate the unit vector pointing from the center vertex to the 
#             # other vertices making up the shared edges between current cell
#             t1 = geometry.unit_vector_boundary_check(v, s1[1], data)
#             t2 = geometry.unit_vector_boundary_check(v, s2[1], data)
#             if v == data.v: # TEST
#                 print("T Vectors:")
#                 print(t1)
#                 print(t2)
#             # equation from paper
#             dp = -1 * (t1 + t2)
#             if v == data.v: # TEST
#                 print("dp:")
#                 print(n1)
#                 print(n2)
#             # calculate force from specific cell
#             # equation from paper
#             de = (
#                 2 * data.KA * (comp_cells[i].area - data.A0) * da + 
#                 2 * data.KP * (comp_cells[i].perimeter - data.P0) * dp
#                 )
#             force += de
#             if v == data.v: # TEST
#                 print("de:")
#                 print(de)
#         forces.append(force)
#     return forces