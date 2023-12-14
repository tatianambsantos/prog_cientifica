class MyCurve:
    def __init__(self,_p1=None,_p2=None):
        self.m_p1 = _p1
        self.m_p2 = _p2
    def setP1(self,_p1):
        self.m_p1 = _p1
    def setP2(self,_p2):
        self.m_p2 = _p2
    def getP1(self):
        return self.m_p1
    def getP2(self):
        return self.m_p2