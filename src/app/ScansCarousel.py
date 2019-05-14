# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 16:39:09 2019

File: ScansCarousel.py

Class ScansCarousel

The ScansCarousel class.

.. inheritance-diagram:: ScansCarousel


:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 31-Mar-2019 | FOE    | - Class created.                                     |
+-------------+--------+------------------------------------------------------+



.. seealso:: None
.. note:: None
.. todo:: Bug pending. Although loading of scans is correct but rendering
    of the thumbnails is not.

.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""

## Import
#import warnings
#import deprecation


from PyQt5.QtCore import Qt, QSize #Imports constants and basic elements
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem
from PyQt5.QtGui import QIcon, QPixmap, QImage

import numpy as np
#import cv2


from octant import __version__
import octant.data as octant

## Class definition
class ScansCarousel(QListWidget):
    #Sphinx documentation
    """A carousel for displaying the different :class:`octant.data.OCTscan`
    in an :class:`octant.data.OCTvolume`.

    It permits interactive selection of current scan.

    .. seealso:: None
    .. note:: None
    .. todo:: None

    """

    #Private class attributes shared by all instances

    #Class constructor
    def __init__(self):
        """ Class constructor. Creates an empty carousel.
        """
        #Call superclass constructor
        super(ScansCarousel, self).__init__()

        self.setViewMode(QListWidget.IconMode)
        self.setIconSize(QSize(200,200))
        self.setResizeMode(QListWidget.Adjust)

        self.octvolume = None

        return

    #Properties getters/setters
    #
    # Remember: Sphinx ignores docstrings on property setters so all
    #documentation for a property must be on the @property method
    @property
    def octvolume(self): #octvolume getter
        """
        The :class:`octant.data.OCTvolume` which scans are being carouselled.

        :getter: Gets the :class:`octant.data.OCTvolume`
        :setter: Sets the :class:`octant.data.OCTvolume`
        :type: :class:`octant.data.OCTvolume`
        """
        return self.__octvolume

    @octvolume.setter
    def octvolume(self,newVol): #octvolume setter
        if (type(newVol) is octant.OCTvolume) or (newVol is None):
            self.__octvolume = newVol
        else:
            warnMsg = self.getClassName() + ':octvolume: Unexpected document type.'
            warnings.warn(warnMsg,SyntaxWarning)
        self._resetScansList()
        return None

    #Private methods
    def _resetScansList(self):
        """Resets the scans list (i.e. the QListWidgetItems of the QListWidget)

        This function is to be called after the property :attr:`octvolume`\
        is set.
        """
        self.clear()
        scanList = None
        if self.octvolume is not None:
            scanList = self.octvolume.scans
        if scanList is not None:
            for scan in scanList:
                tmp = np.repeat(scan.data[:, :, np.newaxis], 3, axis=2)
                    #Conveniently convert Gray to RGB for correct visualization with QImage
                height, width, nChannels = tmp.shape
                bytesPerLine = 3 * width #Use 1 for gray images and 3 for RGB
                qimg = QImage(tmp.data,width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
                #qimg = QImage(tmp.data,width, height, bytesPerLine, QImage.Format_Indexed8)
                self.addItem(QListWidgetItem(QIcon(QPixmap.fromImage(qimg)),scan.scantype));
        return None


    #Public methods

    def getClassName(self):
        """Get the class name as a string.

        Get the class name as a string.

        :returns: The class name.
        :rtype: string
        """
        return type(self).__name__
