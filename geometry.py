import vertex
import data_holder
import numpy as np

def __vertex_boundary_check(v1, v2, data):
    """
    Takes 2 vertices and returns a list vertex of the second vertex if it
    needs adjustment

    
    vvvvvvvvvvvvv
    Used Strictly for polygon!!!
    ^^^^^^^^^^^^^^^^^^

    """
    next_vertex = [v2[0], v2[1]]
    
    if abs(v1[0] - v2[0]) > data.lx / 2:
        next_vertex[0] = abs(next_vertex[0] - data.lx)
    if abs(v1[1] - v2[1]) > data.ly / 2:
        next_vertex[1] = abs(next_vertex[1] - data.ly)

    return next_vertex

def create_polygon(vert_list, data):
    """
    Takes list of vertex objects and creates a polygon in list of list format
    """

    vertices = []

    for v in vert_list:
        vertices.append([v.x, v.y])

    for i in range(len(vertices) - 1):
        vertices[i + 1] = __vertex_boundary_check(vertices[i], vertices[i + 1], data)
    
    return vertices

def __return_second_vertex(v1, v2, data):
    next_vertex = [v2[0], v2[1]]
    # check if either boundary is broken
    if abs(v1[0] - v2[0]) > data.lx / 2:
        if v1[0] > v2[0]:
            next_vertex[0] = v2[0] + data.lx
        else:
            next_vertex[0] = v2[0] - data.lx
    if abs(v1[1] - v2[1]) > data.ly / 2:
        if v1[1] > v2[1]:
            next_vertex[1] = v2[1] + data.lx
        else:
            next_vertex[1] = v2[1] - data.lx
    return next_vertex

def distance_formula(v1, v2):
    return ((v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2 ) ** (1 / 2)

def distance_formula_boundary_check(v1, v2, data):
    # compute distance between points
    xdist = v1[0] - v2[0]
    ydist = v1[1] - v1[1]
    # if xdist is greater than half of lx, then the round() term becomes a 1
    # we then have the signed distance between the two points
    # similar logic for dy
    dx = xdist - data.lx * round(xdist / data.lx)
    dy = ydist - data.ly * round(ydist / data.ly)
    # then we can return the distance formula using dx and dy
    return (dx ** 2 + dy ** 2) ** (1 / 2)

# def midpoint_formula(v1, v2):
#     return np.array([(v1[0] + v2[0]) / 2, (v1[1] + v2[1]) / 2])

# def midpoint_formula_boundary_check(v1, v2, data):
#     v2 = __return_second_vertex(v1, v2, data)
#     return midpoint_formula(v1, v2) % np.array([data.lx, data.ly])

def unit_vector_boundary_check(v1, v2, data):
    temp = v1
    v1 = v2
    v2 = temp
    # compute distance between points
    xdist = v1[0] - v2[0]
    ydist = v1[1] - v2[1]
    # if xdist is greater than half of lx, then the round() term becomes a 1
    # we then have the signed distance between the two points
    # similar logic for dy
    dx = xdist - data.lx * round(xdist / data.lx)
    dy = ydist - data.ly * round(ydist / data.ly)
    vector = np.array([dx, dy])
    magnitude = ((vector ** 2).sum()) ** (1 / 2)
    return vector / magnitude

def find_shared_edge(cell1, cell2, v1):
    for cell1_vert in cell1.vert_obj_list:
        if cell1_vert != v1:
            for cell2_vert in cell2.vert_obj_list:
                if cell1_vert == cell2_vert:
                    return (v1, cell1_vert)
    raise ValueError