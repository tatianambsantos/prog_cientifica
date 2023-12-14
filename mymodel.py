
from mycurve import MyCurve
from mypoint import MyPoint
import json


class MyModel:

    def __init__(self):
        self.m_verts = []
        '''
        p1 = MyPoint(100.0,100.0)
        p2 = MyPoint(200.0,100.0)
        p3 = MyPoint(150.0,175.0)
        self.m_verts.append(p1)
        self.m_verts.append(p2)
        self.m_verts.append(p3)
        '''
        self.m_curves = []
        self.x_min = 0
        self.x_max = 100
        self.y_min = 0
        self.y_max = 100
        self.delta = 20

        self.temp_top = 0
        self.temp_bottom = 0
        self.temp_esq = 0
        self.temp_dir = 0

        self.num_lines = int((self.y_max - self.y_min)/self.delta + 1)
        self.num_cols = int((self.x_max - self.x_min) / self.delta + 1)

        #mapeamento das particulas no grid
        #[bordo, temperatura, coord_x, coord_y]
        self.grid = []

        #lista dos stencils de cada particula
        self.connect = []
        self.coordinates_index_map = {}


    def setVerts(self,_x,_y):
        self.m_verts.append(MyPoint(_x,_y))
    def getVerts(self):
        return self.m_verts
    def setCurve(self,_x1,_y1,_x2,_y2):
        self.m_curves.append(MyCurve(MyPoint(_x1,_y1),MyPoint(_x2,_y2)))
    def getCurves(self):
        return self.m_curves
    def isEmpty(self):
        return (len(self.m_verts) == 0) and (len(self.m_curves) == 0)
    def getBoundBox(self):
        if (len(self.m_verts) < 1) and (len(self.m_curves) < 1):
            return 0.0,10.0,0.0,10.0
        if len(self.m_verts) > 0:
            xmin = self.m_verts[0].getX()
            xmax = xmin
            ymin = self.m_verts[0].getY()
            ymax = ymin
            for i in range(1,len(self.m_verts)):
                if self.m_verts[i].getX() < xmin:
                    xmin = self.m_verts[i].getX()
                if self.m_verts[i].getX() > xmax:
                    xmax = self.m_verts[i].getX()
                if self.m_verts[i].getY() < ymin:
                    ymin = self.m_verts[i].getY()
                if self.m_verts[i].getY() > ymax:
                    ymax = self.m_verts[i].getY()
        if len(self.m_curves) > 0:
            if len(self.m_verts) == 0:
                xmin = min(self.m_curves[0].getP1().getX(),self.m_curves[0].getP2().getX())
                xmax = max(self.m_curves[0].getP1().getX(),self.m_curves[0].getP2().getX())
                ymin = min(self.m_curves[0].getP1().getY(),self.m_curves[0].getP2().getY())
                ymax = max(self.m_curves[0].getP1().getY(),self.m_curves[0].getP2().getY())
            for i in range(1,len(self.m_curves)):
                temp_xmin = min(self.m_curves[i].getP1().getX(),self.m_curves[i].getP2().getX())
                temp_xmax = max(self.m_curves[i].getP1().getX(),self.m_curves[i].getP2().getX())
                temp_ymin = min(self.m_curves[i].getP1().getY(),self.m_curves[i].getP2().getY())
                temp_ymax = max(self.m_curves[i].getP1().getY(),self.m_curves[i].getP2().getY())
                if temp_xmin < xmin:
                    xmin = temp_xmin
                if temp_xmax > xmax:
                    xmax = temp_xmax
                if temp_ymin < ymin:
                    ymin = temp_ymin
                if temp_ymax > ymax:
                    ymax = temp_ymax
        print(xmin,xmax,ymin,ymax)
        return xmin,xmax,ymin,ymax
    

    def createMesh(self, x_min, x_max, y_min, y_max, delta, temp_top, temp_bottom, temp_esq, temp_dir):
        print(temp_top, temp_bottom, temp_esq, temp_dir)
        self.num_lines = int((y_max - y_min)/delta + 1)
        self.num_cols = int((x_max - x_min) / delta + 1)
        self.setCurve(x_min, y_min, x_max, y_min)
        self.setCurve(x_min, y_min, x_min,y_max)
        self.setCurve(x_max, y_min, x_max, y_max)
        self.setCurve(x_min, y_max, x_max, y_max)

        index = 1
        for i in range(self.num_lines):
            for j in range(self.num_cols):

                # build grid
                x = x_min + j * self.delta
                y = y_min + i * self.delta
                self.setVerts(x, y)

                if i == 0:
                    self.grid.append([1,temp_bottom,x,y])
                elif i == self.num_lines - 1:
                    self.grid.append([1,temp_top,x,y])
                elif j == 0:
                    self.grid.append([1,temp_esq,x,y])
                elif j == self.num_cols - 1:
                    self.grid.append([1,temp_dir,x,y])
                else:
                    self.grid.append([0,0,x,y])


                self.coordinates_index_map[(i,j)] = index 
                
                index = index + 1
            
        print(self.grid)
        #cria o stencil de cada particula e adiciona em connect
        for i in range(self.num_lines):
            for j in range(self.num_cols):
                
                stencil = [0,0,0,0,self.coordinates_index_map[(i,j)]]

                if j - 1 >= 0:
                    stencil[0] = self.coordinates_index_map[(i,j-1)]
                if j + 1 <= self.num_cols-1:
                    stencil[1] = self.coordinates_index_map[(i,j+1)]
                if i - 1 >= 0:
                    stencil[2] = self.coordinates_index_map[(i-1,j)]
                if i + 1 <= self.num_lines-1:
                    stencil[3] = self.coordinates_index_map[(i+1,j)]
                
                self.connect.append(stencil)
        print("created stencil")

        with open("teste.json", "w") as data_json:
            json.dump({'cc': self.get_boundary_conditions(), 'connection_map': self.connect}, data_json, indent=4)    
        
        
    def get_boundary_conditions(self):
        return [[b,t] for [b,t,_,_] in self.grid]
    
    def get_window_coordinates(self):
        # we assume that the real world coordinates are from 0 to 100
        # coordinates in Qt go from -1 to 1 
        return [[x / 50 -1, y / 50 -1] for [_,_,x,y] in self.grid]
    
        