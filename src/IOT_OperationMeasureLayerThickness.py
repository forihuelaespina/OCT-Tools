"""
-*- coding: utf-8 -*-

File: IOT_OperationMeasureLayerThickness.py

Class IIOT_OperationMeasureLayerThickness

A class for measuring layer thicknesses on OCT segmentations


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

.. seealso:: None
.. note:: None
.. todo:: None


.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Arlem Aleida Castillo Avila <acastillo@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""

## Import
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage import io, color

from IOT_Operation import IOT_Operation
from IOT_RetinalLayers import IOT_RetinalLayers



## Class definition
class IOT_OperationMeasureLayerThickness(IOT_Operation):
    #Sphinx documentation
    """A class for measuring layer thicknesses on OCT segmentations.

    This class estimates the thickness of layers from a segmented OCT image.

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
        self._pWidth = 1; #Pixel width in [mm]
        self._pHeight = 1; #Pixel height in [mm]
        self._imgin = np.zeros(shape = (0,0,0), dtype = np.uint8 ); #Segmentation input image
        self._layerIndex = -1; #Retinal layer index
        self._thickness = -1; #Thickness of the last measured layer

    #Private methods

    #Public methods
    def getPixelWidth(self):
        return self._pWidth

    def setPixelWidth(self,w):
        self._pWidth = w; #In [mm]
        return

    def getPixelHeight(self):
        return self._pHeight

    def setPixelHeight(self,h):
        self._pHeight = h; #In [mm]
        return


    def getLayerThickness(self,segmentedImage, layerName, pixel = -1):
        #print(self.getClasName(),": perfilometry: Estimating intensity profile")
        self._imgin = segmentedImage
        #Define a default output
        thickness = -1;
        #Check whether an image has been provided
        if self._imgin is None:
            print(self.getClasName(),": Image not selected. Generating a default empty profile.")
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
                print(self.getClasName(),": Unexpected image shape.")
                return self._perfil


            layerIndex = IOT_RetinalLayers().getLayerIndex(layerName)

            I2shape = I2.shape
            imWidth = I2shape(2);
            tmpThicknesses = np.zeros(shape = (1,imWidth), dtype = np.uint8 )
            #io.imshow(I2)
            if pixel == -1:
                #Sobre toda la imagen
                for x in range(1, imWidth):
                    #Find the superior border
                    supPixel = max(np.nonzero(I2[:,x]==layerIndex))
                    #Find the inferior border
                    subPixel = max(np.nonzero(I2[:,x]==(layerIndex-1))

                tmpThicknesses[x]=supPixel - subPixel

            else:
                #Sobre una ventana (o incluso un unico pixel)
                #Hay que generalizarlo como un parámetro de la función
                pixel = [round(I2shape(1)/2), round(I2shape(2)/2)]
                tmpWidth = pixel(2)-pixel(1)
                tmpThicknesses = np.zeros(shape = (1,tmpWidth), dtype = np.uint8 )
                for x in range(pixel(1), pixel(2)):
                    #Find the superior border
                    supPixel = max(np.nonzero(I2(:,x)==layerIndex))
                    #Find the inferior border
                    subPixel = max(np.nonzero(I2(:,x)==(layerIndex-1))

                tmpThicknesses(x)=supPixel - subPixel
                print('PENDING - Currently unable to measure average thickness')

        thickness =np.mean(tmpThicknesses,1) * self._pHeight
        self._thickness = thickness
        return self._thickness
