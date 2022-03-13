class WorldObject:
    def __init__(self, location : tuple, width, height):
        self.X, self.Y = location
            
        self.Width = width
        if self.Width%2 == 0:
            self.Width = self.Width + 1
            
        self.Height = height
        if self.Height%2 == 0:
            self.Height = self.Height + 1
