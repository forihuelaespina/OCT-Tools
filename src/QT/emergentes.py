# -*- coding: utf-8 -*-
"""
Created on Tue May 22 12:45:59 2018

@author: Aleida
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QPushButton, QGraphicsView, QLabel, QAction, QFileDialog, QMenuBar, QMenu
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic
import numpy as np
from reader import AmiraReader 
import matplotlib.pyplot as plt
from skimage import io
import flattening as fl
import perfilometro as perf
import stitch as st
import segment as seg
import time

#Clase del menú de herramientas
class menuHerramientas(QWidget):
 #Método constructor de la clase
 def __init__(self):
  #Iniciar el objeto QMainWindow
  QWidget.__init__(self)
  #Cargar la configuración del archivo .ui en el objeto
  uic.loadUi("QT/menu_casoCompleto.ui", self)

###################################################################################

#Clase heredada de QMainWindow (Constructor de ventanas)
class Ventana(QMainWindow):
 #Método constructor de la clase
 def __init__(self):
  #Iniciar el objeto QMainWindow
  QMainWindow.__init__(self)
  #Cargar la configuración del archivo .ui en el objeto
  uic.loadUi("QT/principal.ui", self)
  
  self.menu = menuHerramientas() 
  self.img = self.menu.paso1.clicked.connect(self.stitching)
#  
#  
  self.actionNuevo.setShortcut('Ctrl+a')
  self.img = self.actionNuevo.triggered.connect(self.stitching)
#  
  self.img = self.menu.paso2.clicked.connect(self.rectificar)
  self.img = self.menu.paso3.clicked.connect(self.segmentar)
  
#  
#  self.tabs = QTabWidget()
#  inicio = expedienteOCT()
#  self.tabs.addTab(inicio, "Bienvenido")
#  
  self.menuVertical.addWidget(self.menu) 
#  self.panelPrincipal.addWidget(self.tabs)
 def segmentar(self):
     plt.close(self.fig)
     im = self.img
     #im = io.imread("D:\Documentos\OCT\imagenes\image5.png")
     im = seg.segmentar(im)
     self.fig = plt.figure()
     io.imshow(im)
     return im
     
 def rectificar(self):
     plt.close('all')
     im = self.img
     io.imshow(im)
     im = fl.flatening(self.img)
     io.imshow(im)
     #im = io.imread("D:\Documentos\OCT\imagenes\image4.png")
     self.perfilometro(im)
     
     print(im)
     #perfil = perf.perfilometro(im)
     self.fig = plt.figure()
     
     return im
     
 def stitching(self):
     image1 = self.nuevo()
     image2 = self.nuevo()
     image3 = st.stitch(image1, image2)
     self.img = image3
     self.fig = plt.figure()
     io.imshow(image1)
     self.fig = plt.figure()
     io.imshow(image2)
     self.fig = plt.figure()
     io.imshow(image3)
     return image3
     #plt.imsave('D:\Documentos\OCT\imagenes\image3.png', image3 , format ='png')
     #self.perfilometro(image3)

 def nuevo(self):
  #Se captura el nombre del archivo a abrir
  options = QFileDialog.Options()
  options |= QFileDialog.DontUseNativeDialog
  fileName, _ = QFileDialog.getOpenFileName(self,"Nuevo expediente OCT", "\imagenes","All Files (*);;Python Files (*.py)", options=options)
  if fileName:
      print(fileName)
  ext = fileName.split(".")
  extension = ext[1]
  print(extension)
  if extension == "am":
      carpeta = AmiraReader(fileName).carpeta
      fileName = (carpeta+"scan1.png")
  fname = io.imread(fileName)
  return fname

 def perfilometro(self, fname):  
  self.perfil = perf.perfilometro(fname)
  
  # Set up the axes with gridspec
#  self.fig = plt.figure()
#  grid = plt.GridSpec(4, 4)
#  main_ax = self.fig.add_subplot(grid[:-1, 0:3])
#  y_hist = self.fig.add_subplot(grid[:-1, 3], xticklabels=[], sharey=main_ax)
#  
#  #plt.subplot()
#  #plt.subplot(1,2,1)
#  main_ax.imshow(fname)
#  #plt.subplot(1,2,2)
#  y_hist.plot(self.perfil, np.arange(0,len(self.perfil)))
#  plt.show()
  
  
     

  
