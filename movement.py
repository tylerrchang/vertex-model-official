import vertex
import copy

def move_vertices(vert_list, data):
    # vert_list_old = copy.deepcopy(vert_list)
    forces = calc_forces(vert_list, data) # returns a list
    for vert, force in zip(vert_list, forces):
        # add force and check for out of bounds
        vert.x = (vert.x + force[0]) % data.lx
        vert.y = (vert.y + force[1]) % data.ly
    # check for T1 transitions
        # lots of checks 
    # set new parameters
    # 1. polygons need to get updated
    for cell_ in data.cell_list:
        cell_.create_cell_polygon()


def calc_forces(vert_list, data):
    forces = []
    for _ in range(len(vert_list)):
        forces.append([1, 1])
    return forces