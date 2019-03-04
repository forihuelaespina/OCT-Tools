"""
-*- coding: utf-8 -*-

File: OpPerfilometer.py

Class OpPerfilometer

Estimates reflectance perfilometry or brightness profile from OCT scans.

Initial code isolated from previous file perfilometro.py


:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 3-Aug-2018  | FOE    | - Removed default value for first parameter of       |
|             |        |   function perfilometer, and added an internal       |
|             |        |   parameter check on the function.                   |
+-------------+--------+------------------------------------------------------+   
| 4-Aug-2018  | FOE    | - Isolated minimal solution.                         |
|             |        | - Encapsulated in class.                             |
+-------------+--------+------------------------------------------------------+   
| 22-Aug-2018 | FOE    | - Rebranded to capital "O" in operation;             |
|             |        |   IOT_Operation                                      |
|             |        | - Improved verbosity; now using class name           |
+-------------+--------+------------------------------------------------------+
| 23-Sep-2018 | FOE    | - Updated comments and added Sphinx                  |
|             |        |   documentation to the class                         |
+-------------+--------+------------------------------------------------------+
| 17-Sep-2018 | FOE    | - Adapted to IOT_Operation becoming abstract and new |
|             |        |   capabilities. Added method .execute, integration of|
|             |        |   operands, given operation name, deprecated method  |
|             |        |   perfilometry.                                      |
+-------------+--------+------------------------------------------------------+
| 18-Oct-2018 | FOE    | - Now using the class:`IOT_OCTscan`                  |
|             |        | - Operation meta-parameters py:attr:`pixelColumn`    |
|             |        |   and py:attr:`windowHalfWidth` are now encapsulated.|
+-------------+--------+------------------------------------------------------+
|  5-Nov-2018 | FOE    | - Minor debugging                                    |
|             |        | - Added a toDo for listening to operands change so   |
|             |        |   that property pixelCount is always within range.   |
+-------------+--------+------------------------------------------------------+
|  1-Dec-2018 | FOE    | - Adapted to new signature of inherited execute()    |
|             |        |   method to accept parameters.                       |
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
|             |        | - Previously deprecated method perfilometer have now |
|             |        |   been fully removed.                                |
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
from octant.data import OCTscan
from .Operation import Operation


## Class definition
class OpScanPerfilometer(Operation):
    #Sphinx documentation
    """This class retrieves the reflectivity (brightness profile) from an OCT image.
    
    Estimates reflectance perfilometry (brightness profile) from class:`octant.data.OCTscan`.

    .. seealso:: None
    .. note:: None
    .. todo:: The pixelColumn property currently does not listens to changes
        in the operand, and thus changes in the operand might make the
        pixelColumn to "go" outside range.
        
    """
 
    #Private class attributes shared by all instances
    
    #Class constructor
    def __init__(self):
        #Call superclass constructor
        super().__init__()

        #Set the operation name
        self.name = "Perfilometer"
        
        #Initialize private attributes unique to this instance
        self.pixelColumn = -1 #Pixel around where to measure.
        self.windowHalfWidth = 0 #Width of measuring window
    
    
    #Properties getters/setters
    #
    # Remember: Sphinx ignores docstrings on property setters so all
    #documentation for a property must be on the @property method
    @property
    def pixelColumn(self): #pixelColumn getter
        """
        The pixel column around which to calculate the brightness profile.
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
        calculate the brightness profile.
        
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
        :func:`octant.op.Operation.addOperand()`.
        
        .. note:: If py:attr:`pixelColumn` is set to -1, global calculations are carried
            out regardless of the value of the window size.
            If the window around py:attr:`pixelColumn` sized 
            2* py:attr:`windowHalfWidth` exceeds the :class:`octant.data.OCTscan`
            operand width, the window will be truncated.

        :returns: Result of executing the operation.
        :rtype: list of float
        """
        #print(self._getClasName(),": flattening: Starting flattening")
        
        #Ensure the operand has been set.
        if (self.arity() <1):
            warnMsg = self.getClassName() + ':execute: Operand not set.'
            warnings.warn(warnMsg,SyntaxWarning)
            return None
        
        imgin = self.operands[0]
        
        if type(imgin) is OCTscan:
            imgin=imgin.data

        theScanWidth = imgin.shape[1]
        if (self.pixelColumn >= theScanWidth):
            warnMsg = self.getClassName() + ':pixelColumn: Value outside range.'
            warnings.warn(warnMsg,SyntaxWarning)
            return None

        
        #print("OCT-Tools: IOT_operationPerfilometer: perfilometry: Estimating intensity profile")
        #Define a default output
        perfil = np.array([0]);
        #Check whether an image has been provided
        if imgin is None:
            print(self.getClassName(),": Image not selected. Generating a default empty profile.")
        else:
            #Normal behaviour of the function
            
            #Check whether the image is in RGB (ndim=3) or in grayscale (ndim=2)
            #and convert to grayscale if necessary
            if imgin.ndim == 2:
                #Dimensions are only width and height. The image is already in grayscale.
                I2=imgin
            elif imgin.ndim == 3:
                #Image is in RGB. Convert.
                I2=color.rgb2gray(imgin);
            else: #Unexpected case. Return warning
                print(self.getClassName(),": Unexpected image shape.")
                self.result = perfil
                return self.result
            
            if self.pixelColumn == -1:
                #Sobre toda la imagen
                perfil =np.mean(I2,1)
            else:
                #Sobre una ventana (o incluso un unico pixel)  
                lowerLimit = max(0,self.pixelColumn-self.windowHalfWidth)
                upperLimit = min(I2.shape[1],self.pixelColumn+self.windowHalfWidth)
                perfil = np.mean(I2[:,lowerLimit:upperLimit],1)
        self.result = perfil
        return self.result    
            

#    #@deprecated(version='0.2', reason="Deprecated. Use method execute() instead.")
#    @deprecation.deprecated(deprecated_in="0.2", removed_in="0.3",
#                        current_version=__version__,
#                        details="Use method execute() instead.")
#    def perfilometry(self,image, pixel = -1 , a = 5):
#        #Encapsulate the image as an OCTscan
#        tmp=OCTscan(image)
#        self.clear()
#        self.addOperand(tmp)
#        self.pixelColumn = pixel
#        self.windowHalfWidth = a
#        #Execute
#        self.execute()
