# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 22:06:40 2018

@author: Aleida
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.interpolate import interp1d

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

fig, ax = plt.subplots()
img = mpimg.imread('D:\Documentos\OCT\git\src\code\OCT\scan1.png')
gray = rgb2gray(img)
im = ax.imshow(gray, cmap = plt.get_cmap('gray'))
aux = np.argmax(gray, axis=0)
mg = np.mean(aux)
sdg = np.std(aux)
markers = []

for i in range(0,len(aux)):
    if mg - sdg <= aux[i] <= mg +sdg: 
        markers+= [aux[i]]
    else:
        markers+= [markers[i-1]]

x = np.arange(len(markers))
f = interp1d(x, markers, kind = 'cubic')
        
ax.plot(f(x), '.')
plt.show()
