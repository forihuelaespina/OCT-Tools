# File: run.py
#
# Main file for OCT-Tools
#
#
#
# @dateCreated: ??
# @authors: Arlem Aleida Castillo Avila, Felipe Orihuela-Espina
# @dateModified: 22-Aug-2018
#
# See also:
# 


## Log
# 4-Aug-2018: FOE: Isolated minimal solution
# 
# 21-Aug-2018: FOE: Updated main window class from OCTToolsMainWindow to
#   IOT_GUI_MainWindow (later rebranded as IOT_GUI_ToolsWindow
# 
# 21-Aug-2018: FOE:
#   * Run is now a class
#   * The application main window is no longer the tools menu window (IOT_GUI_ToolsWindow),
#   but the document window (IOT_GUI_DocumentWindow)
# 


## Import
import sys
from PyQt5.QtWidgets import QApplication
#, QMainWindow, QWidget, QHBoxLayout, QTabWidget, QPushButton, QGraphicsView, QLabel, QAction, QFileDialog
#from PyQt5.QtGui import QIcon, QPixmap
#from PyQt5 import uic


from IOT_GUI_DocumentWindow import *
from IOT_GUI_ToolsWindow import *


## Class definition
class OCTToolsApp():

    #Private class attributes shared by all instances

    #Class constructor
    def __init__(self):
        pass

if __name__ == "__main__":
    print("OCT-Tools: Initiating...")
    #Instancia para iniciar una aplicación
    app = QApplication(sys.argv)
    #Crear un objeto de la clase OCTToolsMainWindow
    _toolsWindow = IOT_GUI_ToolsWindow()
    _docWindow = IOT_GUI_DocumentWindow()
    _toolsWindow.connectDocumentWindow(_docWindow)
    
    #Show the windows
    _toolsWindow.show()
    _docWindow.show()
    
    #Ejecutar la aplicación y salir al terminar
    sys.exit(app.exec_())
