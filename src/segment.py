    # -*- coding: utf-8 -*-
"""
Created on Mon May 21 20:16:06 2018

@author: Aleida
"""

from skimage import feature
import cv2
import segmentationUtils
#import matlab.engine

def segmentar(img):
    #Carga imagen
    #img,nombre = segmentationUtils.carga_imagen('D:\Documentos\OCT\imagenes\image4.png')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #segmentationUtils.mostrar_imagen(img)
    
    #Elimina el ruido externo de la imagen
    # =============================================================================
    #Elimina ruido
    img = segmentationUtils.ejecuta_close(img,4,4)
    segmentationUtils.mostrar_imagen(img)
    cv2.imwrite("paso2.tiff", img)
    
    eng = matlab.engine.start_matlab()
    eng.retSegment(img)
    #segmentationUtils.mostrar_imagen(img)
    
    
    
    #Elimina la imagen creada
    segmentationUtils.elimina_imagen(nombre)
