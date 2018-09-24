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

.. seealso:: None
.. note:: None
.. todo:: None
   

.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Arlem Aleida Castillo Avila <acastillo@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""

## Import

#import sys

from PyQt5.QtWidgets import QMainWindow, QDockWidget, QWidget, QGroupBox, QPushButton, QMenu, QAction, QVBoxLayout
#from PyQt5 import uic

from IOT_GUI_DocumentWindow import IOT_GUI_DocumentWindow
from IOT_GUI_EditSegmentationTools import IOT_GUI_EditSegmentationTools

from IOT_OperationEditSegmentation import IOT_OperationEditSegmentation





###################################################################################


#Clase heredada de QMainWindow (Constructor de ventanas)
class IOT_GUI_ToolsWindow(QMainWindow):
    #Sphinx documentation
    """A panel for accessing tools.
    
    A panel for accessing tools.
    
    
    .. seealso:: 
    .. note:: 
    .. todo:: 
        
    """
    
 
    #Private class attributes shared by all instances

    #Class constructor
    def __init__(self):
        #Call superclass constructor
        QMainWindow.__init__(self)
        #QDockWidget.__init__(self)

        self._docWindow = None
        
        #Cargar la configuración del archivo .ui en el objeto
        # uic.loadUi("GUI/IOT_GUI_ToolsWindow.ui", self)
        #     #The .ui resource file contains the menu and status bars
        self.move(50,50)
    
        #Initialize private attributes unique to this instance
        #self._menuTools = menuTools() #Buttons of actions sequence in the main window
        
        #Group main operations
        self._menuTools = QGroupBox()
        
        bOpenImage = QPushButton("Open Image")
        bOpenImage.clicked.connect(self.abrir)
        bOpenImage.setEnabled(True)

        bMosaicing = QPushButton("Mosaicing")
        bMosaicing.clicked.connect(self.stitching)
        bMosaicing.setEnabled(False)
        
        bFlattening = QPushButton("Flattening")
        bFlattening.clicked.connect(self.rectificar)
        bFlattening.setEnabled(False)
        
        bSegment = QPushButton("Automatic segmentation")
        bSegment.clicked.connect(self.segmentar)
        bSegment.setEnabled(False)
        
        bEditSegment = QPushButton("Start edit segmentation")
        bEditSegment.clicked.connect(self.editSegmentar)
        bEditSegment.setEnabled(False)
        
        buttonPanelLayout = QVBoxLayout();
        buttonPanelLayout.addWidget(bOpenImage);
        buttonPanelLayout.addWidget(bMosaicing);
        buttonPanelLayout.addWidget(bFlattening);
        buttonPanelLayout.addWidget(bSegment);
        buttonPanelLayout.addWidget(bEditSegment);
        self._menuTools.setLayout(buttonPanelLayout);
        #self._menuTools.setVisible(True)

        
        #Menu
        mArchive = QMenu('Archive')

        actionOpen = QAction(mArchive)
        actionOpen.setObjectName('Open')
        actionOpen.setShortcut('Ctrl+O')
        actionOpen.setStatusTip('Open OCT image')
        actionOpen.triggered.connect(self.abrir)
        
        actionExit = QAction(mArchive)
        actionOpen.setObjectName('Exit')
        actionExit.setStatusTip('Exit OCT-Tools application')
        actionExit.triggered.connect(self.closeEvent)

        mArchive.addAction(actionOpen)     
        mArchive.addSeparator()
        mArchive.addAction(actionExit)
        self.menuBar().addMenu(mArchive)
        
        
        #self.actionNuevo.setShortcut('Ctrl+a')
        #self.actionAbrir.setShortcut('Ctrl+o')
        #self.actionSalir.triggered.connect(self.close)
        
        #self.actionAbrir.triggered.connect(self.abrir)
        #self.actionSalir.triggered.connect(self.closeEvent)
        
        
        
        #Edit segmentation panel
        self._groupEditSegmentation = IOT_GUI_EditSegmentationTools() #Edit segmentation tools panel
        
        frameLayout = QVBoxLayout();
        frameLayout.addWidget(self._menuTools) 
        frameLayout.addWidget(self._groupEditSegmentation)
        centralWidget = QWidget()
        centralWidget.setLayout(frameLayout)
        self.setCentralWidget(centralWidget)
        
        #  self.panelPrincipal.addWidget(self.tabs)
    
        self.show()
        self._menuTools.setVisible(True)
        self._groupEditSegmentation.setEnable(False)
        self._groupEditSegmentation.setVisible(True)
        
        return
        


        
    #Public methods
    def connectDocumentWindow(self,theDocWindow):
        self._docWindow = theDocWindow
        self._groupEditSegmentation.connectDocumentWindow(self._docWindow)
    
    
    def abrir(self):
        #Open an OCT image to work on.
        if self._docWindow is not None:
            tmp=self._docWindow.abrir()
            if tmp is not None:
                buttonList  = self._menuTools.children();
                for b in buttonList:
                    b.setEnabled(True)
        return


     
    def editSegmentar(self):
        #Starts/Stops manual segmentation step
        if self._docWindow is not None:
            #If there is no current segmentation, generate a dummy one
            seg = IOT_OperationEditSegmentation()
            theDoc = self._docWindow.getDocument()
            im = theDoc.getStudy()
            imSegmented = theDoc.getScanSegmentation()
            imSegmented = seg.initEditSegmentation(im,imSegmented) #This in turn
                                        #will call the ._generateDummySegmentation
                                        #if needed.
            theDoc.setScanSegmentation(imSegmented)
            self._docWindow.setDocument(theDoc)
               
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
  
    def rectificar(self):
        #Flattens cureent study
        if self._docWindow is not None:
            self._docWindow.rectificar()
        return
        
    def segmentar(self):
        #Applies the segmentation step
        if self._docWindow is not None:
            self._docWindow.segmentar()
        return
        
        
    def stitching(self):
        #Selects a second image and applies the stitching step
        if self._docWindow is not None:
            self._docWindow.stitching()
        return



    def closeEvent(self,ev):
    #Capture the closing event 
        if self._docWindow is not None:
            tmp = self._docWindow.close()
            print(tmp)
        #self.close()
     
