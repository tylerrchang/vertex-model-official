import geometry

class Cell:
    def __init__(self, vert_list, data):
        self.vert_obj_list = vert_list
        self.data = data

        # sets fake_polygon, area, and perimeter
        self.create_cell_polygon()
    
    def __str__(self):
        return(f"Polygon with vertices: {self.vert_obj_list}")
    
    def __repr__(self):
        return self.__str__()
    
    def create_cell_polygon(self):
        """
        Creates polygon, calculates area and perimeter
        """
        self.fake_polygon = geometry.create_polygon(self.vert_obj_list, self.data)
        self.area = self.__calc_area()
        self.perimeter = self.__calc_perimeter()

    def __calc_area(self):
        area = 0
        coords = self.fake_polygon
        for i in range(len(coords)):
            area += coords[i][0] * coords[(i + 1) % len(coords)][1] - coords[i][1] * coords[(i + 1) % len(coords)][0]
        area /= 2
    
    def __calc_perimeter(self):
        perimeter = 0
        for i in range(len(self.fake_polygon) - 1):
            if i == 0:
                perimeter += geometry.distance_formula(self.fake_polygon[i], 
                                                       self.fake_polygon[-1])
            perimeter += geometry.distance_formula(self.fake_polygon[i], 
                                                       self.fake_polygon[i + 1])
        return perimeter

    def get_area(self):
        return self.area

    def get_perimeter(self):
        return self.perimeter