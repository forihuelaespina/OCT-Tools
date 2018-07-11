# -*- coding: utf-8 -*-
"""
Created on Thu May  3 11:32:21 2018

@author: Aleida
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage import io

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def perfilometro(I = mpimg.imread('D:\Documentos\OCT\git\src\code\OCT\scan1.png'), pixel = -1 , a = 5):
    I2=rgb2gray(I);
    #io.imshow(I2)
    if pixel == -1:
        #Sobre toda la imagen
        pixel = [round(np.size(I2,0)/2), round(np.size(I2,1)/2)]
        perfil = np.mean(I2[:,pixel[1]-a:pixel[1]+a],1)
        perfil =np.mean(I2,1)
        (ax, ax1) = plt.subplots()
        ax=plt.plot(perfil, np.arange(0,len(perfil)))
    else:
        #Sobre una ventana (o incluso un unico pixel) -La elecición del pixel 563 es de ejemplo. 
        #Hay que generalizarlo como un parámetro de la función
        pixel = [round(np.size(I2,0)/2), round(np.size(I2,1)/2)]
        perfil = np.mean(I2[:,pixel[1]-a:pixel[1]+a],1)
        #ax1=plt.plot(perfil, np.arange(0,len(perfil)))
    return perfil    
    plt.show()
        
