import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class TextBoxMED(QWidget):

    def __init__(self, model):
        super(TextBoxMED, self).__init__()
        self.setGeometry(800, 300, 200, 100)
        self.setWindowTitle("MyGLDrawer")
        
        self.d_value = 50.0
        self.x_min = 0
        self.x_max = 100
        self.y_min = 0
        self.y_max = 100
        self.delta = 20

        #Temperaturas
        self.temp_top = 0
        self.temp_bottom = 0
        self.temp_esq = 0
        self.temp_dir = 0

        self.model = model


        self.okClicked = False
        self.label_xmin = QLabel("Insira o valor de x_min:")
        self.label_xmax = QLabel("Insira o valor de x_max: ")
        self.label_ymin = QLabel("Insira o valor de y_min: ")
        self.label_ymax = QLabel("Insira o valor de y_max: ")
        self.label_delta = QLabel("Insira o valor de delta: ")

        self.label_temp_top = QLabel("Temperatura bordo superior: ")
        self.label_temp_bottom = QLabel("Temperatura bordo inferior: ")
        self.label_temp_esq = QLabel("Temperatura bordo esquerdo: ")
        self.label_temp_dir = QLabel("Temperatura bordo direito: ")


        self.box_xmin = QLineEdit() 
        self.box_xmax = QLineEdit() 
        self.box_ymin = QLineEdit() 
        self.box_ymax = QLineEdit()

        self.box_delta = QLineEdit() 

        self.box_temp_top = QLineEdit()
        self.box_temp_bottom = QLineEdit()
        self.box_temp_esq = QLineEdit()
        self.box_temp_dir = QLineEdit()

        self.b1 = QPushButton("Confirmar")
        
        self.vbox = QVBoxLayout()

        #Tamanho malha
        self.vbox.addWidget(self.label_xmin)
        self.vbox.addWidget(self.box_xmin)
        self.vbox.addWidget(self.label_xmax)
        self.vbox.addWidget(self.box_xmax)
        self.vbox.addWidget(self.label_ymin)
        self.vbox.addWidget(self.box_ymin)
        self.vbox.addWidget(self.label_ymax)
        self.vbox.addWidget(self.box_ymax)
        self.vbox.addWidget(self.label_delta)

        #Espaçamento particulas
        self.vbox.addWidget(self.box_delta)
        self.vbox.addWidget(self.b1)

        #Temperaturas dos bordos
        self.vbox.addWidget(self.label_temp_top)
        self.vbox.addWidget(self.box_temp_top)
        self.vbox.addWidget(self.label_temp_bottom)
        self.vbox.addWidget(self.box_temp_bottom)
        self.vbox.addWidget(self.label_temp_esq)
        self.vbox.addWidget(self.box_temp_esq)
        self.vbox.addWidget(self.label_temp_dir)
        self.vbox.addWidget(self.box_temp_dir)

        self.setLayout(self.vbox)

        self.b1.clicked.connect(self.onConfClicked)
    
    def onConfClicked(self):
        try:
            self.x_min = float(self.box_xmin.text())
            self.x_max = float(self.box_xmax.text())
            self.y_min = float(self.box_ymin.text())
            self.y_max = float(self.box_ymax.text())
            self.delta = float(self.box_delta.text())

            self.temp_top = float(self.box_temp_top.text())
            self.temp_bottom = float(self.box_temp_bottom.text())
            self.temp_esq = float(self.box_temp_esq.text())
            self.temp_dir = float(self.box_temp_dir.text())
        except:
            print("erro")
        self.okClicked = True
        self.model.createMesh(self.x_min, self.x_max, self.y_min, self.y_max, self.delta, self.temp_top, self.temp_bottom, self.temp_esq, self.temp_dir)
        self.close()
        