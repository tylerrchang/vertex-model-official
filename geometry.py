import vertex
import data_holder
import numpy as np

def __vertex_boundary_check(v1, v2, data):
    """
    DEPRECIATED
    
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
        vertices.append([v[0], v[1]])

    for i in range(len(vertices) - 1):
        vertices[i + 1] = __return_second_vertex(vertices[i], vertices[i + 1], data)
    
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
    ydist = v1[1] - v2[1]
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
    """
    from v1 to v2
    """
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

def unit_vector_perp_to_edge(edge_vector, center_vector, data):
    """
    Takes a unit vector and rotates it 90 degrees, pointing outward from the center of the polygon.
    Only used for polygons
    """
    # cross product of unit_vector and +z
    x = 0 * 0 - edge_vector[1] * 1
    y = -(0 * 0 - edge_vector[0] * 1)
    dot_prod = x * center_vector[0] + y * center_vector[1]
    new_vec = np.array([x, y]) * - (-1 if dot_prod < 0 else 1)
    return new_vec

# rotate 90 degrees
# https://stackoverflow.com/questions/45701615/how-can-i-rotate-a-line-segment-around-its-center-by-90-degrees
# find the center
def rotate_90_degrees(v1, v2, data):
    x1 = v1[0]
    x2 = v2[0]
    y1 = v1[1]
    y2 = v2[1]

    cx = (x1+x2)/2
    cy = (y1+y2)/2

    # move the line to center on the origin
    x1-=cx
    y1-=cy
    x2-=cx
    y2-=cy
    # rotate both points
    xtemp = x1
    ytemp = y1
    x1=-ytemp
    y1=xtemp

    xtemp = x2
    ytemp = y2
    x2=-ytemp
    y2=xtemp

    # move the center point back to where it was
    x1+=cx
    y1+=cy
    x2+=cx
    y2+=cy

    v1.x = x1
    v1.y = y1
    v2.x = x2
    v2.y = y2