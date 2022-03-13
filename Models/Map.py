import numpy as np

class Map:
    def __init__(self, world = None, objects = None):
        if world is not None:
            self.Width = world.Width
            self.Height = world.Height
        if object is not None:
            self.Matrix = self.GetMapFor(objects)
    
    def GetMapFor(self, objects):
        _loc = [(obj.X, obj.Y) for obj in objects]
        _map = np.zeros((self.Height, self.Width))
        for x, y in _loc:
            _map[x, y] = 1
        return _map
        
    def Slice(self, x_min, x_max, y_min, y_max) -> np.array:
        if x_min < 0:
            x_min = 0
        if x_max >= self.Width-1:
            x_max = self.Width-1
        if y_min < 0:
            y_min = 0
        if y_max >= self.Height-1:
            y_max = self.Height-1

        temp = self.Matrix.copy()
        temp[y_min:y_max+1, x_min:x_max+1] = 5

        return self.Matrix[y_min:y_max+1, x_min:x_max+1]
        
        