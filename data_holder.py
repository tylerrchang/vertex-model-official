class Data_Holder:
    def __init__(self, vert_list, cell_list, lx = 5, ly = 5, KA = 1, KP = 1, dt = 0.01, min_d = 0.1):
        self.vert_list = vert_list
        self.cell_list = cell_list
        self.lx = lx
        self.ly = ly
        self.vert_adjcent_cells = None
        self.KA = KA
        self.KP = KP
        self.dt = dt
        self.D = 5
        self.v0 = .005
        self.min_d = min_d
        # testing
        # self.v = vert_list[28]

        # need to add parameters
        # this will prob expand out consturctor
    def setAP(self):
        self.A0 = self.lx * self.ly / len(self.cell_list)
        # formula for perimeter of retular hexagon with area above
        self.P0 = (3 ** 0.25) * ((8 * self.A0) ** (0.5))

    def set_vert_adjcent_cells(self):
        vert_adjcent_cells = {}

        for v in self.vert_list:
            vert_adjcent_cells[v] = []
            for cell in self.cell_list:
                for v_cell in cell.vert_obj_list:
                    if v == v_cell:
                        vert_adjcent_cells[v].append(cell)
                        break

        self.vert_adjcent_cells = vert_adjcent_cells