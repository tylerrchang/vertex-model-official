import vertex
import cell
import numpy as np
class Data_Holder:
    def __init__(self, vert_list, cell_list, KA = 1, KP = 1, \
                 dt = 0.01, D = 2, v0 = 0.01, max_time = 2, p0 = 1):
        """
        Initializes new Data_Holder
        vert_list = numpy.array
        cell_list = numpy.array
        
        all remaining parameters floats/ints
        """
        self.A0 = 1
        self.P0 = p0 * self.A0 ** (1 / 2)
        self.lx = (len(cell_list)) ** (1 / 2)
        self.ly = (len(cell_list)) ** (1 / 2)
        self.KA = KA
        self.KP = KP
        self.dt = dt
        self.D = D
        self.v0 = v0
        self.min_d = self.lx / 100
        self.max_time = max_time
        # below attributes rely on above attributes, order is important!
        # self.A0, self.P0 = self.__set_AP(cell_list)
        self.vert_list = [vertex.Vertex(v[0], v[1]) for v in vert_list]
        self.cell_list = self.__create_cell_list(cell_list)
        self.vert_adjcent_cells = self.__set_vert_adjcent_cells()

    def __set_AP(self, cell_list):
        """
        Calculates A0 and P0

        Returns a tuple
        """
        # total area divided by num of cells
        A0 = self.lx * self.ly / len(cell_list)
        # formula for perimeter of retular hexagon with area above
        P0 = (3 ** 0.25) * ((8 * A0) ** (0.5))
        return (A0, P0)

    def __set_vert_adjcent_cells(self):
        """
        Creates dictionary of list of cell objects
        Keys = vertices
        Values = list of cell objects adjcent to that vertex

        Returns a dictionary
        """
        
        vert_adjcent_cells = {}

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