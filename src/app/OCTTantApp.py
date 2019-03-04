"""
-*- coding: utf-8 -*-

File: OCTantApp.py

Class OCTantApp

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
| 13-Feb-2019 | FOE    | - Updated support for version control. See version.py|
+-------------+--------+------------------------------------------------------+   
| 28-Feb-2019 | FOE    | - Rebranded as OCTantApp.py                          |
|             |        | - Adapted to new package OCTant structure.           |
|             |        | - Importing statements for classes within the        |
|             |        |   OCTant package have been updated.                  |
+-------------+--------+------------------------------------------------------+   
|  3-Mar-2019 | FOE    | - Tools window is now a child dock of DocumentWindow |
|             |        |   which is left as the only QMainWindow of the app.  |
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
sys.path.insert(0, '..') #This line is not needed while
                    #working in the interpreter, as the main file is in the
                    #same directory. However, it is needed by pynsist when
                    #it creates the installer, so that it "sees" the src
                    #folder.

from PyQt5.QtWidgets import QApplication
#, QMainWindow, QWidget, QHBoxLayout, QTabWidget, QPushButton, QGraphicsView, QLabel, QAction, QFileDialog
#from PyQt5.QtGui import QIcon, QPixmap
#from PyQt5 import uic


from version import __version__
from DocumentWindow import DocumentWindow
#from ToolsDock import ToolsDock


## Class definition
class OCTantApp():
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
        #self.toolsWindow = ToolsDock()
        self.docWindow = DocumentWindow()
        #self.toolsWindow.connectDocumentWindow(self.docWindow)
        #self.docWindow.connectToolsWindow(self.toolsWindow)


    def show(self):
        #self.toolsWindow.show()
        self.docWindow.show()
        

#This is the application entrance point. Note that it is NOT a method of the OCTToolsApp class
def main():
    print("OCTant App v" + __version__ + ": Initiating...")
    #Instancia para iniciar una aplicación
    app = QApplication(sys.argv)
    
    #Show the windows
    tmp = OCTantApp()
    tmp.show()
    
    #Ejecutar la aplicación y salir al terminar
    sys.exit(app.exec_())

# The following two lines, allow me to run the program from the interpreter
#"as a script", while the above method main() allow me to have an entrance
#point so that it is possible to call the method from an installed version
#of the application
if __name__ == "__main__":
    main()