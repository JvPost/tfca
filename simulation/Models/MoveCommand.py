import math

class MoveCommand():
    def __init__(self, dx, dy):
        self.dx = dx 
        self.dy = dy
        self.dist = math.sqrt(dx**2 + dy**2)
        
    def get(self):
        return (self.dx, self.dy)
    
    def add(self, dx, dy):
        self.dx += dx
        self.dy += dy
        self.dist = math.sqrt(dx**2 + dy**2)