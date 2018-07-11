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
  self.img = self.menu.botonNuevo.clicked.connect(self.nuevo)
#  
#  
  self.actionNuevo.setShortcut('Ctrl+a')
  self.actionNuevo.triggered.connect(self.nuevo)
#  
  self.menu.botonFusionar.clicked.connect(self.rectificar)
  
#  
#  self.tabs = QTabWidget()
#  inicio = expedienteOCT()
#  self.tabs.addTab(inicio, "Bienvenido")
#  
  self.menuVertical.addWidget(self.menu) 
#  self.panelPrincipal.addWidget(self.tabs)
    
 def rectificar(self):
     plt.close(self.fig)
     print(self.img)
     im = fl.flatening(self.img)
     #perfil = perf.perfilometro(im)
     
#     self.fig, self.ax = plt.subplots()
#     self.ax.imshow(im, cmap = plt.get_cmap('gray'))
     self.fig = plt.figure()
     grid = plt.GridSpec(4, 4)
     main_ax = self.fig.add_subplot(grid[:-1, 0:3])
     y_hist = self.fig.add_subplot(grid[:-1, 3], xticklabels=[], sharey=main_ax)
#  
#  #plt.subplot()
#  #plt.subplot(1,2,1)
     main_ax.imshow(im, cmap = plt.get_cmap('gray'))
#  #plt.subplot(1,2,2)
     y_hist.plot(self.perfil, np.arange(0,len(self.perfil)))
     plt.show()
     
 def nuevo(self):
  #Se captura el nombre del archivo a abrir
  options = QFileDialog.Options()
  options |= QFileDialog.DontUseNativeDialog
  fileName, _ = QFileDialog.getOpenFileName(self,"Nuevo expediente OCT", "","All Files (*);;Python Files (*.py)", options=options)
  if fileName:
      print(fileName)
  ext = fileName.split(".")
  extension = ext[1]
  print(extension)
  if extension == "am":
      carpeta = AmiraReader(fileName).carpeta
      fileName = (carpeta+"scan1.png")
  fname = io.imread(fileName)
  self.perfil = perf.perfilometro(fname)
  
  # Set up the axes with gridspec
  self.fig = plt.figure()
  grid = plt.GridSpec(4, 4)
  main_ax = self.fig.add_subplot(grid[:-1, 0:3])
  y_hist = self.fig.add_subplot(grid[:-1, 3], xticklabels=[], sharey=main_ax)
  
  #plt.subplot()
  #plt.subplot(1,2,1)
  main_ax.imshow(fname)
  #plt.subplot(1,2,2)
  y_hist.plot(self.perfil, np.arange(0,len(self.perfil)))
  plt.show()
  self.img = fileName
     

  
