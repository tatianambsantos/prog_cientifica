class MyPoint:
    def __init__(self,_x=0,_y=0):
        self.m_x = _x
        self.m_y = _y
    def setX(self,_x):
        self.m_x = _x
    def setY(self,_y):
        self.m_y = _y
    def getX(self):
        return self.m_x
    def getY(self):
        return self.m_y