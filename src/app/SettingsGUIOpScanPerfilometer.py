"""
-*- coding: utf-8 -*-

File: SettingsGUIOpScanPerfilometer.py

Class SettingsGUIOpScanPerfilometer

.. inheritance-diagram:: SettingsGUIOpScanPerfilometer

A frame (QGroupBox) for controlling the settings of the perfilometer
(IOT_OperationFlattening); namely window width and pixel column.


:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 14-Nov-2018 | FOE    | - Class created.                                     |
|             |        | - Added initial controls for perfilometer parameters |
|             |        | - Initial Sphinx documentation for the class         |
+-------------+--------+------------------------------------------------------+
| 12-Dec-2018 | FOE    | - Minor modifications to layout (relocating help     |
|             |        |   labels, etc)                                       |
+-------------+--------+------------------------------------------------------+
| 28-Feb-2019 | FOE    | - Adapted to new package OCTant structure.           |
|             |        |   Class rebranded SettingsGUIOpScanPerfilometer.     |
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
class SettingsGUIOpScanPerfilometer(QGroupBox):
    #Sphinx documentation
    """A GUI to control the parameters of the perfilometer operation.

    A GUI to control the parameters of the perfilometer operation.


    .. seealso:: :class:`SettingGUIOpScanMeasureThickness`
    .. note:: None
    .. todo:: None

    """

    #Private class attributes shared by all instances

    #Class constructor
    def __init__(self):
        #Call superclass constructor
        QGroupBox.__init__(self)

        #Labels
        helpLabel = QLabel("Press ´´Enter´´ to update.")
        columnLabel = QLabel("Pixel column (Use -1 for global):")
        #columnHelpLabel = QLabel("Use -1 for global.")
        widthLabel = QLabel("Window half width [in pixels]:")

        #Edit controls
        self.columnEditBox = QLineEdit()
        self.columnEditBox.setValidator(QIntValidator(-1,9999))
        self.columnEditBox.setText("-1") #default value

        self.widthEditBox = QLineEdit()
        self.widthEditBox.setValidator(QIntValidator(1,9999))
        self.widthEditBox.setText("5") #default value


        #Add subgroups to the main group
        frameLayout = QVBoxLayout();
        frameLayout.addWidget(helpLabel);
        frameLayout.addWidget(columnLabel);
        #frameLayout.addWidget(columnHelpLabel);
        frameLayout.addWidget(self.columnEditBox);
        frameLayout.addWidget(widthLabel);
        frameLayout.addWidget(self.widthEditBox);
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

    def getWidthValue(self):
        """ Retrieves the current value in the width edit box.

        Retrieves the current value in the width edit box.

        :returns: The pixel width value.
        :rtype: integer

        """
        return int ( self.widthEditBox.text() )
