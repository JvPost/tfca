from .WorldObject import WorldObject

class LocatedObject():
    def __init__(self, x: int, y: int, obj):
        self.X = x
        self.Y = y
        self.Object = obj
        