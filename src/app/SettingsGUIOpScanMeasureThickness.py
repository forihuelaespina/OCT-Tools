"""
-*- coding: utf-8 -*-

File: SettingsGUIOpScanMeasureThickness.py

Class SettingsGUIOpScanMeasureThickness

A frame (QGroupBox) for controlling the settings of the layer thickness
measurement (class:`IOT_OperationMeasureLayerThickness`); namely; window
half width and pixel column, pixel width and pixel height.


:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 12-Dec-2018 | FOE    | - Class created.                                     |
|             |        | - Added initial controls for parameters              |
|             |        | - Initial Sphinx documentation for the class         |
+-------------+--------+------------------------------------------------------+
| 28-Feb-2019 | FOE    | - Adapted to new package OCTant structure.           |
|             |        |   Class rebranded SettingsGUIOpScanMeasureThickness. |
|             |        |   The prefix IOT__GUI is drop and the class is now   |
|             |        |   separated from the API.                            |
+-------------+--------+------------------------------------------------------+

.. seealso:: None
.. note:: None
.. todo:: None

.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""


## Import
#import sys

from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QLineEdit, QLabel
from PyQt5.QtGui import QIntValidator

from matplotlib.backend_bases import KeyEvent, MouseEvent



## Class description
class SettingsGUIOpScanMeasureThickness(QGroupBox):
    #Sphinx documentation
    """A GUI to control the parameters of the :class:`octant.op.OpScanMeasureLayerThickness`.
    
    A GUI to control the parameters of the :class:`octant.op.OpScanMeasureLayerThickness`.
    

    .. seealso:: :class:`SettingsGUIOpScanPerfilometer`
    .. note:: None
    .. todo:: None
        
    """
    
    #Private class attributes shared by all instances

    #Class constructor
    def __init__(self):
        #Call superclass constructor
        QGroupBox.__init__(self)
        
        #Labels
        helpLabel = QLabel("When finished, press ´´Enter´´ to update.")

        columnLabel = QLabel("Pixel column (Use -1 for global):")
        #columnHelpLabel = QLabel("Use -1 for global.")
        windowHalfWidthLabel = QLabel("Window half width [in pixels]:")
        pixelWidthLabel = QLabel("Pixel width [in microm]:")
        pixelHeightLabel = QLabel("Pixel height [in microm]:")
        #==All layers will be measured. No need for specific controls
        #layerIndexLabel = QLabel("Layer index:")
        #layerIndexHelpLabel = QLabel("Use -1 for all layers.")
        
        #Edit controls
        self.columnEditBox = QLineEdit() 
        self.columnEditBox.setValidator(QIntValidator(-1,9999))
        self.columnEditBox.setText("-1") #default value
        
        self.windowHalfWidthEditBox = QLineEdit()
        self.windowHalfWidthEditBox.setValidator(QIntValidator(1,9999))
        self.windowHalfWidthEditBox.setText("5") #default value
        
        self.pixelWidthEditBox = QLineEdit()
        self.pixelWidthEditBox.setValidator(QIntValidator(1,9999))
        self.pixelWidthEditBox.setText("10") #default value
        
        self.pixelHeightEditBox = QLineEdit()
        self.pixelHeightEditBox.setValidator(QIntValidator(1,9999))
        self.pixelHeightEditBox.setText("10") #default value
        
        #==All layers will be measured. No need for specific controls
        #self.layerIndexEditBox = QLineEdit()
        #self.layerIndexEditBox.setValidator(QIntValidator(1,9999))
        #self.layerIndexEditBox.setText("-1") #default value
        
    
        #Add subgroups to the main group
        frameLayout = QVBoxLayout();
        frameLayout.addWidget(helpLabel);
        frameLayout.addWidget(columnLabel);
        #frameLayout.addWidget(columnHelpLabel);
        frameLayout.addWidget(self.columnEditBox);
        frameLayout.addWidget(windowHalfWidthLabel);
        frameLayout.addWidget(self.windowHalfWidthEditBox);
        frameLayout.addWidget(pixelWidthLabel);
        frameLayout.addWidget(self.pixelWidthEditBox);
        frameLayout.addWidget(pixelHeightLabel);
        frameLayout.addWidget(self.pixelHeightEditBox);
        #==All layers will be measured. No need for specific controls
        #frameLayout.addWidget(layerIndexLabel);
        #frameLayout.addWidget(layerIndexHelpLabel);
        self.setLayout(frameLayout);
        
        #self.setEnable(False)
        self.setVisible(True)

        return
        

    def getPixelColumnValue(self):
        """ Retrieves the current value in the column edit box.
        
        Retrieves the current value in the column edit box.
        
        :returns: The pixel column value.
        :rtype: integer
        
        """
        return int ( self.columnEditBox.text() )

    def getWindowHalfWidthValue(self):
        """ Retrieves the current value in the window half width edit box.
        
        Retrieves the current value in the window half width edit box.
        
        :returns: The window half width value.
        :rtype: integer
        
        """
        return int ( self.windowHalfWidthEditBox.text() )

        
    def getPixelWidthValue(self):
        """ Retrieves the current value in the pixel width edit box.
        
        Retrieves the current value in the pixel width edit box.
        
        :returns: The pixel width column value.
        :rtype: integer
        
        """
        return int ( self.pixelWidthEditBox.text() )

        
        
    def getPixelHeightValue(self):
        """ Retrieves the current value in the pixel height edit box.
        
        Retrieves the current value in the pixel height edit box.
        
        :returns: The pixel height column value.
        :rtype: integer
        
        """
        return int ( self.pixelHeightEditBox.text() )

        