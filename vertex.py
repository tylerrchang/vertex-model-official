class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return (f"V({self.x}, {self.y})")

    def __repr__(self):
        return self.__str__()