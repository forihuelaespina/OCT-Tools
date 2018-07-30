# -*- coding: utf-8 -*-
"""
Created on Mon May 21 19:54:41 2018

@author: Aleida
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.optimize import curve_fit
from skimage import io
 

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def func(x, a, b, c):
    return a * x*x + b*x + c

def flatening(filename):
    #fig, ax = plt.subplots()
    #img = mpimg.imread('D:\Documentos\OCT\imagenes\image3.png')
    #img = mpimg.imread(filename)
    print("entro")
    gray = filename
    #gray = rgb2gray(img)
    #ax.imshow(gray, cmap = plt.get_cmap('gray'))
    
    aux = np.argmax(gray, axis=0)
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
    
    
    popt, pcov = curve_fit(func, x, markers, method = 'dogbox', loss = 'soft_l1')
    a = func(x0, *popt)
    shift = np.max(a)
    flat = shift-a
    flat = np.round(flat)
    flat =np.ravel(flat).astype(int)
    newgray = gray
    
    for i in range(0,len(a)):
        newgray[:,i] = np.roll(gray[:,i], flat[i], axis=0)
    return newgray
#
#newgray = flatening('D:\Documentos\OCT\imagenes\image3.png')
###Hasta aquí ya hizo el "flatening"
#fig, ax = plt.subplots()
#plt.imsave('D:\Documentos\OCT\imagenes\image4.png', newgray , format ='png', cmap = plt.get_cmap('gray'))
    #io.imshow(newgray)    