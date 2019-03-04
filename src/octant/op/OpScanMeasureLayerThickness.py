"""
-*- coding: utf-8 -*-

File: OpMeasureLayerThickness.py

Class OpMeasureLayerThickness

A class for measuring class:`octant.data.RetinalLayers` thicknesses on
class:`octant.data.OCTscanSegmentation`.


:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 4-Aug-2018  | FOE    | - Isolated minimal solution.                         |
|             |        | - Encapsulated in class.                             |
+-------------+--------+------------------------------------------------------+
| 21-Aug-2018 | FOE    | - Enhanced measurement.                              |
+-------------+--------+------------------------------------------------------+
| 22-Aug-2018 | FOE    | - Rebranded to capital "O" in operation;             |
|             |        |   IOT_Operation                                      |
|             |        | - Improved verbosity; now using class name           |
+-------------+--------+------------------------------------------------------+
| 26-Aug-2018 | FOE    | - Retinal layers are now referenced from class       |
|             |        |   RetinalLayers.                                     |
+-------------+--------+------------------------------------------------------+
| 23-Sep-2018 | FOE    | - Updated comments and added Sphinx                  |
|             |        |   documentation to the class                         |
+-------------+--------+------------------------------------------------------+
|  2-Dec-2018 | FOE    | - Adapted to IOT_Operation becoming abstract and new |
|             |        |   capabilities. Added method .execute, integration of|
|             |        |   operands, given operation name, deprecated method  |
|             |        |   perfilometry.                                      |
|             |        | - Operation meta-parameters are now encapsulated as  |
|             |        |   properties.                                        |
|             |        | - Improved methods documentation.                    |
|             |        | - Improved measuring algorithm                       |
+-------------+--------+------------------------------------------------------+
| 12-Dec-2018 | FOE    | - Deprecated property layerIndex.                    |
|             |        | - New property layers                                |
|             |        | - More than one layer can now be measured at once.   |
+-------------+--------+------------------------------------------------------+
| 13-Dec-2018 | FOE    | - Updated deprecation package to "deprecation" due   |
|             |        |   compilation problems with package "deprecated".    |
+-------------+--------+------------------------------------------------------+
| 27-Feb-2019 | FOE    | - Adapted to new package OCTant structure.           |
|             |        |   Class rebranded Operation. The prefix              |
|             |        |   IOT is drop and it is now part of the package.     |
|             |        |   Also, the subprefix Operation is reduced to Op     |
|             |        |   only, the class name extended with the main        |
|             |        |   operand type.                                      |
|             |        | - Importing statements for classes within this       |
|             |        |   package are now made through package instead       |
|             |        |   of one class at time.                              |
|             |        | - Previously deprecated property layerIndex and      |
|             |        |   method getLayerThickness have now been fully       |
|             |        |   removed.                                           |
+-------------+--------+------------------------------------------------------+
|  3-Feb-2019 | FOE    | - Debugging of errors left during transition to new  |
|             |        |   package OCTant structure; wrong imports and        |
|             |        |   unupdated classes names.                           |
+-------------+--------+------------------------------------------------------+


.. seealso:: None
.. note:: None
.. todo:: None


.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Arlem Aleida Castillo Avila <acastillo@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""

## Import
import warnings
#from deprecated import deprecated
import deprecation

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage import io, color

#from version import __version__
from octant.data import OCTscanSegmentation, RetinalLayers
from .Operation import Operation



## Class definition
class OpScanMeasureLayerThickness(Operation):
    #Sphinx documentation
    """A class for measuring layer thicknesses on OCT segmentations.

    This class estimates the thickness of layers from a segmented OCT image.

    .. seealso:: None
    .. note:: None
    .. todo:: None

    """
    #Private class attributes shared by all instances

    #Class constructor
    def __init__(self):
        """The class constructor.

        The class constructor.

        tmp = OpMeasureLayerThickness() - Creates an empty MeasureLayerThickness operation
        
        """
        #Call superclass constructor
        super().__init__()

        #Initialize private attributes unique to this instance

        #Set the operation name
        self.name = "MeasureLayerThickness"
     
        self.pixelWidth = 1; #Pixel width in [mm]
        self.pixelHeight = 1; #Pixel height in [mm]
        #self.layerIndex = -1; #Retinal layer index
        self.layers = RetinalLayers().getAllLayersIndexes();
            #Retinal layers to be measured. By default, ALL layers are chosen.
        
        self.pixelColumn = -1 #Where to measure
        self.windowHalfWidth = 0 #Width of measuring window
        
        return




    #Properties getters/setters
    #
    # Remember: Sphinx ignores docstrings on property setters so all
    #documentation for a property must be on the @property method
    @property
    def pixelWidth(self): #pixelWidth getter
        """
        Pixel width in [mm].

        :getter: Gets the pixel width.
        :setter: Sets the pixel width.
        :type: double
        """
        return self.__pixelWidth

    @pixelWidth.setter
    def pixelWidth(self,w): #pixelWidth setter
        if (w<=0):
            warnMsg = self.getClassName() \
                        + ':pixelWidth: Width must be bigger than 0 [mm]. ' \
                        + 'Value ' + str(w) + ' will be ignored.'
            warnings.warn(warnMsg,SyntaxWarning)
        else:
            self.__pixelWidth = w;
        return None

    @property
    def pixelHeight(self): #pixelHeight getter
        """
        Pixel height in [mm].

        :getter: Gets the pixel height.
        :setter: Sets the pixel height.
        :type: double
        """
        return self.__pixelWidth

    @pixelHeight.setter
    def pixelHeight(self,h): #pixelHeight setter
        if (h<=0):
            warnMsg = self.getClassName() \
                            + ':pixelHeight: Height must be bigger than 0 [mm]. ' \
                            + 'Value ' + str(h) + ' will be ignored.'
            warnings.warn(warnMsg,SyntaxWarning)
        else:
            self.__pixelHeight = h;
        return None


#    @property
#    #@deprecated(version='0.2', reason="Deprecated. Use property layers instead.")
#    @deprecation.deprecated(deprecated_in="0.2", removed_in="0.3",
#                        current_version=__version__,
#                        details="Use property .layers instead.")
#    def layerIndex(self): #layerIndex getter
#        """
#        Selected retinal layer index(es) for being measured.
#        
#        ..note: Layers may be indicated by their index or by their names
#
#        :getter: Gets the retinal layer index.
#        :setter: Sets the retinal layer index. For selecting just one, an int
#            or a string, may be indicated.
#        :type: list
#        """
#        return self.layers
#
#    @layerIndex.setter
#    def layerIndex(self,i): #layerIndex setter
#        if type(i) is str: #layerName provided?
#            i = octant.RetinalLayers().getLayerIndex(i)
#        self.layers = i;
#        return None

    @property
    def layers(self): #layers getter
        """
        Selected set retinal layers for being measured.
        
        By default, all layers are selected.
        
        Layers may be indicated by their index (see
        :class:`IOT_RetinalLaers`, by their names, or by their acronyms.
        
        ..note: This attribute supersedes py:attr:`layerIndex`

        :getter: Gets the set retinal layers for being measured.
        :setter: Sets the set retinal layers for being measured.
            For selecting just one, a single int or a string, may be provided
            instead of a list.
            For selecting all, either provide the full list, or just -1.
        :type: list
        """
        return self.__layers

    @layers.setter
    def layers(self,theLayers): #layers setter
        if type(theLayers) is not list:
            #Encapsulate as list
            tmp=list()
            tmp.append(theLayers)
            theLayers = tmp
        
            
        #Check that elements of the list are retinal layers and "translate" to
        #internal representation as layer indexes.
        #Correctly identified layers are temporally saved to a new list.
        allLayerIndexes = RetinalLayers().getAllLayersIndexes();
        tmp=list()
        for elem in theLayers:
            if type(elem) is str: #layerName provided?
                elem = RetinalLayers().getLayerIndex(elem)
                tmp.append(elem)
            elif type(elem) is int:
                if elem in allLayerIndexes:
                    tmp.append(elem)
                else:
                    warnMsg = self.getClassName() + ':layers: Unrecognized layer index.'
                    warnings.warn(warnMsg,SyntaxWarning)
            else:
                warnMsg = self.getClassName() + ':layers: Unexpected list element for layers.'
                warnings.warn(warnMsg,SyntaxWarning)
            
        self.__layers = tmp;
        return None


    @property
    def pixelColumn(self): #pixelColumn getter
        """
        The pixel column around which to calculate the layers thicknesses.
        For global calculations, set py:attr:`pixelColumn` to -1.
        
        .. note:: If py:attr:`pixelColumn` exceeds the number of columns in the
            current :class:`octant.data.OCTscan` operand, then a warning is issued and 
            py:attr:`pixelColumn` will be set to -1 for global calculations.
            If the operand has not yet been set, will be set to -1 for global
            calculations.

        :getter: Gets the pixel column
        :setter: Sets the pixel column. 
        :type: int
        """
        return self.__pixelColumn

    @pixelColumn.setter
    def pixelColumn(self,pCol): #pixelColumn setter
        self.__pixelColumn = -1
        if self.arity() >= 1:
            tmpScan = self.operands[0]
            theScanWidth = tmpScan.shape[1]
            if (pCol >= -1 and pCol < theScanWidth):
                self.__pixelColumn = pCol
            else: #Unexpected case. Return warning
                warnMsg = self.getClassName() + ':pixelColumn: Value outside range.'
                warnings.warn(warnMsg,SyntaxWarning)
                #Note that if operands change afterwards, currently this does
                #not update, and may be beyond the range. This needs to be
                #re-check again at execution.
        return None


    @property
    def windowHalfWidth(self): #windowHalfWidth getter
        """
        The half width of the window around the py:attr:`pixelColumn` used to
        calculate the layers thicknesses.
        
        :getter: Gets the window half width.
        :setter: Sets the window half width.
        :type: int
        """
        return self.__windowHalfWidth

    @windowHalfWidth.setter
    def windowHalfWidth(self,w): #windowHalfWidth setter
        if w>=0:
            self.__windowHalfWidth = w
        else: #Unexpected case. Return warning
            warnMsg = self.getClassName() + ':windowHalfWidth: Window size must be a positive integer.'
            warnings.warn(warnMsg,SyntaxWarning)
        return None


    #Private methods

    #Public methods

    def execute(self,*args,**kwargs):
        """Executes the operation on the :py:attr:`operands`.
        
        Executes the operation on the :py:attr:`operands` and stores the outcome
        in :py:attr:`result`. Preload operands using
        :func:`octant.op.addOperand()`.
        
        :returns: Result of executing the operation.
        :rtype: list of thicknesses for selected layers (see :py:attr:`layers`)
        """
        
        #Ensure the operand has been set.
        if (len(self.operands) <1):
            warnMsg = self.getClassName() + ':execute: Operand not set.'
            warnings.warn(warnMsg,SyntaxWarning)
            return None
        
        imgin = self.operands[0]
        if type(imgin) is OCTscanSegmentation:
            imgin=imgin.data

        #Define a default output
        self.result = -1;
        #Check whether an image has been provided
        if imgin is None:
            print(self.getClasName(),": Image not selected. Generating a default empty profile.")
        else:
            #Normal behaviour of the function

            if self.pixelColumn == -1:
                #Sobre toda la imagen
                xmin = 0
                xmax = imgin.shape[1] #Image width
            else:
                #Sobre una ventana (o incluso un unico pixel)  
                xmin = max(0,self.pixelColumn-self.windowHalfWidth)
                xmax = min(I2.shape[1],self.pixelColumn+self.windowHalfWidth)
                
            #Extract window of interest
            imgin = imgin[xmin:xmax,:]
            
            tmpThicknesses = list()
            for elem in self.layers:
                #Count pixels corresponding to layers by column
                #tmpPixelCount = [sum(x) for x in zip(*imgin==elem)] #This works but it is very slow
                tmpPixelCount = sum(imgin==elem)
                #Calculate thickness
                tmpLayerThickness = np.mean(tmpPixelCount) * self.pixelHeight
                tmpThicknesses.append(tmpLayerThickness)
                
            self.result = tmpThicknesses
        
        return self.result




#    @deprecation.deprecated(deprecated_in="0.2", removed_in="0.3",
#                        current_version=__version__,
#                        details="Use method execute() instead.")
#    def getLayerThickness(self,segmentedImage, layerName, pixel = -1):
#        #Encapsulate the image as an OCTscan
#        tmp=OCTscan(segmentedImage)
#        self.clear()
#        self.addOperand(tmp)
#        self.layerIndex = layerName #The setter will transform into an idx
#        self.pixelColumn = pixel
#        #Execute
#        self.execute()

