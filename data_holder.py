import vertex
import cell
"""
Class that holds information about the entire system
"""
class Data_Holder:
    def __init__(self, vert_list, cell_list, KA = 1, KP = 1, \
                 dt = 0.01, D = 2, v0 = 0.01, max_time = 2, p0 = 1):
        """
        Initializes new Data_Holder
        vert_list = numpy.array
        cell_list = list of cell indices (because numpy.arrays are more difficult to work
            with when they are not all the same length
        all remaining parameters floats
        """
        # each cell's area is normalized to 1
        self.A0 = 1
        self.P0 = p0 * self.A0 ** (1 / 2)

        # dimensions of simulation are calculated based on total number of cells
        self.lx = (len(cell_list)) ** (1 / 2) 
        self.ly = (len(cell_list)) ** (1 / 2)

        self.KA = KA
        self.KP = KP
        self.dt = dt
        self.D = D
        self.v0 = v0
        self.min_d = self.lx / 100 # minimum distance that vertices must be for t1 transition
        self.max_time = max_time
        self.vert_list = [vertex.Vertex(v[0], v[1]) for v in vert_list]

        # below attributes rely on above attributes
        self.cell_list = self.__create_cell_list(cell_list) # requires vert_list to be defined
        self.vert_adjcent_cells = self.__set_vert_adjcent_cells() # requires vert_list and cell_list to be defined

    # def __set_AP(self, cell_list):
    #     """
    #     Calculates A0 and P0

    #     Returns a tuple
    #     """
    #     # total area divided by num of cells
    #     A0 = self.lx * self.ly / len(cell_list)
    #     # formula for perimeter of retular hexagon with area above
    #     P0 = (3 ** 0.25) * ((8 * A0) ** (0.5))
    #     return (A0, P0)

    def __set_vert_adjcent_cells(self):
        """
        Tracks what vertices are connected to which cells
        Keys = vertices
        Values = list of cell objects adjcent to that vertex

        Returns a dictionary
        """
        
        vert_adjcent_cells = {}

        # goes through vertices of each cell and checks against current vertex
        for v in self.vert_list:
            vert_adjcent_cells[v] = []
            for single_cell in self.cell_list:
                for v_cell in single_cell.vert_obj_list:
                    if v == v_cell:
                        vert_adjcent_cells[v].append(single_cell)
                        # each cell can contain the same vertex only once
                        break

        return vert_adjcent_cells

    def __create_cell_list(self, cell_list):
        """
        Creates list of cell objects for the data_holder object
        Called in the constructor

        Returns a list
        """

        all_cells = []

        # loop through each row, where a single row represents the indices
        # of vertex objects that make up a single polygon
        for cell_indices in cell_list:
            # list comprehension to add those vertices to a list
            cell_vertex_objects = [
                self.vert_list[vertex_idx] for vertex_idx in cell_indices]
            # add final cell object to list
            all_cells.append(cell.Cell(cell_vertex_objects, self))

        return all_cells