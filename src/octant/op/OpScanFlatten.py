"""
-*- coding: utf-8 -*-

.. currentmodule: src

File: OpFlattening.py

Class OpFlattening

Initial code was isolated from previous file flattening.py


:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
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
| 23-Sep-2018 | FOE    | - Adapted to IOT_Operation becoming abstract and new |
|             |        |   capabilities. Added method .execute, integration of|
|             |        |   operands, given operation name, deprecated method  |
|             |        |   flattening.                                        |
|             |        | - External quadratic function is now a private       |
|             |        |   method and rebranded as fittingQuadraticModel      |
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
|  4-Apr-2019 | FOE    | - Bug fixing. References to                          |
|             |        |   :class:`octant.data.OCTscan` updated.              |
+-------------+--------+------------------------------------------------------+
|  2-Jun-2019 | FOE    | - New read only property deformation map to store    |
|             |        |   the deformation map associated with the flattening |
|             |        |   operation.                                         |
|             |        | - New method applyOperation to repeat a known        |
|             |        |   flatenning operation to operands. This can be used |
|             |        |   to apply the same flattening to a different set    |
|             |        |   of scans. In practical terms, it can be used to    |
|             |        |   apply the same flatenning to segmentation scans    |
|             |        |   after it has been precalculated to anatomical      |
|             |        |   scans.                                             |
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
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
from skimage import io, color

from scipy.optimize import curve_fit
 

#from version import __version__
from .Operation import Operation
from octant.data import OCTscan



## Class definition
class OpScanFlatten(Operation):
    """A flattening operation for :class:`octant.data.OCTscan`.
    
    A flattening operation for :class:`octant.data.OCTscan`.

    The operation represented by this class rectifies an OCT scan.

    
    
    .. seealso:: None
    .. note:: None
    .. todo:: None
        
    """
 
    #Private class attributes shared by all instances
    
    #Class constructor
    def __init__(self):
        #Call superclass constructor
        super().__init__()
        
        #Set the operation name
        self.name = "Flattening"
        
        self.__deformationMap = None
        
        return
    
    
    @property
    def deformationMap(self): #name getter
        """
        A logical name for the study.
        
        This is a read only property.
        
        :getter: Gets the deformationMap associated to the last flattening.
        :type: str
        """
        return self.__deformationMap
    
    
    #Private methods
    # def __str__(self):
    #     #This not working yet; it gets into an infiite recursion as
    #     #super().__str__() calls self.getClassName() in THIS class.
    #     # s = '<' + self.getClassName() + '([' \
    #     #     + super().__str__() + '])>'
    #     s = '<' + self.getClassName() + '([' \
    #             + str(super()) + '])>'
    #     print(super())
    #     return s

    @staticmethod
    def fittingQuadraticModel(x, a, b, c):
        #quadratic model for curve optimization
        return a * x*x + b*x + c

    
    #Public methods
    def execute(self,*args,**kwargs):
        """Executes the operation on the :py:attr:`operands`.
        
        Executes the operation on the :py:attr:`operands` and stores the outcome
        in :py:attr:`result`. Preload operands using
        :func:`octant.Operation.addOperand()`.
        
        :returns: Result of executing the operation.
        :rtype: :class:`octant.data.OCTscan`
        """
        #print(self._getClasName(),": flattening: Starting flattening")
        
        #Ensure the operand has been set.
        if (len(self.operands)<1):
            warnMsg = self.getClassName() + ':execute: Operand not set.'
            warnings.warn(warnMsg,SyntaxWarning)
            return None
        
        imgin = self.operands[0]
        if type(imgin) is OCTscan:
            imgin=imgin.data
        
        #Check whether the image is in RGB (ndim=3) or in grayscale (ndim=2)
        #and convert to grayscale if necessary
        if imgin.ndim == 2:
            #Dimensions are only width and height. The image is already in grayscale.
            I2=imgin
        elif imgin.ndim == 3:
            #Image is in RGB. Convert.
            I2=color.rgb2gray(imgin);
        else: #Unexpected case. Return warning
            print(self._getClasName(),": Unexpected image shape.")
            self.result = imgin
            return self.result
        
        aux = np.argmax(I2, axis=0)
        mg = np.mean(aux)
        sdg = np.std(aux)
        markers = []
        remover =[]
        x0 = np.arange(len(aux))
        
        for i in range(0,len(aux)):
            if mg - 3*sdg <= aux[i] <= mg +3*sdg: 
                markers+= [aux[i]]
            else:
                remover+= [i]
        x=np.delete(x0,remover)
        
        modelCoeffs, pcov = curve_fit(self.fittingQuadraticModel, x, markers, \
                                    method = 'dogbox', loss = 'soft_l1')
        a = self.fittingQuadraticModel(x0, *modelCoeffs)
        shift = np.max(a)
        flat  = shift-a
        flat  = np.round(flat)
        flat  = np.ravel(flat).astype(int)
        self.__deformationMap = flat
        
        newgray = I2
        for i in range(0,len(a)):
            newgray[:,i] = np.roll(I2[:,i], flat[i], axis=0)
        
        self.result = OCTscan(newgray)
        return self.result

#    #@deprecated(version='0.2', reason="Deprecated. Use method execute() instead.")
#    @deprecation.deprecated(deprecated_in="0.2", removed_in="0.3",
#                        current_version=__version__,
#                        details="Use method execute() instead.")
#    def flattening(self,image):
#        #Encapsulate the image as an OCTscan
#        tmp=OCTscan(image)
#        self.clear()
#        self.addOperand(tmp)
#        #Execute
#        self.execute()


    def applyOperation(self, scanA):
        """Apply the current flattening to the given scan.
        
        Instead of calculating the fitting again needed for the
        flattening, this method applies a known fitted quadratic model to
        the given parameters.
        
        The result is NOT stored in :py:attr:`result`.
        
        :param scanA: Image to flatten.
        :type scanA: :class:`octant.data.OCTscan`
        :returns: Result of repeating the last flattening operation onto
             parameter scanA.
        :rtype: :class:`octant.data.OCTscan`
        """
        if type(scanA) is OCTscan:
            scanA=scanA.data
        newgray = scanA
        for i in range(0,len(self.deformationMap)):
            newgray[:,i] = np.roll(scanA[:,i], self.deformationMap[i], axis=0)
        return OCTscan(newgray)
