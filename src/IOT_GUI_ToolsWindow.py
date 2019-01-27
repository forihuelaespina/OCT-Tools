"""
-*- coding: utf-8 -*-

File: IOT_GUI_ToolsWindow.py

Class IOT_GUI_ToolsWindow

A panel for accessing tools

IOT stands for INAOE OCT Tools



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

.. seealso:: None
.. note:: None
.. todo:: None
   

.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Arlem Aleida Castillo Avila <acastillo@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""

## Import

#import sys

from PyQt5.QtWidgets import QMainWindow, QDockWidget, QWidget, QGroupBox, \
        QPushButton, QMenu, QAction, QVBoxLayout, QTabWidget
#from PyQt5 import uic

from IOT_GUI_DocumentWindow import IOT_GUI_DocumentWindow
from IOT_GUI_EditSegmentationTools import IOT_GUI_EditSegmentationTools
from IOT_GUI_PerfilometerParameterSettings import IOT_GUI_PerfilometerParameterSettings
from IOT_GUI_MeasureThicknessParameterSettings import IOT_GUI_MeasureThicknessParameterSettings
from IOT_GUI_BrushParameterSettings import IOT_GUI_BrushParameterSettings

from IOT_OperationEditSegmentation import IOT_OperationEditSegmentation





###################################################################################


#Class inherited from QMainWindow (Constructor de ventanas)
class IOT_GUI_ToolsWindow(QMainWindow):
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

        tmp = IOT_GUI_ToolsWindow() - Creates a panel of GUI controls for
        operating the OCTTools app.
                
        """
        #Call superclass constructor
        QMainWindow.__init__(self)
        #QDockWidget.__init__(self)

        self.docWindow = None
        
        #Cargar la configuración del archivo .ui en el objeto
        # uic.loadUi("GUI/IOT_GUI_ToolsWindow.ui", self)
        #     #The .ui resource file contains the menu and status bars
        self.move(50,50)
    
        #Initialize private attributes unique to this instance
        #self._menuTools = menuTools() #Buttons of actions sequence in the main window
        
        #Group main operations
        self._menuTools = QGroupBox()
        
        bOpenImage = QPushButton("Open Image")
        bOpenImage.clicked.connect(self.openDocument)
        bOpenImage.setEnabled(True)

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
        buttonPanelLayout.addWidget(bOpenImage);
        buttonPanelLayout.addWidget(bMosaicing);
        buttonPanelLayout.addWidget(bFlattening);
        buttonPanelLayout.addWidget(bSegment);
        buttonPanelLayout.addWidget(bEditSegment);
        #buttonPanelLayout.addWidget(bMeasureThickness);
        self._menuTools.setLayout(buttonPanelLayout);
        #self._menuTools.setVisible(True)

        
        #Menu
        mArchive = QMenu('Archive')

        actionOpen = QAction(mArchive)
        actionOpen.setObjectName('Open')
        actionOpen.setShortcut('Ctrl+O')
        actionOpen.setStatusTip('Open OCT image')
        actionOpen.triggered.connect(self.openDocument)
        
        actionExit = QAction(mArchive)
        actionOpen.setObjectName('Exit')
        actionExit.setStatusTip('Exit OCT-Tools application')
        actionExit.triggered.connect(self.closeEvent)

        mArchive.addAction(actionOpen)     
        mArchive.addSeparator()
        mArchive.addAction(actionExit)
        self.menuBar().addMenu(mArchive)
        
        #Edit segmentation panel
        self._groupEditSegmentation = IOT_GUI_EditSegmentationTools() #Edit segmentation tools panel
        

        #Tools settings panel
        self._settings = QTabWidget()

        self._settingsOperationPerfilometer = IOT_GUI_PerfilometerParameterSettings()
        #Listen to changes in the controls
        self._settingsOperationPerfilometer.columnEditBox.returnPressed.connect(self.updateSettings)
        self._settingsOperationPerfilometer.widthEditBox.returnPressed.connect(self.updateSettings)

        self._settingsOperationMeasureThickness = IOT_GUI_MeasureThicknessParameterSettings()
        #Listen to changes in the controls
        self._settingsOperationMeasureThickness.columnEditBox.returnPressed.connect(self.updateSettings)
        self._settingsOperationMeasureThickness.windowHalfWidthEditBox.returnPressed.connect(self.updateSettings)
        self._settingsOperationMeasureThickness.pixelWidthEditBox.returnPressed.connect(self.updateSettings)
        self._settingsOperationMeasureThickness.pixelHeightEditBox.returnPressed.connect(self.updateSettings)
        
        self._settingsOperationBrush = IOT_GUI_BrushParameterSettings()
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
        self.setCentralWidget(centralWidget)
        
        
        self.setWindowTitle("OCT Tools App - Tools Menu")
        
        
        #  self.panelPrincipal.addWidget(self.tabs)
    
        self.show()
        self._menuTools.setVisible(True)
        self._groupEditSegmentation.setEnable(False)
        self._groupEditSegmentation.setVisible(True)
        
        return
        


    #Properties getters/setters
    #
    # Remember: Sphinx ignores docstrings on property setters so all
    #documentation for a property must be on the @property method
    @property
    def documentWindow(self): #documentWindow getter
        """
        The main window of OCTapp.

        :getter: Gets the main app window.
        :setter: Sets the main app window.
        :type: class:`IOT_GUI_DocumentWindow`
        """
        return self.__documentWindow

    @documentWindow.setter
    def documentWindow(self,newDocWindow): #documentWindow setter
        if newDocWindow is None:
            warnMsg = self.getClassName() + ':documentWindow: Main documentWindow not found.'
            warnings.warn(warnMsg,SyntaxWarning)
            newDocWindow = IOT_GUI_DocumentWindow() #Initialize a documentWindow
        if (type(newDocWindow) is IOT_GUI_DocumentWindow):
            self.__documentWindow = newDocWindow
        else:
            warnMsg = self.getClassName() + ':documentWindow: Unexpected documentWindow type.'
            warnings.warn(warnMsg,SyntaxWarning)
        return None
       

        
    #Public methods
    def connectDocumentWindow(self,theDocWindow):
        """Connects this tools window with the document main window.
        
        :returns: None
        """
        self.documentWindow = theDocWindow
        self._groupEditSegmentation.connectDocumentWindow(self.documentWindow)
        return
    
    
    def openDocument(self):
        """Open an class:`IOT_Document` on the main window to work on.
        
        :returns: None
        """
        if self.documentWindow is not None:
            tmp=self.documentWindow.openDocument()
            if tmp is not None:
                buttonList  = self._menuTools.children();
                for b in buttonList:
                    b.setEnabled(True)
        self.documentWindow.refresh()
        return


     
    def editSegmentation(self):
        """Starts/Stops manual segmentation step
        
        :returns: None
        """
        if self.documentWindow is not None:
            #If there is no current segmentation, generate a dummy one
            seg = IOT_OperationEditSegmentation()
            theDoc = self.documentWindow.document
            im = theDoc.study
            imSegmented = theDoc.segmentation
            imSegmented = seg.initEditSegmentation(im,imSegmented) #This in turn
                                        #will call the ._generateDummySegmentation
                                        #if needed.

            theDoc.segmentation = imSegmented
            self.documentWindow.document = theDoc
            self.documentWindow.refresh()
               
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
        if self.documentWindow is not None:
            self.documentWindow.flatten()
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
        if self.documentWindow is not None:
            self.documentWindow.segment()
        return
        
        
    def stitch(self):
        """Calls for stitching operation to be executed.
        
        :returns: None
        """
        if self.documentWindow is not None:
            self.documentWindow.stitch()
        return

    def updateSettings(self):
        """Refreshes the document window following a parameter setting update.
        
        :returns: None
        """
        #Some of the settings may have change. Refresh the document window
        if self.documentWindow is not None:
            self.documentWindow.refresh()
        return

    def closeEvent(self,ev):
        """Closes the main window.
        
        :returns: None
        """
        #Capture the closing event 
        if self.documentWindow is not None:
            tmp = self.documentWindow.close()
            print(tmp)
        #self.close()
     
