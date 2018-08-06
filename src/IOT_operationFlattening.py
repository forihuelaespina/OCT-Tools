# -*- coding: utf-8 -*-

# File: IOT_operationFlattening.py
#
# Operation flattening or rectification
# 
# Initial code isolated from previous file flattening.py
#
# This class rectifies and OCT image
#
#
#
# @dateCreated: 4-Aug-2018
# @authors: Arlem Aleida Castillo Avila, Felipe Orihuela-Espina
# @dateModified: 4-Aug-2018
#
# See also:
# 


#
# LOG:
#
# 4-Aug-2018: FOE:
#   * Isolated minimal solution.
#   * Encapsulated in class.
#


from IOT_operation import IOT_operation

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage import io, color

from scipy.optimize import curve_fit
 


def func(x, a, b, c):
    #quadratic model for curve optimization
    return a * x*x + b*x + c


class IOT_operationFlattening(IOT_operation):

    #Private class attributes shared by all instances
    
    #Class constructor
    def __init__(self):
        #Call superclass constructor
        super().__init__(1) #Set operation arity to 1.
        #Initialize private attributes unique to this instance
        self._imgin = np.zeros(shape = (0,0,0), dtype = np.uint8 ); #Input image
        self._imgout = np.zeros(shape = (0,0,0), dtype = np.uint8 ); #Output image
    
    
    #Private methods
    #def _rgb2gray(self,rgb):
    #    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

    
    #Public methods
    def flattening(self,image):
        #fig, ax = plt.subplots()
        #print("OCT-Tools: IOT_operationFlattening: flattening: Starting flattening")
        self._imgin = image
        
        
        #Check whether the image is in RGB (ndim=3) or in grayscale (ndim=2)
        #and convert to grayscale if necessary
        if self._imgin.ndim == 2:
            #Dimensions are only width and height. The image is already in grayscale.
            I2=self._imgin
        elif self._imgin.ndim == 3:
            #Image is in RGB. Convert.
            I2=color.rgb2gray(self._imgin);
        else: #Unexpected case. Return warning
            print("OCT-Tools: IOT_operationFlattening: Unexpected image shape.")
            return self._imgin
        
        
        
        
        #ax.imshow(I2, cmap = plt.get_cmap('gray'))
        
        aux = np.argmax(I2, axis=0)
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
        
        newgray = I2
        for i in range(0,len(a)):
            newgray[:,i] = np.roll(I2[:,i], flat[i], axis=0)
        
        self._imgout = newgray
        return newgray

