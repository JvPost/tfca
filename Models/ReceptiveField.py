import numpy as np

class ReceptiveField():
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def AsCartesian(self):
        plain = []
        for i, x in enumerate(self.X):
            row = []
            for j, y in enumerate(self.Y):
                row.append([x,y])
            plain.append(row)

        return np.array(plain)
            

    