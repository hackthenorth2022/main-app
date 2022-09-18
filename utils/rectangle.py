class Rectangle:
    def __init__(self, bottomLeft, topRight):
        self.minX = bottomLeft.x
        self.maxX = topRight.x
        self.minY = bottomLeft.y
        self.maxY = topRight.y

    def inRangeX(self, x_coord):
        if x_coord > self.maxX:
            return 1
        if x_coord < self.minX:
            return -1
        return 0

    def inRangeY(self, y_coord):
        if y_coord > self.maxY:
            return 1
        if y_coord < self.minY:
            return -1
        return 0

    def inArea(self, x_coord, y_coord):
        return self.inRangeX(x_coord) == 0 and self.inRangeY(y_coord) == 0

    def sameRectangleY(self, rect):
        return self.maxY > rect.minY and self.minY < rect.maxY
