"""
-*- coding: utf-8 -*-

File: IOT_OperationPerfilometer.py

Class IOT_OperationPerfilometer

Estimates reflectance perfilometry from OCT scans.

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

.. seealso:: None
.. note:: None
.. todo:: None

    
.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Arlem Aleida Castillo Avila <acastillo@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""

## Import
from IOT_Operation import IOT_Operation

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage import io, color




## Class definition
class IOT_OperationPerfilometer(IOT_Operation):
    #Sphinx documentation
    """This class retrieves the specular reflectivity from an OCT image.
    
    Estimates reflectance perfilometry from OCT scans.

    .. seealso:: 
    .. note:: 
    .. todo:: 
        
    """
 
    #Private class attributes shared by all instances
    
    #Class constructor
    def __init__(self):
        #Call superclass constructor
        super().__init__(1) #Set operation arity to 1.
        #Initialize private attributes unique to this instance
        self._imgin = np.zeros(shape = (0,0,0), dtype = np.uint8 ); #Input image
        self._perfil = np.zeros(shape = (0,0,0), dtype = np.uint8 ); #The profile image
    
    
    #Private methods

    #Public methods
    def perfilometry(self,image, pixel = -1 , a = 5):
        #print("OCT-Tools: IOT_operationPerfilometer: perfilometry: Estimating intensity profile")
        self._imgin = image
        #Define a default output
        perfil = np.array([0]);
        #Check whether an image has been provided
        if self._imgin is None:
            print(self.getClassName(),": Image not selected. Generating a default empty profile.")
        else:
            #Normal behaviour of the function
            
            #Check whether the image is in RGB (ndim=3) or in grayscale (ndim=2)
            #and convert to grayscale if necessary
            if self._imgin.ndim == 2:
                #Dimensions are only width and height. The image is already in grayscale.
                I2=self._imgin
            elif self._imgin.ndim == 3:
                #Image is in RGB. Convert.
                I2=color.rgb2gray(self._imgin);
            else: #Unexpected case. Return warning
                print(self.getClassName(),": Unexpected image shape.")
                return self._perfil
            
            I2shape = I2.shape;
            #io.imshow(I2)
            if pixel == -1:
                #Sobre toda la imagen
                perfil =np.mean(I2,1)
            else:
                #Sobre una ventana (o incluso un unico pixel)  
                #Hay que generalizarlo como un parámetro de la función
                pixel = [round(I2shape(1)/2), round(I2shape(2)/2)]
                perfil = np.mean(I2[:,pixel[1]-a:pixel[1]+a],1)
        self._perfil = perfil
        return self._perfil    
            
