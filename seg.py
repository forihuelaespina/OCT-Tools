# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 04:09:49 2018

@author: Aleida
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from scipy import misc, ndimage

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

img = misc.imread('D:\Documentos\OCT\imagenes\image3.png')
img = rgb2gray(img)

G=nx.Graph()
G.add_nodes_from(a.reshape(1,a.size))