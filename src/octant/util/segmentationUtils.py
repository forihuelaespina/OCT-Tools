# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 20:12:03 2018


:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 3-Aug-2018  | ACA    | - File created.                                      |
+-------------+--------+------------------------------------------------------+
| ??-???-2018 | ACA    | - Addition of several functions and debugging.       |
+-------------+--------+------------------------------------------------------+
| 30-Mar-2019 | FOE    | - Added file log.                                    |
+-------------+--------+------------------------------------------------------+


.. seealso:: None
.. note:: None
.. todo:: None


.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Arlem Aleida Castillo Avila <acastillo@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""
import matplotlib.pyplot as plt
from skimage import io, filters
import numpy as np
import cv2
from PIL import Image
from random import randint
import os

#devuelve true si la imagen original era PNG
def esPNG(nombre):
    return nombre != ''

#mostrar imagen
def mostrar_imagen(img):
    fig, ax = plt.subplots()
    io.imshow(img)

#elimina imagen
def elimina_imagen(nombre):
    if esPNG(nombre):
        os.remove(nombre)

#retorna la imagen a cargar
def carga_imagen(path):
    img = Image.open(path)
    nombre = ''
    #Convierte a JPEG la imagen y la salva
    if img.format == 'PNG':
        nombre = '_'+str(randint(1000000, 9999999))+'_.jpg'
        img = img.convert("RGB")
        img.save(nombre, "JPEG")
    #Carga imagen
    return [cv2.imread(nombre if nombre != '' else path),nombre]

#bordeSuperior si es true entonces elimina ruido hacia arriba sino hacia abajo
def elimina_ruido(bordeSuperior,indiceY,indiceX,matrizIMG):
    if bordeSuperior:
        for y in range(indiceY,-1,-1):
            matrizIMG[y][indiceX] = False
    else:
        for y in range(indiceY,np.size(matrizIMG,0)):
            matrizIMG[y][indiceX] = False
    return matrizIMG

#obtiene los indices para comenzar a eliminar en cada iteracion
def obten_indices(bordeSuperior,indiceY,indiceX,matrizIMG,borde):
    maximo = np.size(matrizIMG,0)
    if bordeSuperior:
        if borde:
            for y in range(++indiceY,-1,-1):
                if not matrizIMG[y][indiceX]:
                    indiceY = y
                    break
        else:
            for y in range(++indiceY,maximo):
                if matrizIMG[y][indiceX]:
                    indiceY = y
                    break
    else:
        if borde:
            for y in range(++indiceY,maximo):
                if not matrizIMG[y][indiceX]:
                    indiceY = y
                    break
        else:
            for y in range(++indiceY,-1,-1):
                if matrizIMG[y][indiceX]:
                    indiceY = y
                    break
    return indiceY

#elimina ruido derecha a izquier
def elimina_ruido_der_izq(indiceX,indiceY,matrizIMG,bordeSuperior):
    for x in range(--indiceX,-1,-1):
        if matrizIMG[indiceY][x]:
            indiceY = obten_indices(bordeSuperior,indiceY,x,matrizIMG,True)
        else:
            indiceY = obten_indices(bordeSuperior,indiceY,x,matrizIMG,False)
        matrizIMG = elimina_ruido(bordeSuperior,indiceY,x,matrizIMG)
    return matrizIMG

#actualiza indices
def elimina_indices(indiceY,indiceX,tempY,tempX,matrizIMG,indiceActualY,bordeSuperior):
    if bordeSuperior:
        for y in range(indiceY,np.size(matrizIMG,0)):
            if matrizIMG[y][indiceX]:
                if (y > tempY) or tempY == 0:
                    tempY = y
                    tempX = indiceX
                indiceActualY = y if y > 0 else 0
                break
    else:
        for y in range(indiceY,-1,-1):
            if matrizIMG[y][indiceX]:
                if (y < tempY) or tempY == 0:
                    tempY = y
                    tempX = indiceX
                indiceActualY = ++y if y < np.size(matrizIMG,0) else np.size(matrizIMG,0)-2
                break
    return [tempX,tempY,indiceActualY]

#elimina ruido izquierda a derecha
def elimina_izq_der(bordeSuperior,matrizIMG,tempActualY,tempX,tempY):
    for x in range(51,np.size(matrizIMG,1)):
        if bordeSuperior:
            if not matrizIMG[tempActualY][x]:
                [tempX,tempY,tempActualY] = elimina_indices(tempActualY,x,tempY,tempX,matrizIMG,tempActualY,bordeSuperior)
            else:
                tempActualY = obten_indices(bordeSuperior,tempActualY,x,matrizIMG,True)
            matrizIMG = elimina_ruido(bordeSuperior,tempActualY,x,matrizIMG)
        else:
            if not matrizIMG[tempActualY][x]:
                [tempX,tempY,tempActualY] = elimina_indices(tempActualY,x,tempY,tempX,matrizIMG,tempActualY,bordeSuperior)
            else:
                tempActualY = obten_indices(bordeSuperior,tempActualY,x,matrizIMG,True)
            matrizIMG = elimina_ruido(bordeSuperior,tempActualY,x,matrizIMG)
    return [matrizIMG,tempX,tempY]

#ejecuta elimina ruido izquierda derecha
def ejecuta_elimina_izq_der(tempY,tempX,matrizIMG,bordeSuperior):
    if tempY !=0:
        matrizIMG = elimina_ruido_der_izq(tempX,tempY,matrizIMG,bordeSuperior)
    return matrizIMG

#ejecuta elimina ruido derecha izquierda
def ejecuta_elimina_ruido_extremos(bordeSuperior,tempY,tempX,matrizIMG):
    tempActualY = 0
    tempX = 0
    tempY = 0
    if bordeSuperior:
        for y in range(10,np.size(matrizIMG,0)):
            if matrizIMG[y][50]:
                tempActualY = y
                matrizIMG,tempX,tempY = elimina_izq_der(True,matrizIMG,tempActualY,tempX,tempY)
                break
        matrizIMG = ejecuta_elimina_izq_der(tempY,tempX,matrizIMG,bordeSuperior)
    else:
        for y in range(np.size(matrizIMG,0)-10,-1,-1):
            if matrizIMG[y][50]:
                tempActualY = y
                matrizIMG,tempX,tempY = elimina_izq_der(False,matrizIMG,tempActualY,tempX,tempY)
                break
        matrizIMG = ejecuta_elimina_izq_der(tempY,tempX,matrizIMG,bordeSuperior)
    return matrizIMG

#resalta bordes dado un porcentaje si el parametro esMedia == false, si es true, saca la media y utiliza ese valor para resaltar los bordes
def resalta_bordes(matrizIMG,esMedia,porcentaje):
    maximo = np.amax(matrizIMG)
    media = np.mean(matrizIMG) if esMedia else (np.amax(matrizIMG)*porcentaje)/100
    for y in range (0, np.size(matrizIMG,0)):
        for x in range(0,np.size(matrizIMG,1)):
            if matrizIMG[y][x] > media:
                matrizIMG[y][x] = maximo
    return matrizIMG

#elimina columnas
def elimina_columnas(matrizIMG,x,yInicial):
    for y in range(yInicial,np.size(matrizIMG,0)):
        if not matrizIMG[y][x]:
            break
        else:
            matrizIMG[y][x] = False
    return matrizIMG

#elimina ruido
def elimina_ruido_canny(matrizIMG, iteraciones):
    for i in range(0,iteraciones):
        for y in range (10, np.size(matrizIMG,0) - 1):
            for x in range(1, np.size(matrizIMG,1) - 1):
                if matrizIMG[y][x] and matrizIMG[y+1][x]:
                    matrizIMG = elimina_columnas(matrizIMG,x,y+1)
                if matrizIMG[y][x] and (not matrizIMG[y][x+1] and not matrizIMG[y+1][x+1] and not matrizIMG[y-1][x+1] and
                    not matrizIMG[y+1][x] and not matrizIMG[y][x-1] and not matrizIMG[y+1][x-1] and not matrizIMG[y-1][x-1]):
                    matrizIMG[y][x] = False
    return matrizIMG

#ejecuta close
def ejecuta_close(matrizIMG,x,y):
    kernel = np.ones((x,y),np.uint8)
    matrizIMG = cv2.morphologyEx(matrizIMG, cv2.MORPH_CLOSE, kernel)
    return matrizIMG

#ejecuta open
def ejecuta_open(matrizIMG,x,y):
    kernel = np.ones((x,y),np.uint8)
    matrizIMG = cv2.morphologyEx(matrizIMG, cv2.MORPH_OPEN, kernel)
    return matrizIMG

#ejecuta erode
def ejecuta_erode(matrizIMG,x,y,i):
    kernel = np.ones((x,y),np.uint8)
    matrizIMG = cv2.erode(matrizIMG,kernel,iterations = i)
    return matrizIMG

#ejecuta dilate
def ejecuta_dilate(matrizIMG,x,y,i):
    kernel = np.ones((x,y),np.uint8)
    matrizIMG = cv2.dilate(matrizIMG,kernel,iterations = i)
    return matrizIMG

#ejecuta gradient
def ejecuta_gradient(matrizIMG,x,y):
    kernel = np.ones((x,y),np.uint8)
    matrizIMG = cv2.morphologyEx(matrizIMG, cv2.MORPH_GRADIENT, kernel)
    return matrizIMG

#ejecuta gradient
def ejecuta_blackhat(matrizIMG,x,y):
    kernel = np.ones((x,y),np.uint8)
    matrizIMG = cv2.morphologyEx(matrizIMG, cv2.MORPH_BLACKHAT, kernel)
    return matrizIMG

#ejecuta OTSU
def ejecuta_OTSU(matrizIMG):
    thresh = filters.threshold_otsu(matrizIMG)
    matrizIMG = matrizIMG > thresh
    return matrizIMG

#obtiene los bordes y los almacena en 2 arreglos
def obten_bordes_externos(matrizIMG):
    arraySuperior=[0]*np.size(matrizIMG,1)
    arrayInferior=[0]*np.size(matrizIMG,1)
    for x in range(0,np.size(matrizIMG,1)):
        for y in range(10,np.size(matrizIMG,0)):
            if matrizIMG[y][x]:
                arraySuperior[x] = y
                break
        for y in range(np.size(matrizIMG,0)-1,-1,-1):
            if matrizIMG[y][x]:
                arrayInferior[x] = y
                break
    return [arraySuperior, arrayInferior]

#dado 2 arreglos en "y" modifica todos los valores mayores (arrayInferior) y menores (arraySuperior) a estos, por por el valor minimo en la imagen
def elimina_desde_arreglos(matrizIMG,arraySuperior,arrayInferior):
    arrayImg = matrizIMG.reshape(-1)
    media = min(arrayImg)
    for x in range(0,np.size(matrizIMG,1)):
        indiceY = arraySuperior[x]
        for y in range(indiceY-1,-1,-1):
            matrizIMG[y][x] = media
        indiceY = arrayInferior[x]
        for y in range(indiceY+1,np.size(matrizIMG,0)):
            matrizIMG[y][x] = media
    return matrizIMG
