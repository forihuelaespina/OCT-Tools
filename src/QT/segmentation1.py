# -*- coding: utf-8 -*-
"""
Created on Mon May 21 20:16:06 2018

@author: Aleida
"""

import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from skimage import io, exposure, feature, filters
import flattening as fl
from skimage.morphology import disk, dilation, remove_small_objects, binary_dilation
from skimage.measure import label, regionprops
from skimage.color import label2rgb
import cv2
import bilateral as bi


fig, ax = plt.subplots()
src = cv2.imread('D:\Documentos\OCT\imagenes\image3.png', 0)
io.imshow(src)
#img_nr = bi.bilateral_filter_own(src, 5, 12, 16)
img_nr = cv2.bilateralFilter(src, 6, 50,3)
#img_nr = cv2.fastNlMeansDenoisingMulti(fl.rgb2gray(src), 2, 5, None, 4, 7, 35)


Axx, Axy, Ayy = feature.structure_tensor(img_nr, sigma=2.4, mode = 'constant', cval=0)

#Ayy = exposure.rescale_intensity(Ayy, in_range=(-1, 1))


fig, ax = plt.subplots()
io.imshow(Ayy)
edges = feature.canny(Ayy)
kernel = np.ones((1,1),np.uint8)
opening = cv2.morphologyEx(np.uint8(edges), cv2.MORPH_OPEN, kernel)
fig2, ax3 = plt.subplots()
ax3.imshow(edges, interpolation= 'nearest', cmap = plt.get_cmap('gray'))








#
#from PIL import Image 
#img = Image.fromarray(img_nr)
#rsFactor = 0.1
##img = img.resize( ( (int(img.size[0]*rsFactor)),(int(img.size[1]*rsFactor))) ,Image.ANTIALIAS)
##img = np.array(img)
##szImg = img.shape
#
#sx = ndimage.sobel(img, axis=0, mode='constant')
#sy = ndimage.sobel(img, axis=1, mode='constant')
#sob = np.hypot(sx, sy) 
#sob = exposure.rescale_intensity(sob, in_range=(-1, 1))
#io.imshow(sob)
#thresh = filters.threshold_otsu(sob)
#binary = (sob >= 0.07)
#io.imshow(binary)
#sob = binary_dilation(binary, disk(1))
#sob = remove_small_objects(sob, 1000)
######
#io.imshow(sob)
#
##add a column of zeros on both sides, which saves us from having to know the 
##endpoints of the layers a priori.
#imgNew = np.lib.pad(img, ((0,0),(1,1)), 'constant')
#szImgNew = imgNew.shape
#gradImg = np.zeros(szImgNew)
#
#for i in range(0,(int(szImgNew[1]))):
#    #Change to float, otherwise negative gradient values will be reported as 
#    #(value)mod4 (and then converted to floats without telling anyone)
#    #>:-(
#    gradImg[:,i] = np.gradient(([float(ele) for ele in imgNew[:,i]]), 2)
#    
##vertical gradient, scaled so that all values are between 0 and 1
#gradImg = (gradImg - np.amin(gradImg))/(np.amax(gradImg) - np.amin(gradImg))
#fig, ax = plt.subplots()
#io.imshow(gradImg)
#
##Aumento el contraste
#img =exposure.equalize_adapthist(gradImg, clip_limit=0.03)
#fig, ax = plt.subplots()
#io.imshow(img)





#
#edges = feature.canny(img_nr)
#fig, ax = plt.subplots()
#io.imshow(edges)
#
##Obtengo los tensores
#Axx, Axy, Ayy = feature.structure_tensor(img, sigma=5, mode = 'constant', cval=1)
#fig, ax = plt.subplots()
#io.imshow(Ayy)
#
##Elimino ruido
#img_nr = ndimage.median_filter(Ayy, 20)
#fig, ax = plt.subplots()
#io.imshow(img_nr)
#
#img = exposure.rescale_intensity(Ayy, in_range=(-1, 1))
#fig, ax = plt.subplots()
#io.imshow(img)
#
#edges = feature.canny(img)
#fig, ax = plt.subplots()
#io.imshow(edges)
