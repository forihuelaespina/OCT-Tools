# -*- coding: utf-8 -*-
"""
Created on Tue May 22 13:17:41 2018

@author: Aleida
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QPushButton, QGraphicsView, QLabel, QAction, QFileDialog, QMenuBar, QMenu
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic

class menuHerramientas(QWidget):
 #Método constructor de la clase
 def __init__(self):
  #Iniciar el objeto QMainWindow
  QWidget.__init__(self)
  #Cargar la configuración del archivo .ui en el objeto
  uic.loadUi("QT/menus.ui", self)