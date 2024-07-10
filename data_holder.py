class Data_Holder:
    def __init__(self, vert_list, cell_list, lx = 5, ly = 5):
        self.vert_list = vert_list
        self.cell_list = cell_list
        self.lx = lx
        self.ly = ly
        self.vert_adjcent_cells = None

        # need to add parameters
        # this will prob expand out consturctor
    def setAP(self):
        self.A0 = self.lx * self.ly / len(self.cell_list)
        self.P0 = (self.A0 / ((3 ** (3 / 2)) / 2)) ** 0.5
