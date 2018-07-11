    # -*- coding: utf-8 -*-
"""
Created on Mon May 21 20:16:06 2018

@author: Aleida
"""

from skimage import feature
import cv2
import segmentationUtils
#Carga imagen
img,nombre = segmentationUtils.carga_imagen('D:\Documentos\OCT\imagenes\image4.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#segmentationUtils.mostrar_imagen(img)
img2 = img

#Elimina el ruido externo de la imagen
# =============================================================================
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

# =============================================================================
#obtiene bordes exteriores
arraySuperior, arrayInferior = segmentationUtils.obten_bordes_externos(binary)

#elimina ruido a la imagen original
img2 = segmentationUtils.elimina_desde_arreglos(img2, arraySuperior, arrayInferior)
#segmentationUtils.mostrar_imagen(img2)
# =============================================================================

img2 = segmentationUtils.ejecuta_close(img2,2,1)
#segmentationUtils.mostrar_imagen(img2)

img2 = feature.canny(img2,sigma = 2.5)
#segmentationUtils.mostrar_imagen(img2)

img2 = segmentationUtils.elimina_ruido_canny(img2,1)
segmentationUtils.mostrar_imagen(img2)

#Elimina la imagen creada
segmentationUtils.elimina_imagen(nombre)
