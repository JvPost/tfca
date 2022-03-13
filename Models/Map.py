from email.policy import default
from typing import Collection
import numpy as np

from Models.WorldObject import WorldObject

class Map:
    def __init__(self, world = None, objects = None):
        if world is not None:
            self.Width = world.Width
            self.Height = world.Height
            self.ObjectDict = defaultdict(list)
            self.Objects = objects
        if objects is not None:
            self.Matrix = self.GetMapFor(objects)
            self.ObjectDict = self.GetObjectDict()
            
        
    def GetMapFor(self, objects):
        _loc = [(obj.X, obj.Y) for obj in objects]
        _map = np.zeros((self.Height, self.Width))
        for x, y in _loc:
            _map[y, x] = 1
        return _map

    def GetObjectDict(self):
        for obj in self.Objects:
            self.ObjectDict[(obj.X, obj.Y)].append(obj)

    def GetObjectList(self):
        return [obj for obj in self.Objects]
    

    
        
        