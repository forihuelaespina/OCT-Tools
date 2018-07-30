# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 19:52:45 2018

@author: Aleida
"""

from skimage import feature
import cv2
import segmentationUtils
from subprocess import call
import scipy.io
from random import randint
import os
import matplotlib.pyplot as plt
import numpy as np



#Carga imagen
img = cv2.imread('D:\Documentos\OCT\imagenes\image1.jpg')
nombre = '_'+str(randint(1000000, 9999999))+'_.jpg'
cv2.imwrite(nombre, img)  

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#segmentationUtils.mostrar_imagen(img)

#Elimina el ruido externo de la imagen
# =============================================================================
#Elimina ruido
img = cv2.bilateralFilter(img, 6, 50,3)
img = segmentationUtils.ejecuta_close(img,4,4)
#segmentationUtils.mostrar_imagen(img)
#cv2.imwrite("paso2.tiff", img)
directorio = os.getcwd() + '\\'+ nombre
print(directorio)
call(["retSegment\\for_testing\\retSegment", directorio])
mat = scipy.io.loadmat(directorio+'_octSegmentation_layers.mat')
retinalLayers = mat['retinalLayers']


fig = plt.figure(figsize = (10,10))
imgplot = plt.imshow(img, cmap=plt.cm.gray, figure = fig)

x = retinalLayers[0][0][0][0]
y = retinalLayers[0][0][1][0]
plt.plot(y,x, 'b-', figure = fig, label = retinalLayers[0][0][4][0])


x = retinalLayers[0][1][0][0]
y = retinalLayers[0][1][1][0]
plt.plot(y,x, 'r-', figure = fig, label = retinalLayers[0][1][4][0])


x = retinalLayers[0][2][0][0]
y = retinalLayers[0][2][1][0]
plt.plot(y,x, 'g-', figure = fig, label = retinalLayers[0][2][4][0])


x = retinalLayers[0][3][0][0]
y = retinalLayers[0][3][1][0]
plt.plot(y,x, 'm-', figure = fig, label = retinalLayers[0][3][4][0])


x = retinalLayers[0][4][0][0]
y = retinalLayers[0][4][1][0]
plt.plot(y,x, 'y-', figure = fig, label = retinalLayers[0][4][4][0])


x = retinalLayers[0][5][0][0]
y = retinalLayers[0][5][1][0]
plt.plot(y,x, 'c-', figure = fig, label = retinalLayers[0][5][4][0])


x = retinalLayers[0][6][0][0]
y = retinalLayers[0][6][1][0]
plt.plot(y,x, 'w-', figure = fig, label = retinalLayers[0][6][4][0])
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

#segmentationUtils.mostrar_imagen(img)



#Elimina la imagen creada
segmentationUtils.elimina_imagen(nombre)