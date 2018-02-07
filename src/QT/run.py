import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QTabWidget, QPushButton, QGraphicsView, QLabel, QAction, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic
from views import *

#Instancia para iniciar una aplicación
app = QApplication(sys.argv)
#Crear un objeto de la clase
_ventana = Ventana()
#Mostra la ventana
_ventana.show()
#Ejecutar la aplicación
app.exec_()