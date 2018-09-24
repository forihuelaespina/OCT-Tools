"""
-*- coding: utf-8 -*-

File: IOT_GUI_EditSegmentationTools.py

Class IOT_GUI_EditSegmentationTools

A frame (QGroupBox) for accessing the editing segmentation tools (IOT_OperationEditSegmentation)

IOT stands for INAOE OCT Tools

:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 27-Aug-2018 | FOE    | - Class created.                                     |
|             |        | - Added initial groups for COI and ROI based         |
|             |        |   manipulations.                                     |
|             |        | - Added buttons for initial operations; Delete and   |
|             |        |   ChangeLabel                                        |
+-------------+--------+------------------------------------------------------+
| 30-Aug-2018 | FOE    | - Incorporated buttons other editing operations.     |
+-------------+--------+------------------------------------------------------+
| 23-Sep-2018 | FOE    | - Updated comments and added Sphinx documentation to |
|             |        |   the class                                          |
+-------------+--------+------------------------------------------------------+

.. seealso:: None
.. note:: None
.. todo:: None

.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""


## Import
#import sys

from PyQt5.QtWidgets import QGroupBox, QPushButton, QVBoxLayout, QInputDialog, QMessageBox

from IOT_OperationEditSegmentation import IOT_OperationEditSegmentation
from IOT_RetinalLayers import IOT_RetinalLayers

from matplotlib.backend_bases import KeyEvent, MouseEvent



## Class description
class IOT_GUI_EditSegmentationTools(QGroupBox):
    #Sphinx documentation
    """A base class for operations on IOT_OCTvolumes and IOT_OCTscans.
    
    A base class for operations on IOT_OCTvolumes and IOT_OCTscans.
    

    .. seealso:: IOT_OperationEditSegmentation
    .. note:: 
    .. todo:: 
        
    """
    
 
    #Private class attributes shared by all instances

    #Class constructor
    def __init__(self):
        #Call superclass constructor
        QGroupBox.__init__(self)
        
        
        self._docWindow = None
        self._lastEvent = None #To temporally store mouse events

        self._seg = IOT_OperationEditSegmentation()
        
        self._buttonList = list()
        
        #Group for COI based manipulation operations
        COIframe = QGroupBox("COI based manipulation")
        
        bCOIDelete = QPushButton("Delete")
        bCOIDelete.clicked.connect(self.opCOIDelete)
        bCOIDelete.setEnabled(True)

        bCOIChangeLabel = QPushButton("Change Label")
        bCOIChangeLabel.clicked.connect(self.opCOIChangeLabel)
        bCOIChangeLabel.setEnabled(True)

        COIframeLayout = QVBoxLayout();
        COIframeLayout.addWidget(bCOIDelete);
        COIframeLayout.addWidget(bCOIChangeLabel);
        COIframe.setLayout(COIframeLayout);

        self._buttonList.append(bCOIDelete)
        self._buttonList.append(bCOIChangeLabel)

        #Group for ROI based manipulation operations
        ROIframe = QGroupBox("ROI based manipulation")
        
        bROIDelete = QPushButton("Delete")
        bROIDelete.clicked.connect(self.opROIDelete)
        bROIDelete.setEnabled(True)

        bROIChangeLabel = QPushButton("Change Label")
        bROIChangeLabel.clicked.connect(self.opROIChangeLabel)
        bROIChangeLabel.setEnabled(True)
        
        ROIframeLayout = QVBoxLayout();
        ROIframeLayout.addWidget(bROIDelete);
        ROIframeLayout.addWidget(bROIChangeLabel);
        ROIframe.setLayout(ROIframeLayout);
        
        self._buttonList.append(bROIDelete)
        self._buttonList.append(bROIChangeLabel)

        #Add subgroups to the main group
        frameLayout = QVBoxLayout();
        frameLayout.addWidget(COIframe);
        frameLayout.addWidget(ROIframe);
        self.setLayout(frameLayout);
        
        
        
        
        self.setEnable(False)
        self.setVisible(True)
        
        return


    #Public methods
    def getClassName(self):
        return type(self).__name__

    def connectDocumentWindow(self,theDocWindow):
        self._docWindow = theDocWindow
    
    
    

    def opCOIDelete(self):
    #Execute a COI deletion operation
        #Get parameters
        r = IOT_RetinalLayers()
        items = r.getAllLayersNames()
        lName, flagOKPressed = QInputDialog.getItem(self, "Input parameter", "Layer name:", items, 0, False)
        if flagOKPressed:
            params=list()
            params.append(r.getLayerIndex(lName))
            #...and simply pass the command.
            self._docWindow.opEditSegmentation('COIDelete',params)
        return

    def opCOIChangeLabel(self):
    #Execute a COI deletion operation
        #Get parameters
        r = IOT_RetinalLayers()
        items = r.getAllLayersNames()
        lName, flagOKPressed = QInputDialog.getItem(self, "Input parameter", "Layer name:", items, 0, False)
        if flagOKPressed:
            newLName, flagOKPressed = QInputDialog.getItem(self, "Input parameter", "New layer name:", items, 0, False)

        if flagOKPressed:
            params=list()
            params.append(r.getLayerIndex(newLName))
            params.append(r.getLayerIndex(lName))
    
            #...and simply pass the command.
            self._docWindow.opEditSegmentation('COIChangeLabel',params)
            
        return



    def opROIDelete(self):
    #Execute a ROI deletion operation
        #Get parameters
        #Select ROI
        tmp=QMessageBox(QMessageBox.Information,"Select ROI","Please click on figure to select ROI.")
        tmp.exec_()
        print(self.getClassName(),": opROIDelete: Please click to select ROI.")
        mEvent = self._docWindow.waitForMouseButtonPress()
        #print(mEvent)
        try:
            mousePos = (int(mEvent.x), int(mEvent.y))
            mouseCoords = (mEvent.xdata, mEvent.ydata)
        except:
            mousePos = (0,0)
            mouseCoords = (mEvent.xdata, mEvent.ydata)
        mouseButton = mEvent.button 
        
        params=list()
        params.append(mousePos)
        
        #...and simply pass the command.
        self._docWindow.opEditSegmentation('ROIDelete',params)
        return

    def opROIChangeLabel(self):
    #Execute a ROI deletion operation
        #Get parameters
        #Select ROI
        tmp=QMessageBox(QMessageBox.Information,"Select ROI","Please click on figure to select ROI.")
        tmp.exec_()
        print(self.getClassName(),": opROIChangeLabel: Please click to select ROI.")
        mEvent = self._docWindow.waitForMouseButtonPress()
        #print(mEvent)
        try:
            mousePos = (int(mEvent.x), int(mEvent.y))
            mouseCoords = (mEvent.xdata, mEvent.ydata)
        except:
            mousePos = (0,0)
            mouseCoords = (mEvent.xdata, mEvent.ydata)
        mouseButton = mEvent.button 
       
        #Select new layer
        flagOKPressed = True
        if flagOKPressed:
            r = IOT_RetinalLayers()
            items = r.getAllLayersNames()
            lName, flagOKPressed = QInputDialog.getItem(self, "Input parameter", "New layer name:", items, 0, False)

        if flagOKPressed:
            params=list()
            params.append(r.getLayerIndex(lName))
            params.append(mousePos)
            #...and simply pass the command
            self._docWindow.opEditSegmentation('ROIChangeLabel',params)
        return


    def setEnable(self,b):
        for theButton in self._buttonList:
            theButton.setEnabled(b)
        return

