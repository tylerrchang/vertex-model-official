import vertex
import numpy as np
import geometry

"""
Class that calculates the forces acting on each vertex based on the system and
applies the force to the vertices, the total energy of the system, the t1 transition
"""

def move_vertices(vert_list, data):
    """
    Updates the vertices in the data_holder object
    """
    forces = calc_forces(vert_list, data) # returns a list
    for vert, force in zip(vert_list, forces):
        # add force and check for out of bounds
        sum_x = 0
        sum_y = 0
        neighbor_count = len(data.vert_adjcent_cells[vert])
        for cell in data.vert_adjcent_cells[vert]:
            sum_x += cell.rand_move_vector[0]
            sum_y += cell.rand_move_vector[1]
        vert.x = (vert.x - force[0] * data.dt + 1 / neighbor_count * sum_x * data.dt) % data.lx
        vert.y = (vert.y - force[1] * data.dt + 1 / neighbor_count * sum_y * data.dt) % data.ly
        # no noise motion
        # vert.x = (vert.x + 1 / neighbor_count * sum_x) % data.lx
        # vert.y = (vert.y + 1 / neighbor_count * sum_y) % data.ly
        
    # update polygons with new vertices (this involves creating a new fake polygon)
    for cell_ in data.cell_list:
        cell_.create_cell_polygon()


def calc_forces(vert_list, data):
    """
    Calculates forces necessary to act on vertices for a single step
    """
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
            # current vertex
            s1 = geometry.find_shared_edge(comp_cells[i], comp_cells[(i + 1) % len(comp_cells)], v)
            s2 = geometry.find_shared_edge(comp_cells[i], comp_cells[(i + 2) % len(comp_cells)], v)

            # calculate da/dhijk
            # calculate length of shared edge between 2 other cells
            l1 = geometry.distance_formula_boundary_check(s1[0], s1[1], data)
            l2 = geometry.distance_formula_boundary_check(s2[0], s2[1], data)

            # calculate dp/dhijk
            # calculate vector normal to each shared edge, the vector points 
            # away from the center of the cell
            # calculate the unit vector pointing from the center vertex to the 
            # other vertices making up the shared edges between current cell
            # and remaining cells with the vertex
            t1 = geometry.unit_vector_boundary_check(v, s1[1], data)
            t2 = geometry.unit_vector_boundary_check(v, s2[1], data)

            # taken from paper
            dp = -1 * (t1 + t2)

            # calculate normal vector
            center_vertex_unit_vector = geometry.unit_vector_boundary_check(v, comp_cells[i].center, data)
            n1 = geometry.unit_vector_perp_to_edge(t1, center_vertex_unit_vector, data)
            n2 = geometry.unit_vector_perp_to_edge(t2, center_vertex_unit_vector, data)

            # taken from paper
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
        total_energy += (cell.area/data.A0 - data.A0/data.A0) ** 2 + data.KP * \
            (cell.perimeter/(data.A0 ** (1/2)) - data.P0/(data.A0 ** (1/2))) ** 2 / \
            (data.A0 * data.KA)
        
    return total_energy

def t1_transition_check(data, completed_transition):
    """
    Checks all vertices to see if t1 transition is necessary
    """
    # loop each cell
    for cell in data.cell_list:
        verts = cell.vert_obj_list
        # loop over each edge in the cell
        for i in range(len(verts)):
            # check length
            if (
                geometry.distance_formula_boundary_check(
                    verts[i], verts[(i + 1) % len(verts)], data
                )
                <= data.min_d
            ):
                # keep track of edges that already were t1 transitioned in this step
                # by tracking the edges
                ids = id(verts[i]) + id(verts[(i + 1) % len(verts)])
                if ids not in completed_transition:
                    completed_transition.add(ids)
                    t1_transition(verts[i], verts[(i + 1) % len(verts)], data)
                    t1_transition_check(data, completed_transition)
                    break
        


def t1_transition(v1, v2, data):
    """
    Carries out the t1 transition
    """
    # when t1 transition is across boundary
    if geometry.distance_formula(v1, v2) > data.min_d:
        # copy original vertex objects and shift new vertices to just outside
        # boundaries so the vertices can rotate correctly
        v2_prime = geometry.return_second_vertex(v1, v2, data)
        v2_prime_obj = vertex.Vertex(v2_prime[0], v2_prime[1])
        v1_prime = geometry.return_second_vertex(v2, v1, data)
        v1_prime_obj = vertex.Vertex(v1_prime[0], v1_prime[1])
        # rotate vertices
        geometry.rotate_90_degrees(v2, v1_prime_obj, data)
        geometry.rotate_90_degrees(v1, v2_prime_obj, data)
    # t1 transition not across boundary
    else:
        geometry.rotate_90_degrees(v2, v1, data)
    
    # adjusts vertices assiciated with the 4 cells involved in a t1 transition,
    # also updates the vert_adjcent_cells associated with data_holder
    mod_cell_list = [None, None]
    v = [v1, v2]
    for i in range(2):
        for cell in data.vert_adjcent_cells[v[i]]:
            vert_list = cell.vert_obj_list
            if v[(i + 1) % 2] not in vert_list:
                vert_list.insert((vert_list.index(v[i]) + 1) % len(vert_list), v[(i + 1) % 2])
                mod_cell_list[i] = cell
                break

    for i in range(2):
        for cell in data.vert_adjcent_cells[v[i]]:
            vert_list = cell.vert_obj_list
            if cell != mod_cell_list[i] and vert_list[(vert_list.index(v[i]) + 1) % len(vert_list)] == v[(i + 1) % 2]:
                vert_list.remove(v[i])
                data.vert_adjcent_cells[v[i]].remove(cell)
                data.vert_adjcent_cells[v[i]].append(mod_cell_list[(i + 1) % 2])
                break
