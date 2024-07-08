import vertex
import data_holder

def __vertex_boundary_check(v1, v2, data):
    """
    Takes 2 vertices and returns a list vertex of the second vertex if it
    needs adjustment
    """
    next_vertex = [v2[0], v2[1]]

    if abs(v1[0] - v2[0]) > data.lx / 2:
        next_vertex[0] -= data.lx
    if abs(v1[1] - v2[1]) > data.ly / 2:
        next_vertex[1] -= data.ly

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

def distance_formula(v1, v2):
    return ((v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2 ) ** (1 / 2)
