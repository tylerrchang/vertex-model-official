import geometry
import numpy as np
import math

class Cell:
    def __init__(self, vert_list, data):
        self.vert_obj_list = vert_list
        self.data = data

        # generate original direction of motion of random cell motion,
        # however this is modified in the create cell polygon method

        self.theta = np.random.uniform(0, 2 * math.pi)
        self.rand_move_vector = [self.data.v0 * math.cos(self.theta), 
                                 self.data.v0 * math.sin(self.theta)]
        # sets fake_polygon, area, and perimeter
        self.total_movement = None
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
        self.__calc_area()
        self.__calc_perimeter()
        self.__calc_center()
        self.__calc_rand()

    def __calc_area(self):
        area = 0
        coords = self.fake_polygon
        for i in range(len(coords)):
            area += coords[i][0] * coords[(i + 1) % len(coords)][1] - coords[i][1] * coords[(i + 1) % len(coords)][0]
        self.area = abs(area) / 2.0

    def __calc_perimeter(self):
        perimeter = 0
        for i in range(len(self.fake_polygon) - 1):
            if i == 0:
                perimeter += geometry.distance_formula(self.fake_polygon[i], 
                                                       self.fake_polygon[-1])
            perimeter += geometry.distance_formula(self.fake_polygon[i], 
                                                       self.fake_polygon[i + 1])
        self.perimeter = perimeter

    def __calc_center(self):
        x = 0
        y = 0
        for v in self.fake_polygon:
            x += v[0]
            y += v[1]
        if self.total_movement != None:
            old_center = self.center
        self.center = np.array([x, y]) / len(self.fake_polygon)
        if self.total_movement != None:
            old_center_prime = geometry.return_second_vertex(self.center, old_center, self.data)
            increment = [self.center[0] - old_center_prime[0], self.center[1] - old_center[1]]
            self.total_movement[0] += increment[0]
            self.total_movement[1] += increment[1]
        else:
            self.total_movement = [0,0]

    def get_area(self):
        return self.area

    def get_perimeter(self):
        return self.perimeter

    def __calc_rand(self):
        # made it -1 to 1 so cell can rotate either direction
        self.theta = (self.theta + (np.random.uniform(-1, 1) * \
                    (2 * self.data.D) ** (1 / 2) * (self.data.dt) ** (1 / 2))
                    ) % (2 * math.pi)
        self.rand_move_vector = [self.data.v0 * math.cos(self.theta), 
                                 self.data.v0 * math.sin(self.theta)]
