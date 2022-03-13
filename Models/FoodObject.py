from .WorldObject import WorldObject

class FoodObject(WorldObject):
    def __init__(self, location, foodWidth, foodHeight):
        super().__init__(location, foodWidth, foodHeight)