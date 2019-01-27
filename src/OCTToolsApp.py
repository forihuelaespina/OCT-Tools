"""
-*- coding: utf-8 -*-

File: OCTToolsApp.py

Class OCTToolsApp

Application entrance point.

:Log:

+-------------+--------+------------------------------------------------------+   
| Date        | Author | Description                                          |
+=============+========+======================================================+
| Feb-2018    | AACA   | - File created as run.py                             |
+-------------+--------+------------------------------------------------------+   
| 4-Aug-2018  | FOE    | - Isolated minimal solution.                         |
+-------------+--------+------------------------------------------------------+   
| 21-Aug-2018 | FOE    | - Updated main window class from OCTToolsMainWindow  |
|             |        |   to IOT_GUI_MainWindow (later rebranded as          |
|             |        |   IOT_GUI_ToolsWindow                                |
+-------------+--------+------------------------------------------------------+   
| 22-Aug-2018 | FOE    | - Run is now a class. File rebranded to OCTToolsApp  |
|             |        |   from run.py                                        |
|             |        | - The application main window is no longer the tools |
|             |        |   menu window (IOT_GUI_ToolsWindow), but the document|
|             |        |   window (IOT_GUI_DocumentWindow).                   |
+-------------+--------+------------------------------------------------------+   
| 9-Sep-2018  | FOE    | - "Separated" the entry points as a script, from the |
|             |        |   entry point as an installed program.               |
|             |        | - Added "src" to the path for "installed" execution. |
+-------------+--------+------------------------------------------------------+
| 23-Sep-2018 | FOE    | - Updated comments and added Sphinx                  |
|             |        |   documentation to the class                         |
+-------------+--------+------------------------------------------------------+
| 14-Nov-2018 | FOE    | - Connected the tools window to the document window. |
+-------------+--------+------------------------------------------------------+   

.. seealso:: None
.. note:: None
.. todo:: None
    
 
.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Arlem Aleida Castillo Avila <acastillo@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""


## Import
import sys
#Add paths
sys.path.insert(0, 'src') #This line is not needed while
                    #working in the interpreter, as the main file is in the
                    #same directory. However, it is needed by pynsist when
                    #it creates the installer, so that it "sees" the src
                    #folder.

from PyQt5.QtWidgets import QApplication
#, QMainWindow, QWidget, QHBoxLayout, QTabWidget, QPushButton, QGraphicsView, QLabel, QAction, QFileDialog
#from PyQt5.QtGui import QIcon, QPixmap
#from PyQt5 import uic


from IOT_GUI_DocumentWindow import *
from IOT_GUI_ToolsWindow import *


## Class definition
class OCTToolsApp():
    #Sphinx documentation
    """Application entrance point.
    
    Application entrance point.
    
    .. seealso:: None
    .. note:: None
    .. todo:: None
        
    """

    #Private class attributes shared by all instances

    #Class constructor
    def __init__(self):
        #Crear un objeto de la clase OCTToolsMainWindow
        self._toolsWindow = IOT_GUI_ToolsWindow()
        self._docWindow = IOT_GUI_DocumentWindow()
        self._toolsWindow.connectDocumentWindow(self._docWindow)
        self._docWindow.connectToolsWindow(self._toolsWindow)


    def show(self):
        self._toolsWindow.show()
        self._docWindow.show()
        

#This is the application entrance point. Note that it is NOT a method of the OCTToolsApp class
def main():
    print("OCT-Tools: Initiating...")
    #Instancia para iniciar una aplicación
    app = QApplication(sys.argv)
    
    #Show the windows
    tmp = OCTToolsApp()
    tmp.show()
    
    #Ejecutar la aplicación y salir al terminar
    sys.exit(app.exec_())

# The following two lines, allow me to run the program from the interpreter
#"as a script", while the above method main() allow me to have an entrance
#point so that it is possible to call the method from an installed version
#of the application
if __name__ == "__main__":
    main()