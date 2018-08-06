# File: run.py
#
# Main file for OCT-Tools
#
#
#
# @dateCreated: ??
# @authors: Arlem Aleida Castillo Avila, Felipe Orihuela-Espina
# @dateModified: 4-Aug-2018
#
# See also:
# 


#
# LOG:
# 4-Aug-2018: FOE: Isolated minimal solution
# 

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QTabWidget, QPushButton, QGraphicsView, QLabel, QAction, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic
from OCTToolsMainWindow import *

print("OCT-Tools: Initiating...")
#Instancia para iniciar una aplicación
app = QApplication(sys.argv)
#Crear un objeto de la clase OCTToolsMainWindow
_ventana = OCTToolsMainWindow()
#Mostra la ventana
_ventana.show()
#Ejecutar la aplicación y salir al terminar
app.exec_()
