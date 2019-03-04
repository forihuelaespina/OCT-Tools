"""
-*- coding: utf-8 -*-

File: EditSegmentationToolsPanel.py

Class EditSegmentationToolsPanel

A frame (QGroupBox) for accessing the editing segmentation tools
(originally for operation in class:`octant.op.OpSegmentationEdit` but
later extended to other operations that work over
class:`octant.data.OCTscanSegmentation`)

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
| 20-Jan-2019 | FOE    | - Incorporated support for voxel based operations.   |
|             |        |   This currently supports class:`IOT_OperationBrush`.|
|             |        | - Improved Sphinx comments on methods.               |
+-------------+--------+------------------------------------------------------+
| 28-Feb-2019 | FOE    | - Adapted to new package OCTant structure.           |
|             |        |   Class rebranded DocumentWindow. The prefix IOT__GUI|
|             |        |   is drop and the class is now separated from the    |
|             |        |   API.                                               |
+-------------+--------+------------------------------------------------------+
|  3-Feb-2019 | FOE    | - Debugging of errors left during transition to new  |
|             |        |   package OCTant structure; wrong imports and        |
|             |        |   unupdated classes names.                           |
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

from matplotlib.backend_bases import KeyEvent, MouseEvent

from octant.data import RetinalLayers
from octant.op import OpSegmentationEdit


## Class description
class OpSegmentationEditToolsPanel(QGroupBox):
    #Sphinx documentation
    """A class:`QGroupBox` GUI for accesing operations over class:`IOT_OCTscanSegmentation`.
    
    A class:`QGroupBox` GUI for accesing operations over
    class:`octant.data.OCTscanSegmentation`. This includes operations executed by:
    
    * class:`octant.data.OpSegmentationEdit` - Note that this in turn represent
      several ROI and COI based operations.
    * class:`octant.op.OpSegmentationBrush`
    

    .. seealso:: None
    .. note:: None
    .. todo:: None
        
    """
    
 
    #Private class attributes shared by all instances

    #Class constructor
    def __init__(self):
        """The class constructor.

        The class constructor.
        
        tmp = OpSegmentationEditTools - Creates a default 
            class:`QGroupBox` GUI for accesing operations over class:`octant.data.OCTscanSegmentation`

        :param theOCTScan: The OCT scan to be segmented
        :type img: :class:`octant.data.OCTscan`
        
        """
        #Call superclass constructor
        QGroupBox.__init__(self)
        
        
        self._docWindow = None
        self._lastEvent = None #To temporally store mouse events

        self._seg = OpSegmentationEdit()
        
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


        #Group for Voxel (VOI) based manipulation operations
        VOIframe = QGroupBox("VOI based manipulation")

        bVOIBrush = QPushButton("Brush")
        bVOIBrush.clicked.connect(self.opVOIBrush)
        bVOIBrush.setEnabled(True)

        VOIframeLayout = QVBoxLayout();
        VOIframeLayout.addWidget(bVOIBrush);
        VOIframe.setLayout(VOIframeLayout);

        self._buttonList.append(bVOIBrush)


        #Add subgroups to the main group
        frameLayout = QVBoxLayout();
        frameLayout.addWidget(COIframe);
        frameLayout.addWidget(ROIframe);
        frameLayout.addWidget(VOIframe);
        self.setLayout(frameLayout);
        
        
        
        
        self.setEnable(False)
        self.setVisible(True)
        
        return


    #Public methods
    def getClassName(self):
        """Get the class name as a string.

        Get the class name as a string.

        :returns: The class name.
        :rtype: string
        """
        return type(self).__name__

    def connectDocumentWindow(self,theDocWindow):
        """Connects this GUI to a main document window class:`DocumentWindow`.

        Connects this GUI to a main document window class:`DocumentWindow`.

        :returns: None
        """
        self._docWindow = theDocWindow
        return None
    
    
    

    def opCOIDelete(self):
        """Calls for the execution of a class:`octant.op.OpSegmentationEdit` COI deletion operation

        Calls for the execution of a class:`octant.op.OpSegmentationEdit` COI deletion operation

        :returns: None
        """
        #Get parameters
        r = RetinalLayers()
        items = r.getAllLayersNames()
        lName, flagOKPressed = QInputDialog.getItem(self, "Input parameter", "Layer name:", items, 0, False)
        if flagOKPressed:
            params=list()
            params.append(r.getLayerIndex(lName))
            #...and simply pass the command.
            self._docWindow.opEditSegmentation('COIDelete',params)
        return None

    def opCOIChangeLabel(self):
        """Calls for the execution of a class:`octant.op.OpSegmentationEdit` COI change label operation

        Calls for the execution of a class:`octant.op.OpSegmentationEdit` COI change label operation

        :returns: None
        """
        #Get parameters
        r = octant.RetinalLayers()
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
            
        return None



    def opROIDelete(self):
        """Calls for the execution of a class:`IOT_OperationEditSegmentation` ROI deletion operation

        Calls for the execution of a class:`IOT_OperationEditSegmentation` ROI deletion operation

        :returns: None
        """
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
        return None

    def opROIChangeLabel(self):
        """Calls for the execution of a class:`IOT_OperationEditSegmentation` ROI change label operation

        Calls for the execution of a class:`IOT_OperationEditSegmentation` ROI change label operation

        :returns: None
        """
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
            r = RetinalLayers()
            items = r.getAllLayersNames()
            lName, flagOKPressed = QInputDialog.getItem(self, "Input parameter", "New layer name:", items, 0, False)

        if flagOKPressed:
            params=list()
            params.append(r.getLayerIndex(lName))
            params.append(mousePos)
            #...and simply pass the command
            self._docWindow.opEditSegmentation('ROIChangeLabel',params)
        return None


    def opVOIBrush(self):
        """Calls for the execution of a class:`octant.op.OpSegmentationBrush` operation

        Calls for the execution of a class:`octant.op.OpSegmentationBrush` operation

        :returns: None
        """
        if self._docWindow is not None:
            self._docWindow.brush()
        return None

    def setEnable(self,b):
        """Enables buttons in the GUI.
        
        Enables buttons in the GUI

        :returns: None
        """
        for theButton in self._buttonList:
            theButton.setEnabled(b)
        return None

