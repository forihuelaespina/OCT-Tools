# -*- coding: utf-8 -*-

# File: IOT_OperationSegmentation.py
#
# Operation Segmentation
# 
# Initial code isolated from previous file segment.py
#
# This class makes an automated segmentation of retinal layers from an OCT image
#
#
#
# @dateCreated: Feb-2018
# @authors: Arlem Aleida Castillo Avila, Felipe Orihuela-Espina
# @dateModified: 22-Aug-2018
#
# See also:
# 


#
# LOG:
#
# 5-Aug-2018: FOE:
#   * Isolated minimal solution.
#   * Encapsulated in class.
#
# 22-Aug-2018: FOE:
#   * Class name rebranded to capital "O" in operation
#   * Improved verbosity; now using class name
#


## Import
from IOT_Operation import IOT_Operation

import numpy as np
from skimage import feature, color
import cv2 #That's OpenCV
import segmentationUtils
#import matlab.engine




class IOT_OperationSegmentation(IOT_Operation):

    #Private class attributes shared by all instances
    
    #Class constructor
    def __init__(self):
        #Call superclass constructor
        super().__init__(1) #Set operation arity to 1.
        #Initialize private attributes unique to this instance
        self._imgin = np.zeros(shape = (0,0,0), dtype = np.uint8 ); #Input image
        self._imgout = np.zeros(shape = (0,0,0), dtype = np.uint8 ); #The segmented image
    
    
    #Private methods
        

    #Public methods
    def segmentar(self,image):
        #print("OCT-Tools: IOT_operationSegmentation: segmentar: Initiating retinal layer segmentation")
        self._imgin = image
        #Define a default output
        segmentedImage = np.zeros(shape = (0,0,0), dtype = np.uint8 );
        
        
        #Check whether the image is in RGB (ndim=3) or in grayscale (ndim=2)
        #and convert to grayscale if necessary
        #img = cv2.cvtColor(self._imgin, cv2.COLOR_BGR2GRAY)
        if self._imgin.ndim == 2:
            #Dimensions are only width and height. The image is already in grayscale.
            img=self._imgin
        elif self._imgin.ndim == 3:
            #Image is in RGB. Convert.
            img=color.rgb2gray(self._imgin);
        else: #Unexpected case. Return warning
            print(self.getClassName(),": Unexpected image shape.")
            return segmentedImage
        #segmentationUtils.mostrar_imagen(img)
        
        
        
        
        ## Algoritmo 1: Basado en el código de Matlab CASeReL
        # https://pangyuteng.github.io/caserel/
        #
        # Llama externamente a retSegment.exe
        #
        # Requiere de Matlab Runtime environment 
        
        
       #  #Remove external noise from image
       #  img = segmentationUtils.ejecuta_close(img,4,4) #Clausura
       #  #segmentationUtils.mostrar_imagen(img)
       #  
       #  #Generate temporal intermediate image file to be processed externally
       #  tmpFilename = "paso2.tiff"
       #  cv2.imwrite(tmpFilename, img)
       #  
       #  #Rely externally on the matlab algorithm for segmentation
       # # eng = matlab.engine.start_matlab()
       # # eng.retSegment(img)
       #  #segmentationUtils.mostrar_imagen(img)
       #  
       #  #Delete the intermediate image file
       #  segmentationUtils.elimina_imagen(tmpFilename)
        
        
        
        
        ## Algoritmo 2: Arlem
        img2 = img

        #Elimina ruido
        img = segmentationUtils.ejecuta_close(img,4,4)
        #segmentationUtils.mostrar_imagen(img)
        
        #Amplifica capas
        img = segmentationUtils.ejecuta_dilate(img,5,20,1)
        #segmentationUtils.mostrar_imagen(img)
        
        #Tensor
        Axx, Axy, Ayy = feature.structure_tensor(img)
        #segmentationUtils.mostrar_imagen(Ayy)
        
        #Elimina mas ruido
        Ayy = segmentationUtils.ejecuta_close(Ayy,6,1)
        #segmentationUtils.mostrar_imagen(Ayy)
        
        #Resalta las capas que sean mayores a la media
        Ayy = segmentationUtils.resalta_bordes(Ayy,True,0)
        #segmentationUtils.mostrar_imagen(Ayy)
        
        #Elimina aun mas ruido
        Ayy = segmentationUtils.ejecuta_open(Ayy,1,1)
        #segmentationUtils.mostrar_imagen(Ayy)
        
        #Binarizacion
        binary = segmentationUtils.ejecuta_OTSU(Ayy)
        #segmentationUtils.mostrar_imagen(binary)
        
        #elimina ruido del posible borde superior
        binary = segmentationUtils.ejecuta_elimina_ruido_extremos(True,0,0,binary)
        #segmentationUtils.mostrar_imagen(binary)
        
        #elimina ruido del posible borde inferior
        binary = segmentationUtils.ejecuta_elimina_ruido_extremos(False,0,0,binary)
        #segmentationUtils.mostrar_imagen(binary)
        
        #obtiene bordes exteriores
        arraySuperior, arrayInferior = segmentationUtils.obten_bordes_externos(binary)
        
        #elimina ruido a la imagen original
        img2 = segmentationUtils.elimina_desde_arreglos(img2, arraySuperior, arrayInferior)
        #segmentationUtils.mostrar_imagen(img2)
        
        img2 = segmentationUtils.ejecuta_close(img2,2,1)
        #segmentationUtils.mostrar_imagen(img2)
        
        img2 = feature.canny(img2,sigma = 2.5)
        #segmentationUtils.mostrar_imagen(img2)
        
        img2 = segmentationUtils.elimina_ruido_canny(img2,1)
        #segmentationUtils.mostrar_imagen(img2)
        
                
        print(self.getClassName(),": segmentar: Finishing retinal layer segmentation")
        
        
        
        self._imgout = img2
        return self._imgout    
