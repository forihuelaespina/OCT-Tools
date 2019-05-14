"""
-*- coding: utf-8 -*-

File: ToolsDock.py

Class ToolsDock

.. inheritance-diagram:: ToolsDock

A dockable panel for accessing tools



:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 3-Aug-2018  | FOE    | - Initial code isolated from previous file           |
|             |        |   emergentes.py                                      |
|             |        | - Explicit declaration of attributes                 |
|             |        | - "Nuevo": Ahora captura el caso de que se "cancele" |
|             |        |   la operación de abrir                              |
+-------------+--------+------------------------------------------------------+
| 5-Aug-2018  | FOE    | - Isolated minimal solution.                         |
|             |        | - menuHerramientas now rebranded menuTools           |
|             |        | - Function nuevo now rebranded abrir (because that   |
|             |        |   its what it actually does                          |
|             |        | - Desactivate not programmes menu options            |
|             |        | - Added menu File->Exit functionality                |
|             |        | - Revised image rendering algorithm. It is now open  |
|             |        |   from the beginning and automatically updates the   |
|             |        |   perfilometer with every change in the main figure. |
|             |        |   Also the gridding of the subplots has been         |
|             |        |   improved.                                          |
+-------------+--------+------------------------------------------------------+
| 21-Aug-2018 | FOE    | - Class rebranded as IOT_GUI_MainWindow              |
+-------------+--------+------------------------------------------------------+
| 22-Aug-2018 | FOE    | - Class rebranded as IOT_GUI_ToolsWindow             |
+-------------+--------+------------------------------------------------------+
| 26-Aug-2018 | FOE    | - Tools menu no longer rely on the QtDesigner        |
|             |        |   generated .ui file. Now, all butons are added      |
|             |        |   "manually" for greater control.                    |
+-------------+--------+------------------------------------------------------+
| 1-Sep-2018  | FOE    | - There is no longer a flagEditSegmentation to keep  |
|             |        |   track of when editing is possible. Instead, only   |
|             |        |   buttons related to these operations are set        |
|             |        |   enable or disabled.                                |
|             |        | - Some cleaning. Removal of unused code.             |
+-------------+--------+------------------------------------------------------+
| 23-Sep-2018 | FOE    | - Reconverted attribute _arity to property arity.    |
|             |        |   Methods getArity and setArity become deprecated,   |
|             |        |   and issue a warning.                               |
|             |        | - Updated comments and added Sphinx documentation    |
|             |        |   to the class                                       |
+-------------+--------+------------------------------------------------------+
| 14-Nov-2018 | FOE    | - Added panel for settings.                          |
|             |        | - Window title set to "IOT tools menu"               |
|             |        | - New method updateSettings                          |
|             |        | - Added tab to settings panel to control operation   |
|             |        |   class:`IOT_OperationPerfilometer`                  |
+-------------+--------+------------------------------------------------------+
|  2-Dec-2018 | FOE    | - Encapsulated the docWindow properties and          |
|             |        |   deprecated get/set pair for that property.         |
|             |        | - Minor debugging                                    |
+-------------+--------+------------------------------------------------------+
| 12-Dec-2018 | FOE    | - Added button and execute call for operation        |
|             |        |   class:`IOT_OperationMeasureThickness`              |
|             |        | - Added tab to settings panel to control operation   |
|             |        |   class:`IOT_OperationMeasureThickness`              |
|             |        | - Internal methods are now named in English          |
|             |        |   e.g. 'openDocument' instead of 'abrir'             |
|             |        | - Updated comments and added Sphinx documentation    |
|             |        |   to the class                                       |
|             |        | - Added method measureThickness to call for the      |
|             |        |   corresponding operation to be executed.            |
+-------------+--------+------------------------------------------------------+
| 20-Jan-2019 | FOE    | - Added support for the class:`IOT_OperationBrush`   |
|             |        |   operation.                                         |
+-------------+--------+------------------------------------------------------+
| 28-Feb-2019 | FOE    | - Adapted to new package OCTant structure.           |
|             |        |   Class rebranded ToolsDock.                         |
|             |        |   The prefix IOT_GUI is drop and the class is now    |
|             |        |   separated from the API.                            |
+-------------+--------+------------------------------------------------------+
|  3-Feb-2019 | FOE    | - Debugging of errors left during transition to new  |
|             |        |   package OCTant structure; wrong imports and        |
|             |        |   unupdated classes names.                           |
|             |        | - ToolsDock is now a QDockWidget (instead of a       |
|             |        |   QMainWindow). Property documentWindow has been     |
|             |        |   eliminated, and instead, calls to main window are  |
|             |        |   made using method parent().                        |
+-------------+--------+------------------------------------------------------+
| 17-Mar-2019 | FOE    | - Menu moved to application main window.             |
|             |        | - method openDocument renamed importAmiraFile.       |
|             |        | - Eliminated method closeEvent.                      |
+-------------+--------+------------------------------------------------------+
| 30-Mar-2019 | FOE    | - Button bOpenImage is now renamed bImportImage and  |
|             |        |   its label reads "Import image"                     |
+-------------+--------+------------------------------------------------------+
|  4-Apr-2019 | FOE    | - Method importAmiraFile rename importFile.          |
|             |        | - Bug fixing. In method editSegmentation, call to    |
|             |        |   parent window was still using "old" property       |
|             |        |   `documentWindow`. In now calls method parent().    |
+-------------+--------+------------------------------------------------------+

.. seealso:: None
.. note:: None
.. todo:: None


.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Arlem Aleida Castillo Avila <acastillo@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""

## Import

#import sys
import warnings


from PyQt5.QtWidgets import QDockWidget, QWidget, QGroupBox, \
        QPushButton, QVBoxLayout, QTabWidget
#from PyQt5 import uic

import octant as octant
#
#from octant.op import OpSegmentationEdit

#from DocumentWindow import DocumentWindow
#import DocumentWindow
from OpSegmentationEditToolsPanel import OpSegmentationEditToolsPanel
from SettingsGUIOpScanPerfilometer import SettingsGUIOpScanPerfilometer
from SettingsGUIOpScanMeasureThickness import SettingsGUIOpScanMeasureThickness
from SettingsGUIOpSegmentationBrush import SettingsGUIOpSegmentationBrush




###################################################################################


#Class inherited from QDockWidget
class ToolsDock(QDockWidget):
    #Sphinx documentation
    """A panel for accessing tools.

    A panel for accessing tools.


    .. seealso:: None
    .. note:: None
    .. todo:: None

    """


    #Private class attributes shared by all instances

    #Class constructor
    def __init__(self):
        """The class constructor.

        The class constructor.

        tmp = ToolsDock() - Creates a panel of GUI controls for
        operating the OCTantApp.

        """
        #Call superclass constructor
        QDockWidget.__init__(self)

        #self.documentWindow = None
        self.setWindowTitle("OCTantApp - Tools dock")

        #self.move(50,50)

        #Initialize private attributes unique to this instance
        #self._menuTools = menuTools() #Buttons of actions sequence in the main window

        #Group main operations
        self._menuTools = QGroupBox()

        bImportImage = QPushButton("Import Image")
        bImportImage.clicked.connect(self.importFile)
        bImportImage.setEnabled(True)

        bMosaicing = QPushButton("Mosaicing")
        bMosaicing.clicked.connect(self.stitch)
        bMosaicing.setEnabled(False)

        bFlattening = QPushButton("Flattening")
        bFlattening.clicked.connect(self.flatten)
        bFlattening.setEnabled(False)

        bSegment = QPushButton("Automatic segmentation")
        bSegment.clicked.connect(self.segment)
        bSegment.setEnabled(False)

        bEditSegment = QPushButton("Start edit segmentation")
        bEditSegment.clicked.connect(self.editSegmentation)
        bEditSegment.setEnabled(False)

        # bMeasureThickness = QPushButton("Measure layers thickness ")
        # bMeasureThickness.clicked.connect(self.editSegmentation)
        # bMeasureThickness.setEnabled(False)

        buttonPanelLayout = QVBoxLayout();
        buttonPanelLayout.addWidget(bImportImage);
        buttonPanelLayout.addWidget(bMosaicing);
        buttonPanelLayout.addWidget(bFlattening);
        buttonPanelLayout.addWidget(bSegment);
        buttonPanelLayout.addWidget(bEditSegment);
        #buttonPanelLayout.addWidget(bMeasureThickness);
        self._menuTools.setLayout(buttonPanelLayout);
        #self._menuTools.setVisible(True)

        #Edit segmentation panel
        self._groupEditSegmentation = OpSegmentationEditToolsPanel() #Edit segmentation tools panel


        #Tools settings panel
        self._settings = QTabWidget()

        self._settingsOperationPerfilometer = SettingsGUIOpScanPerfilometer()
        #Listen to changes in the controls
        self._settingsOperationPerfilometer.columnEditBox.returnPressed.connect(self.updateSettings)
        self._settingsOperationPerfilometer.widthEditBox.returnPressed.connect(self.updateSettings)

        self._settingsOperationMeasureThickness = SettingsGUIOpScanMeasureThickness()
        #Listen to changes in the controls
        self._settingsOperationMeasureThickness.columnEditBox.returnPressed.connect(self.updateSettings)
        self._settingsOperationMeasureThickness.windowHalfWidthEditBox.returnPressed.connect(self.updateSettings)
        self._settingsOperationMeasureThickness.pixelWidthEditBox.returnPressed.connect(self.updateSettings)
        self._settingsOperationMeasureThickness.pixelHeightEditBox.returnPressed.connect(self.updateSettings)

        self._settingsOperationBrush = SettingsGUIOpSegmentationBrush()
        #Listen to changes in the controls
        self._settingsOperationBrush.colorDropMenu.currentIndexChanged.connect(self.updateSettings)
        self._settingsOperationBrush.radiusEditBox.returnPressed.connect(self.updateSettings)



        self._settings.addTab(self._settingsOperationPerfilometer,"Perfilometer");
        self._settings.addTab(self._settingsOperationMeasureThickness,"Thickness Measurement");
        self._settings.addTab(self._settingsOperationBrush,"Brush");


        frameLayout = QVBoxLayout();
        frameLayout.addWidget(self._menuTools)
        frameLayout.addWidget(self._groupEditSegmentation)
        frameLayout.addWidget(self._settings)
        centralWidget = QWidget()
        centralWidget.setLayout(frameLayout)
        #self.setCentralWidget(centralWidget)
        self.setWidget(centralWidget)


        #self.setWindowTitle("OCTant App - Tools Menu")


        #  self.panelPrincipal.addWidget(self.tabs)

        #self.show()
        #self._menuTools.setVisible(True)
        #self._groupEditSegmentation.setEnable(False)
        #self._groupEditSegmentation.setVisible(True)

        return



#    #Properties getters/setters
#    #
#    # Remember: Sphinx ignores docstrings on property setters so all
#    #documentation for a property must be on the @property method
#    @property
#    def documentWindow(self): #documentWindow getter
#        """
#        The main window of OCTapp.
#
#        :getter: Gets the main app window.
#        :setter: Sets the main app window.
#        :type: class:`DocumentWindow`
#        """
#        return self.__documentWindow
#
#    @documentWindow.setter
#    def documentWindow(self,newDocWindow): #documentWindow setter
#        if newDocWindow is None:
##            warnMsg = self.getClassName() + ':documentWindow: Main documentWindow not found.'
##            warnings.warn(warnMsg,SyntaxWarning)
##            newDocWindow = DocumentWindow() #Initialize a documentWindow
#            self.__documentWindow = None #Can be used to clear connection
#        if (type(newDocWindow) is DocumentWindow):
#            self.__documentWindow = newDocWindow
#        else:
#            warnMsg = self.getClassName() + ':documentWindow: Unexpected documentWindow type.'
#            warnings.warn(warnMsg,SyntaxWarning)
#        return None



    #Public methods
    def getClassName(self):
        """Get the class name as a string.

        Get the class name as a string.

        :returns: The class name.
        :rtype: string
        """
        return type(self).__name__

    def connectDocumentWindow(self,theDocWindow):
        """Connects this tools window with the document main window.

        :returns: None
        """
        self.documentWindow = theDocWindow
        self._groupEditSegmentation.connectDocumentWindow(self.documentWindow)
        return


    def importFile(self):
        """Open an class:`octant:data.Document` on the main window to work on.

        :returns: None
        """
        tmp=self.parent().openFile()
        if tmp is not None:
            buttonList  = self._menuTools.children();
            for b in buttonList:
                b.setEnabled(True)
        self.parent().refresh()
        return



    def editSegmentation(self):
        """Starts/Stops manual segmentation step

        :returns: None
        """
        #If there is no current segmentation, generate a dummy one
        seg = octant.op.OpSegmentationEdit()
        theDoc = self.parent().document
        im = theDoc.getCurrentScan()
        imSegmented = theDoc.segmentation
        imSegmented = seg.initEditSegmentation(im,imSegmented) #This in turn
                                    #will call the ._generateDummySegmentation
                                    #if needed.

        theDoc.segmentation = imSegmented
        self.parent().document = theDoc
        self.parent().refresh()

        #Enable/Disable the edit segmentation tools
        buttonList  = self._menuTools.parentWidget().findChildren(QPushButton)
        for b in buttonList:
            if 'Start' in b.text():
                #Segmenting
                b.setText("Stop manual edit segmentation")
                #self._groupEditSegmentation.setVisible(True)
                self._groupEditSegmentation.setEnable(True)

            elif 'Stop' in b.text():
                b.setText("Start manual edit segmentation")
                #self._groupEditSegmentation.setVisible(False)
                self._groupEditSegmentation.setEnable(False)
        return

    def flatten(self):
        """Calls for flatenning operation to be executed.

        :returns: None
        """
        self.parent().flatten()
        return

    # def measureThickness(self):
    #     """Calls for measuring thickness operation to be executed.
    #
    #     :returns: None
    #     """
    #     if self.documentWindow is not None:
    #         self.documentWindow.measureThickness()
    #     return

    def segment(self):
        """Calls for segmentation operation to be executed.

        :returns: None
        """
        self.parent().segment()
        return


    def stitch(self):
        """Calls for stitching operation to be executed.

        :returns: None
        """
        self.parent().stitch()
        return

    def updateSettings(self):
        """Refreshes the document window following a parameter setting update.

        :returns: None
        """
        #Some of the settings may have change. Refresh the document window
        self.parent().refresh()
        return

#    def closeEvent(self,ev):
#        """Closes the main window.
#
#        :returns: None
#        """
#        #Capture the closing event
#        tmp = self.parent().close()
#        #self.close()
#        return
