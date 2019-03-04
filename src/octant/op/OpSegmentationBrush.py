"""
-*- coding: utf-8 -*-

File: OpBrush.py

Class OpBrush

Operation Brush



:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
|  9-Jan-2018 | FOE    | - Class created.                                     |
+-------------+--------+------------------------------------------------------+
| 20-Jan-2018 | FOE    | - Major debugging.                                   |
+-------------+--------+------------------------------------------------------+
| 13-Dec-2018 | FOE    | - Remove importing of deprecated.                    |
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

import warnings

import numpy as np

from octant.data import OCTscanSegmentation, RetinalLayers
from .Operation import Operation


## Class definition
class OpSegmentationBrush(Operation):
    #Sphinx documentation
    """Operation Brush over a :class:`octant.data.OCTscanSegmentation`
    
    This class permits manual manipulation of a segmentation of retinal layers
    from an OCT image. The class provides a brush for "repainting" pixels
    of the segmentation assigning them a new layer label.
    
    This is a unary operation. Operand is of class class:`octant.data.OCTscanSegmentation`
        
    
    Current brush is squared.
        
    .. seealso:: None
    .. note:: None
    .. todo:: Add "rounded" brush.
        
    """
    
    #Class constructor
    def __init__(self):
        """The class constructor.

        The class constructor.

        tmp = OpSegmentationBrush() - Creates an empty brush operation
                
        """
        #Call superclass constructor
        super().__init__()

        #Set the operation name
        self.name = "Brush"

        #Initialize private attributes unique to this instance

        self.color = OCTscanSegmentation._BACKGROUND #Brush color.
        self.radius = 3; #Brush radius in pixels
    
        return
        
        
    #Properties getters/setters
    #
    # Remember: Sphinx ignores docstrings on property setters so all
    #documentation for a property must be on the @property method
    @property
    def color(self): #brushColor getter
        """
        The brush color, i.e. the retinal layer ID with which the brush paints;
        "Color" here is used as an analogy to painting.
        
        You can also set the color to BACKGROUND (default).
        
        .. seealso:: class:`octant.data.RetinalLayers`
                
        :getter: Gets the brush color
        :setter: Sets the brush color. Must be either BACKGROUND or a retinal layer.
        :type: tuple
        """
        return self.__color

    @color.setter
    def color(self,newColor): #color setter
        rlayers = RetinalLayers();
        if type(newColor) is str:
            #Convert to numerical index
            newColor = rlayers.getLayerIndex(newColor);
        
        #Check it is "within" range
        validColors = list()
        validColors.append(OCTscanSegmentation._BACKGROUND)
        validColors = validColors + rlayers.getAllLayersIndexes() #Concatenate lists
        #print(validColors)
        if newColor in validColors:
            self.__color = newColor
        else:
            warnMsg = self.getClassName() + ':color: Unexpected brush color. Brush color not updated.'
            warnings.warn(warnMsg,SyntaxWarning)
            
        return None
        
    @property
    def radius(self): #radius getter
        """
        The brush radius in pixels.
        
        You can also set the color to BACKGROUND (default).
        
        .. seealso:: class:`octant.data.RetinalLayers`
                
        :getter: Gets the brush color
        :setter: Sets the brush color. Must be either BACKGROUND or a retinal layer.
        :type: tuple
        """
        return self.__radius

    @radius.setter
    def radius(self,newRadius): #radius setter
        if type(newRadius) is not int:
            warnMsg = self.getClassName() + ':radius: Brush radius must be an integer.'
            warnings.warn(warnMsg,SyntaxWarning)
        elif newRadius > 0:
            self.__radius = newRadius
            
        return None
        
    #Private methods


    #Public methods 
    def execute(self,*args,**kwargs):
        """Executes the operation on the :py:attr:`operands`.
        
        Executes the operation on the :py:attr:`operands` and stores the 
        outcome in :py:attr:`result`. Preload operands using
        :func:`octant.Operation.addOperand()`.
        
        :param inputWindow: The document window from where to listen to mouse input
        :type inputWindow: class:`app.GUI_DocumentWindow`
        :returns: Result of executing the operation.
        :rtype: :class:`octant.OCTscanSegmentation`
        """
        #print(self._getClasName(),": brush: Starting brush")
        
        #Define a default result
        self.result = self.operands[0]; #Start by copying operand into result
        
        #Ensure the operand has been set.
        if (self.arity() <1):
            warnMsg = self.getClassName() + ':execute: Operand not set.'
            warnings.warn(warnMsg,SyntaxWarning)
            return self.result
        
        if not args: #Check if args is empty
            warnMsg = self.getClassName() + ':execute: No voxels selected.'
            warnings.warn(warnMsg,SyntaxWarning)
            return self.result
            
        voxelList = args[0] #List of visited voxels.
                            #Note that these are the center of the brush
        r = self.radius
        for tmpVoxel in voxelList:
            #Update the voxel (and its radius-sized neighbourhood)
            #print("Brushing " + str(tmpVoxel) + " in color " + str(self.color))
            #Extract squared subimage around voxel (without exceeding borders).
            xmin = max(0,tmpVoxel[0]-r)
            xmax = min(self.result.shape[0],tmpVoxel[0]+r+1)
            ymin = max(0,tmpVoxel[1]-r)
            ymax = min(self.result.shape[1],tmpVoxel[1]+r+1)
            ixgrid = np.ix_(np.arange(xmin,xmax),
                            np.arange(ymin,ymax))
            self.result.data[ixgrid] = self.color
        return self.result