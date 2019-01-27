"""
-*- coding: utf-8 -*-

.. currentmodule: src

File: IOT_OperationFlattening.py

Class IOT_OperationFlattening

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

.. seealso:: None
.. note:: None
.. todo:: None


.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Arlem Aleida Castillo Avila <acastillo@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""


## Import
from IOT_Operation import IOT_Operation
from IOT_OCTscan import IOT_OCTscan

import warnings
from deprecated import deprecated

import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
from skimage import io, color

from scipy.optimize import curve_fit
 





## Class definition
class IOT_OperationFlattening(IOT_Operation):
    """A flattening operation for :class:`OCTscan`.
    
    A flattening operation for :class:`OCTscan`.

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
        
        #Initialize private attributes unique to this instance
        #self._imgin = np.zeros(shape = (0,0,0), dtype = np.uint8 ); #Input image
        #self._imgout = np.zeros(shape = (0,0,0), dtype = np.uint8 ); #Output image
    
        return
    
    
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
        :func:`IOT:Operation.addOperand()`.
        
        :returns: Result of executing the operation.
        :rtype: :class:`IOT_OCTscan`
        """
        #print(self._getClasName(),": flattening: Starting flattening")
        
        #Ensure the operand has been set.
        if (len(self.operands)<1):
            warnMsg = self.getClassName() + ':execute: Operand not set.'
            warnings.warn(warnMsg,SyntaxWarning)
            return None
        
        imgin = self.operands[0]
        if isinstance(imgin,(IOT_OCTscan,)):
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
        
        popt, pcov = curve_fit(self.fittingQuadraticModel, x, markers, method = 'dogbox', loss = 'soft_l1')
        a = self.fittingQuadraticModel(x0, *popt)
        shift = np.max(a)
        flat = shift-a
        flat = np.round(flat)
        flat =np.ravel(flat).astype(int)
        
        newgray = I2
        for i in range(0,len(a)):
            newgray[:,i] = np.roll(I2[:,i], flat[i], axis=0)
        
        self.result = IOT_OCTscan(newgray)
        return self.result

    @deprecated(version='0.2', reason="Deprecated. Use method execute() instead.")
    def flattening(self,image):
        #Encapsulate the image as an IOT_OCTscan
        tmp=IOT_OCTscan(image)
        self.clear()
        self.addOperand(tmp)
        #Execute
        self.execute()
