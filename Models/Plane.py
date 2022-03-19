import numpy as np

class Plane():
    def __init__(self, location: tuple, dx: int, dy: int = None):
        self.dx = dx
        if dy == None:
            self.dy = dx
        else:
            self.dy = dy
        
        self.Cartesian = self.__asCartesian()

    def __asCartesian(self) -> np.ndarray:
        matrix = []
        for dx_i in range(-self.dx, self.dx+1):
            row = []
            for dy_i in range(-self.dy, self.dy+1):
                row.append([dx_i, dy_i])
            matrix.append(row)
        return np.array(matrix)

    