# -*- coding: utf-8 -*-

# File: IOT_OperationFlattening.py
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
# @dateModified: 22-Aug-2018
#
# See also:
# 


## Log
#
# 4-Aug-2018: FOE:
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
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage import io, color

from scipy.optimize import curve_fit
 


def func(x, a, b, c):
    #quadratic model for curve optimization
    return a * x*x + b*x + c



## Class definition
class IOT_OperationFlattening(IOT_Operation):

    #Private class attributes shared by all instances
    
    #Class constructor
    def __init__(self):
        #Call superclass constructor
        super().__init__(1) #Set operation arity to 1.
        #Initialize private attributes unique to this instance
        self._imgin = np.zeros(shape = (0,0,0), dtype = np.uint8 ); #Input image
        self._imgout = np.zeros(shape = (0,0,0), dtype = np.uint8 ); #Output image
    
    
    #Private methods

    
    #Public methods
    def flattening(self,image):
        #fig, ax = plt.subplots()
        #print(self._getClasName(),": flattening: Starting flattening")
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
            print(self._getClasName(),": Unexpected image shape.")
            return self._imgin
        
        
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

