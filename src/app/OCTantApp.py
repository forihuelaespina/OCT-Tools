"""
-*- coding: utf-8 -*-

File: OCTantApp.py

Class OCTantApp

.. inheritance-diagram:: OCTantApp

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
| 17-Mar-2019 | FOE    | - Added properties appsettings and appsettingsfile.  |
|             |        | - docWindow attribute converted to docwindow         |
|             |        |   property.                                          |
|             |        | - Cleaner exit with call to deleteLater              |
|             |        | - Removed method show. Now the document window show  |
|             |        |   is called accesing the docwindow property.         |
|             |        | - Class OCTantApp now becomes a QApplication         |
|             |        |   (previously we had 2 separated objects; one for the|
|             |        |   QApplication and another just for "holding" the    |
|             |        |   the main window.)                                  |
+-------------+--------+------------------------------------------------------+
| 31-Mar-2019 | FOE    | - Fixed comments of property docwindow which were    |
|             |        |   referring to Settings.                             |
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
if not sys.path[0] == '..':
    sys.path.insert(0, '..')
#sys.path.append('..')
                    #This line is not needed while
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

import octant as oc

## Class definition
class OCTantApp(QApplication):
    #Sphinx documentation
    """Application entrance point.

    Application entrance point.

    .. seealso:: None
    .. note:: None
    .. todo:: None

    """

        #Private class attributes shared by all instances

    #Class constructor
    #def __init__(self, **kwargs):
    def __init__(self, kwargs): #DO NOT use the classical ** before kwargs in this case!
        print("OCTant App v" + __version__ + ": Initiating...")
        #Call superclass constructor
        super().__init__(kwargs) #For Python 3

        #Initialize private attributes unique to this instance
        self.document = None #The current document. Initialize a document
        self.docwindow = DocumentWindow(theparentapp = self)
        #self.docwindow.parentapp = self #Connect the window with the application

        self.appsettingsfile = '..\\..\\resources\\OCTantApp.config'
        self.appsettings = oc.data.Settings()

        print("Reading application settings from " +  self.appsettingsfile + ".")
        self.appsettings.read(self.appsettingsfile)
        #print(tmp.appsettings)

        #Finally, show the main window
        self.docwindow.show()

        return

#    def show(self):
#        #self.toolsWindow.show()
#        self.docwindow.show()



    #Properties getters/setters
    #
    # Remember: Sphinx ignores docstrings on property setters so all
    #documentation for a property must be on the @property method
    @property
    def document(self): #document getter
        """
        The application opened document.

        :getter: Gets the application opened document
        :setter: Sets the application opened document
        :type: class:`octant.data.Document`
        """
        return self.__document

    @document.setter
    def document(self,newDoc): #document setter
        if newDoc is None:
            newDoc = oc.data.Document() #Initialize a document
        if (type(newDoc) is oc.data.Document):
            self.__document = newDoc
        else:
            warnMsg = self.getClassName() + ':document: Unexpected document type.'
            warnings.warn(warnMsg,SyntaxWarning)
        return None

    @property
    def docwindow(self): #appsettings getter
        """
        Access the application main window

        :getter: Gets the application main window
        :setter: Sets the application main window
        :type: class:`octant.app.DocumentWindow`
        """
        return self.__docwindow

    @docwindow.setter
    def docwindow(self,newDocWindow): #document setter
        if newDocWindow is None:
            newDocWindow = DocumentWindow() #Initialize settings
        if (type(newDocWindow) is DocumentWindow):
            self.__docwindow = newDocWindow
        else:
            warnMsg = self.getClassName() + ':docwindow: Unexpected docwindow type.'
            warnings.warn(warnMsg,SyntaxWarning)
        return None

    @property
    def appsettings(self): #appsettings getter
        """
        The application settings.

        :getter: Gets the application settings
        :setter: Sets the application settings
        :type: class:`octant.data.Settings`
        """
        return self.__appsettings

    @appsettings.setter
    def appsettings(self,newSettings): #document setter
        if newSettings is None:
            newSettings = oc.data.Settings() #Initialize settings
        if (type(newSettings) is oc.data.Settings):
            self.__appsettings = newSettings
        else:
            warnMsg = self.getClassName() + ':appsettings: Unexpected settings type.'
            warnings.warn(warnMsg,SyntaxWarning)
        return None

    @property
    def appsettingsfile(self): #appsettings getter
        """
        The settings file name.

        :getter: Gets the current settings file name.
        :setter: Sets the current settings file name.
        :type: str
        """
        return self.__appsettingsfile

    @appsettingsfile.setter
    def appsettingsfile(self,newFilename): #document setter
        if newFilename is None:
            newFilename = '..\\..\\resources\\OCTantApp.config' #Initialize
        if (type(newFilename) is str):
            self.__appsettingsfile = newFilename
        else:
            warnMsg = self.getClassName() + ':appsettingsfile: Unexpected settings filename type.'
            warnings.warn(warnMsg,SyntaxWarning)
        return None


#This is the application entrance point. Note that it is NOT a method of the OCTantApp class
def main():

    from OCTantApp import OCTantApp #Make the import explicit so that class type is OCTantApp instead of __main__.OCTantApp

    #Instancia para iniciar una aplicación
    myApp = OCTantApp(sys.argv) #The application object. OCTantApp is a QApplication
    #myApp = OCTantApp() #OCTantApp is a QApplication
    myApp.aboutToQuit.connect(myApp.deleteLater) #Ensures the application is
                                    #deleted after closing, and in practice
                                    #removes a closing exception.
    #Starts the event loop and exit upon quitting
    #QApplication quits when the last primary window (window with no parent) is closed
    myApp.exec_()
    sys.exit(0)

# The following two lines, allow me to run the program from the interpreter
#"as a script", while the above method main() allow me to have an entrance
#point so that it is possible to call the method from an installed version
#of the application
if __name__ == "__main__":
    main()
