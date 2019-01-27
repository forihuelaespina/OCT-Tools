"""
-*- coding: utf-8 -*-

File: IOT_GUI_BrushParameterSettings.py

Class IOT_GUI_BrushParameterSettings

A frame (QGroupBox) for controlling the settings of the segmentation brush
(IOT_OperationBrush).

IOT stands for INAOE OCT Tools.

:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 20-Jan-2019 | FOE    | - Class created.                                     |
|             |        | - Added initial controls for perfilometer parameters |
|             |        | - Initial Sphinx documentation for the class         |
+-------------+--------+------------------------------------------------------+
| 12-Dec-2018 | FOE    | - Minor modifications to layout (relocating help     |
|             |        |   labels, etc)                                       |
+-------------+--------+------------------------------------------------------+

.. seealso:: None
.. note:: None
.. todo:: None

.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""


## Import
#import sys

from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QLineEdit, QComboBox, QLabel
from PyQt5.QtGui import QIntValidator

from matplotlib.backend_bases import KeyEvent, MouseEvent

from IOT_RetinalLayers import IOT_RetinalLayers
from IOT_OCTscanSegmentation import IOT_OCTscanSegmentation

## Class description
class IOT_GUI_BrushParameterSettings(QGroupBox):
    #Sphinx documentation
    """A GUI to control the parameters of the segmentation brush operation.
    
    A GUI to control the parameters of the segmentation brush operation.
    

    .. seealso:: None
    .. note:: None
    .. todo:: None
        
    """
    
    #Private class attributes shared by all instances

    #Class constructor
    def __init__(self):
        #Call superclass constructor
        QGroupBox.__init__(self)
        
        #Labels
        helpLabel = QLabel("Use mouse for brushing; click, maintain pressed and move.")
        colorLabel = QLabel("Retinal layer (a.k.a. brush color):")
        #columnHelpLabel = QLabel("Use -1 for global.")
        radiusLabel = QLabel("Brush radius [in pixels]:")
        
        #Controls
        r = IOT_RetinalLayers()
        items = r.getAllLayersNames()
        tmp=list()
        tmp.append("BACKGROUND")
        items = tmp + items #Concatenate both lists
        self.colorDropMenu = QComboBox()
        self.colorDropMenu.insertItems(0,items)
        self.colorDropMenu.setCurrentIndex(0) #default value
        
        self.radiusEditBox = QLineEdit()
        self.radiusEditBox.setValidator(QIntValidator(1,9999))
        self.radiusEditBox.setText("5") #default value
        
    
        #Add subgroups to the main group
        frameLayout = QVBoxLayout();
        frameLayout.addWidget(helpLabel);
        frameLayout.addWidget(colorLabel);
        #frameLayout.addWidget(columnHelpLabel);
        frameLayout.addWidget(self.colorDropMenu);
        frameLayout.addWidget(radiusLabel);
        frameLayout.addWidget(self.radiusEditBox);
        self.setLayout(frameLayout);
        
        #self.setEnable(False)
        self.setVisible(True)

        return
        

    def getColorValue(self):
        """ Retrieves the current value in the color drop down menu.
        
        Retrieves the current value in the color drop down menu.
        
        :returns: The color (retinal layer index) value.
        :rtype: integer
        
        """
        return int ( self.colorDropMenu.currentIndex() )

    def getRadiusValue(self):
        """ Retrieves the current value in the radius edit box.
        
        Retrieves the current value in the radius edit box.
        
        :returns: The radius value.
        :rtype: integer
        
        """
        return int ( self.radiusEditBox.text() )