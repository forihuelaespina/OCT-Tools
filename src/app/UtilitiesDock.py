"""
-*- coding: utf-8 -*-

File: IOT_GUI_UtilitiesDock.py

Class IOT_GUI_UtilitiesDock

.. inheritance-diagram:: UtilitiesDock

A dockable panel for tools and utilities. It provides a tabbed set of panels
for selecting scan within a volume or reporting layer thicknesses among others.

IOT stands for INAOE OCT Tools



:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 12-Dec-2018 | FOE    | - Class created.                                     |
+-------------+--------+------------------------------------------------------+
| 24-Feb-2019 | FOE    | - Updated deprecation package to "deprecation" due   |
|             |        |   compilation problems with package "deprecated".    |
+-------------+--------+------------------------------------------------------+
|  3-Mar-2018 | FOE    | - Solved circular importing with DocumentWindow.     |
+-------------+--------+------------------------------------------------------+
| 31-Mar-2018 | FOE    | - Added tab and property for holding the scans       |
|             |        |   carousel.                                          |
+-------------+--------+------------------------------------------------------+

.. seealso:: None
.. note:: None
.. todo:: None


.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""

## Import

#import sys

import warnings
#import deprecation

from PyQt5.QtCore import Qt #Imports constants
from PyQt5.QtWidgets import QDockWidget, QWidget, QGroupBox, QGridLayout, \
        QTabWidget, QLabel
#from PyQt5 import uic

#from DocumentWindow import DocumentWindow
#import DocumentWindow #Use this formula to avoid circular importing clash
from ScansCarousel import ScansCarousel
from octant.data import RetinalLayers


###################################################################################


#Class inherited from QDockWidget
class UtilitiesDock(QDockWidget):
    #Sphinx documentation
    """A dockable panel for tools and utilities.

    A dockable panel for tools and utilities.


    .. seealso:: None
    .. note:: None
    .. todo:: None

    """
    #Private class attributes shared by all instances

    #Class constructor
    def __init__(self):
        """The class constructor.

        The class constructor.

        tmp = UtilitiesDock() - Creates a dockable panel for tools
        and utilities

        """
        #Call superclass constructor
        QDockWidget.__init__(self)

        #self.documentWindow = None

        self.setWindowTitle("OCTantApp - Utilities dock")

        #Create the different utilities panels

        #Panel for scan selection within volume
        #
        # PENDING
        #

        #Tab for reporting layers thicknesses
        self._utilThickness = QGroupBox()

        tmp = RetinalLayers()
        layers = tmp.getAllLayersIndexes()

        tabLayout = QGridLayout();
        tmpThicknesses = list()
        layerNamesLabels = list()
        thicknessValuesLabels = list()
        pos=1
        for elem in layers:
            tmpThicknesses.append(0)
            #Create labels for each layer and add them to the layout
            layerNamesLabels.append(QLabel(tmp.getLayerName(elem) + ":"))
            tabLayout.addWidget(layerNamesLabels[-1],pos,1,Qt.AlignRight);
            thicknessValuesLabels.append(QLabel(str(tmpThicknesses[-1])))
            tabLayout.addWidget(thicknessValuesLabels[-1],pos,3,Qt.AlignLeft);
            pos=pos+1
        self.layerThicknesses = tmpThicknesses
        self.__layerThicknessesLabels = [QLabel("0") for x in range(len(layers))] #Just a trick. Do not remove!
        self.layerThicknessesLabels = thicknessValuesLabels
        self._utilThickness.setLayout(tabLayout)

        #Tab with the scans carousel
        self.scanscarousel = ScansCarousel()

        #Create the tab widget and add the different utilities tabs
        self._utilities = QTabWidget()
        self._utilities.addTab(self._utilThickness,"Layer Thicknesses");
        self._utilities.addTab(self.scanscarousel,"Scans Carousel");

        #Add tabbed panel to main dock
        self.setWidget(self._utilities)
        return

    #Properties getters/setters
    #
    # Remember: Sphinx ignores docstrings on property setters so all
    #documentation for a property must be on the @property method
#    @property
#    def documentWindow(self): #documentWindow getter
#        """
#        The main window of OCTant.
#
#        :getter: Gets the main app window.
#        :setter: Sets the main app window.
#        :type: class:`DocumentWindow`
#        """
#        return self.__documentWindow
#
#    @documentWindow.setter
#    def documentWindow(self,newDocWindow): #documentWindow setter
#        print(newDocWindow)
#        if newDocWindow is None:
##            warnMsg = self.getClassName() + ':documentWindow: Main documentWindow not found.'
##            warnings.warn(warnMsg,SyntaxWarning)
##            newDocWindow = DocumentWindow() #Initialize a documentWindow
#            self.__documentWindow = None; #Can be used to clear connection
#        if (type(newDocWindow) is DocumentWindow):
#            self.__documentWindow = newDocWindow
#        else:
#            warnMsg = self.getClassName() + ':documentWindow: ' \
#                        + 'Unexpected type ' + str(type(newDocWindow)) + '.'
#            warnings.warn(warnMsg,SyntaxWarning)
#        return None

    @property
    def scanscarousel(self): #scanscarousel getter
        """
        The scans carousel.

        :getter: Gets the scans carousel
        :setter: Sets the scans carousel
        :type: :class:`octant.app.ScansCarousel`
        """
        return self.__scanscarousel

    @scanscarousel.setter
    def scanscarousel(self,newCarousel): #scanscarousel setter
        if (newCarousel is None):
            #Initialize to empty
            self.__scanscarousel = ScansCarousel()
        elif (type(newCarousel) is ScansCarousel):
            self.__scanscarousel = newCarousel
        else:
            warnMsg = self.getClassName() + ':scanscarousel: Unexpected document type.'
            warnings.warn(warnMsg,SyntaxWarning)
        return None


    @property
    def layerThicknesses(self): #layerThicknesses getter
        """
        The layers thicknesses to be rendered.

        :getter: Gets the layers thicknesses to be rendered.
        :setter: Sets the layers thicknesses to be rendered.
        :type: list thickness values
        """
        return self.__layerThicknesses

    @layerThicknesses.setter
    def layerThicknesses(self,newThicknesses): #layerThicknesses setter
        self.__layerThicknesses = newThicknesses
        return None


    @property
    def layerThicknessesLabels(self): #layerThicknessesLabels getter
        """
        The labels (or rather the text on them) for rendering layers thicknesses.

        :getter: Gets the labels for rendering layers thicknesses.
        :setter: Sets the labels for rendering layers thicknesses.
        :type: list label texts for rending thicknesses
        """
        #Note that internally the Qlabels are stored
        tmp = list()
        for elem in self.__layerThicknessesLabels:
            tmp.append(elem.text)
        return tmp

    @layerThicknessesLabels.setter
    def layerThicknessesLabels(self,labelsNewText): #layerThicknessesLabels setter
        pos = 0;
        for elem in labelsNewText:
            #theLabel = self.__layerThicknessesLabels[pos]
            if type(elem) is str:
                self.__layerThicknessesLabels[pos].setText(labelsNewText[pos])
            elif type(elem) is QLabel:
                self.__layerThicknessesLabels[pos] = labelsNewText[pos]
            else:
                self.__layerThicknessesLabels[pos].setText(str(labelsNewText[pos]))
            pos=pos+1
        return None

    #Public methods

    def getClassName(self):
        """Get the class name as a string.

        Get the class name as a string.

        :returns: The class name.
        :rtype: string
        """
        return type(self).__name__


    def refresh(self):
        """Refreshes the thicknesses labels
        """
        self.layerThicknessesLabels = self.layerThicknesses
        self._utilThickness.update()
        return None
