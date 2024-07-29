class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False
    
    def __hash__(self):
        return hash((id(self)))

    def __str__(self):
        return (f"V({self.x}, {self.y})")

    def __repr__(self):
        return self.__str__()
    
    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError