from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from mycanvas import *
from mymodel import *
from textBox import *

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(100,100,600,400)
        self.setWindowTitle("MyGLDrawer")
        self.canvas = MyCanvas()
        self.setCentralWidget(self.canvas)
        # create a model object and pass to canvas
        self.model = MyModel()
        self.canvas.setModel(self.model)
        #Text Box
        self.textBox = TextBox(self.canvas.m_model)
        # create a Toolbar
        tb = self.addToolBar("File")
        # fit = QAction(QIcon("icons/fit.jpg"),"fit",self)
        fit = QAction("Fit",self)  # Apenas texto no botão
        draw = QAction("Desenhar", self)
        tb.addAction(draw)
        tb.actionTriggered[QAction].connect(self.tbpressed)

        # add insertText
        boxText = QAction(QIcon(r"radius.png"),"particulas",self)
        tb.addAction(boxText)

        # add fit
        fit = QAction(QIcon(r"fit.png"),"fit",self)
        tb.addAction(fit)

        # add MED
        fit = QAction(QIcon(r"json.png"),"med",self)
        tb.addAction(fit)


        tb.actionTriggered[QAction].connect(self.tbpressed)

    def tbpressed(self,a):
        if a.text() == "fit":
            self.canvas.fitWorldToViewport()
        elif a.text() == "Desenhar":
            self.canvas.drawLines = not self.canvas.drawLines
            self.canvas.update()   
        elif a.text() == "particulas":
            self.textBox.show()
        elif a.text() == "med":
            self.textBoxMED.show()