class Rectangle:
    def __init__(self, bottomLeft, topRight):
        self.minX = bottomLeft.x
        self.maxX = topRight.x
        self.minY = bottomLeft.y
        self.maxY = topRight.y

    def inRangeX(self, x_coord):
        return x_coord <= self.maxX and x_coord >= self.minX

    def inRangeY(self, y_coord):
        return y_coord <= self.maxY and y_coord >= self.minY

    def inArea(self, x_coord, y_coord):
        return self.inRangeX(x_coord) and self.inRangeY(y_coord)

    def sameRectangleY(self, rect):
        return self.maxY > rect.minY and self.minY < rect.maxY
