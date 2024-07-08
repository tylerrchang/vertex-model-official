from shapely.geometry import Polygon
import vertex
import cell
import data_holder

def read_vertices(filepath):
    """
    Parses vertices in txt file given
    """

    vert_list = [] # List of tuples with all verticies
    data = ""

    # Try reading in file, if fail return None
    try:
        with open(filepath) as f:
            data = f.read()
    except FileNotFoundError:
        print("No file found")
        return None
    
    # Parse data
    for line in data.split("\n"):
        coords = line.split("\t")
        vertex = (float(coords[0]), float(coords[1]))
        vert_list.append(vertex)

    print(vert_list)
    return vert_list

def read_polygon_vertices(filepath):
    """
    Parses vertices of each polygon in txt file given
    """

    poly_list = [] # List of lists with a list element for each polygon's vertices
    data = ""

    # Try reading in file, if fail return None
    try:
        with open(filepath) as f:
            data = f.read()
    except FileNotFoundError:
        print("No file found")
        return None
    
    # Parse data
    for line in data.split("\n"):
        vert_list = []
        for v in line.split("\t"):
            vert_list.append(int(v.strip()))
        poly_list.append(vert_list)

    return poly_list

def create_vertices(vert_list):
    """
    Makes list of vertice objects
    """
    vertices = [] # List of vertex objects

    # loop over tuples + create and add to vertieces
    for x,y in vert_list:
        vertices.append(vertex.Vertex(x, y))

    return vertices

def create_cells(all_vertices, poly_list, data):
    """
    Makes list of cells

    Param: all_vertices has objects
    """
    cell_list = [] # Stores cell objects

    # go through each list of vertex indicies from read in data
    for vert_list in poly_list:

        polygon_vertex_objects = [] # holds vertex objects

        for v in vert_list:
            polygon_vertex_objects.append(all_vertices[v])

        cell_list.append(cell.Cell(polygon_vertex_objects, data))

    return cell_list

def read_data(vert_file_path, poly_file_path):
    """
    Reads all data and returns a Data_Holder object
    """

    vert_list = read_vertices(vert_file_path)
    vert_obj_list = create_vertices(vert_list)

    cell_indices_list = read_polygon_vertices(poly_file_path)

    # there is a bit of a circular dependence here -- must initialize object first then call create_cells
    data = data_holder.Data_Holder(vert_obj_list, None)

    cell_list = create_cells(vert_obj_list, cell_indices_list, data)

    data.cell_list = cell_list

    return data

