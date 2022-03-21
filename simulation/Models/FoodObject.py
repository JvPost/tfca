from .WorldObject import WorldObject

class FoodObject(WorldObject):
    def __init__(self, foodWidth, foodHeight):
        super().__init__(foodWidth, foodHeight)