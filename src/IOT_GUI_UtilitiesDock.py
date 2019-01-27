"""
-*- coding: utf-8 -*-

File: IOT_GUI_UtilitiesDock.py

Class IOT_GUI_UtilitiesDock

A dockable panel for tools and utilities. It provides a tabbed set of panels
for selecting scan within a volume or reporting layer thicknesses among others.

IOT stands for INAOE OCT Tools



:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 12-Dec-2018 | FOE    | - Class created.                                     |
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
from deprecated import deprecated

from PyQt5.QtCore import Qt #Imports constants
from PyQt5.QtWidgets import QDockWidget, QWidget, QGroupBox, QGridLayout, \
        QTabWidget, QLabel
#from PyQt5 import uic

from IOT_RetinalLayers import IOT_RetinalLayers


###################################################################################


#Class inherited from QDockWidget
class IOT_GUI_UtilitiesDock(QDockWidget):
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

        tmp = IOT_GUI_UtilitiesDock() - Creates a dockable panel for tools
        and utilities
                
        """
        #Call superclass constructor
        QDockWidget.__init__(self)

        self.docWindow = None

        self.setWindowTitle("OCT Tools App - Utilities dock")
        
        


        #Create the different utilities panels
        
        #Panel for scan selection within volume
        #
        # PENDING
        #

        #Panel for reporting layers thicknesses
        self._utilThickness = QGroupBox()
        
        tmp = IOT_RetinalLayers()
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
        
        #Create the tab widget and add the different utilities tabs
        self._utilities = QTabWidget()
        self._utilities.addTab(self._utilThickness,"Layer Thicknesses");

        #Add tabbed panel to main dock
        self.setWidget(self._utilities)
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
    
    def refresh(self):
        """Refreshes the thicknesses labels
        """
        self.layerThicknessesLabels = self.layerThicknesses
        self._utilThickness.update()
        return None
        