import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QTabWidget, QMenuBar, QMenu
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon

class ChildWindow(QWidget):
    def __init__(self, name=None):
        super(ChildWindow, self).__init__()
        self.name = name
        self.initUI()
 
    def initUI(self):
 
        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Child Window %s' % self.name)
        self.show()
 
class Ventana(QMainWindow):
 
    def __init__(self):
        QMainWindow.__init__(self)
        self.defineAspect()
    
    def defineAspect(self):        
        self.title = 'OCT-Tools'
        self.left = 10
        self.top = 10
        self.width = 1300
        self.height = 700
        self.children = []
        
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QHBoxLayout(self.centralwidget)
#        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(-11, 9, 271, 781))
#        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.panelDerecho = QHBoxLayout()
        self.panelDerecho.setObjectName("panelDerecho")  
        self.panelPrincipal = QHBoxLayout()        
        self.panelPrincipal.setGeometry(QRect(-11, 9, 271, 781))
        self.panelPrincipal.setStretch(1,1)
        self.tabs = QTabWidget()
        self.tabs.addTab(QWidget(), "Bienvenido")
        self.panelPrincipal.addWidget(self.tabs)
        self.panelPrincipal.setObjectName("panelPrincipal")
        self.horizontalLayoutWidget.addLayout(self.panelDerecho,1)
        self.horizontalLayoutWidget.addLayout(self.panelPrincipal,2)
        
        self.menubar = QMenuBar()
        self.menubar.setGeometry(QRect(0, 0, 1300, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.setMenuBar(self.menubar)
        
        self.initUI()
              
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)  
        child = ChildWindow(name="Hija")
        self.children.append(child)
        self.show()
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    #Crear un objeto de la clase
    _ventana = Ventana()
    #Mostra la ventana
    _ventana.show()
    #Ejecutar la aplicación
    app.exec_()