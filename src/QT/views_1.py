import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QPushButton, QGraphicsView, QLabel, QAction, QFileDialog, QMenuBar, QMenu
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic
from reader import AmiraReader 

class panelDatosComplementarios(QWidget):
 #Método constructor de la clase
 def __init__(self):
  #Iniciar el objeto QMainWindow
  QWidget.__init__(self)
  #Cargar la configuración del archivo .ui en el objeto
  #uic.loadUi("QT/principal_imagenes.ui", self)

  self.referenciaL = QWidget()
  self.histogramaL = QVBoxLayout()
  
 def setReferencia(self, img):
# Create widget
  label = QLabel(self)
  pixmap = QPixmap(img)
  label.setPixmap(pixmap)
  self.resize(pixmap.width(),pixmap.height())
    
  self.show()
  
  
class panelScan(QWidget):
 #Método constructor de la clase
 def __init__(self):
  #Iniciar el objeto QMainWindow
  QWidget.__init__(self)
  #Cargar la configuración del archivo .ui en el objeto
  #uic.loadUi("QT/principal_imagenes.ui", self)

  self.tabScans = QTabWidget()
  bscans = QWidget()
  cscans = QWidget()
  self.tabScans.addTab(bscans, "B-scans")
  self.tabScans.addTab(cscans, "C-scans")
  

class canvasOCT(QWidget):
 #Método constructor de la clase
 def __init__(self):
  #Iniciar el objeto QMainWindow
  QWidget.__init__(self)
  #Cargar la configuración del archivo .ui en el objeto
 
  
  
 def imagen(self, img):  
  # Create widget
  label = QLabel(self)
  pixmap = QPixmap(img)
  label.setPixmap(pixmap)
  self.canvas.resize(pixmap.width(),pixmap.height())
    
  self.show()
  
class imagenesOCT(QTabWidget):
 def __init__(self):
  QTabWidget.__init__(self)
  
  self.setTabPosition(2)
  
 def setimagen(self, img):
  self.canvas = canvasOCT()
  self.canvas.imagen(img)
  self.addTab(self.canvas, "Pr")

class panelOCT(QWidget):
 #Método constructor de la clase
 def __init__(self):
  #Iniciar el objeto QMainWindow
  QWidget.__init__(self)
  #Cargar la configuración del archivo .ui en el objeto
  uic.loadUi("QT/principal_imagenes.ui", self)
  
  self.imagenesOCT = imagenesOCT()
  self.scan = panelScan()
  self.scanL.addWidget(self.scan.tabScans)
  
 def setimagen(self, img):
  self.imagenesOCT.setimagen(img)
  self.canvasL.addWidget(self.imagenesOCT) 
 

class expedienteOCT(QWidget):
 #Método constructor de la clase
 def __init__(self):
  #Iniciar el objeto QMainWindow
  QWidget.__init__(self)
  #Cargar la configuración del archivo .ui en el objeto
  uic.loadUi("QT/principal.ui", self)
  
  self.panel = panelOCT()
  self.datosC = panelDatosComplementarios()
  
 def setimagen(self, img):
  self.panel.setimagen(img)
  self.expedienteI.addWidget(self.panel)
 
 def setDatosC(self, ref):
  self.datosC.setReferencia(ref)
  self.expedienteG.addWidget(self.datosC)

class menuHerramientas(QWidget):
 #Método constructor de la clase
 def __init__(self):
  #Iniciar el objeto QMainWindow
  QWidget.__init__(self)
  #Cargar la configuración del archivo .ui en el objeto
  uic.loadUi("QT/menus.ui", self)
  
  
 def nuevo(self):
#Se captura el nombre del archivo a abrir
  options = QFileDialog.Options()
  options |= QFileDialog.DontUseNativeDialog
  fileName, _ = QFileDialog.getOpenFileName(self,"Nuevo expediente OCT", "","All Files (*);;Python Files (*.py)", options=options)
  if fileName:
   print(fileName)
  return fileName
  
 def agregarReferencia(self):
#Se captura el nombre del archivo a abrir
  options = QFileDialog.Options()
  options |= QFileDialog.DontUseNativeDialog
  fileName, _ = QFileDialog.getOpenFileName(self,"Agregar Referencia", "","All Files (*);;Python Files (*.py)", options=options)
  if fileName:
   print(fileName)
  return fileName


#Clase heredada de QMainWindow (Constructor de ventanas)
class Ventana(QMainWindow):
 #Método constructor de la clase
 def __init__(self):
  #Iniciar el objeto QMainWindow
  QMainWindow.__init__(self)
  #Cargar la configuración del archivo .ui en el objeto
  uic.loadUi("QT/mainwindow.ui", self)
  
  self.menu = menuHerramientas() 
  self.menu.botonNuevo.clicked.connect(self.nuevo)
  
  
  self.actionNuevo.setShortcut('Ctrl+a')
  self.actionNuevo.triggered.connect(self.nuevo)
  
  self.actionAgregar_referencia_ocular.setShortcut('Ctrl+r')
  self.actionAgregar_referencia_ocular.triggered.connect(self.agregarReferencia)
  
  self.tabs = QTabWidget()
  inicio = expedienteOCT()
  self.tabs.addTab(inicio, "Bienvenido")
  
  self.panelDerecho.addWidget(self.menu)  
  self.panelPrincipal.addWidget(self.tabs)
 
 def nuevo(self):
  fileName = self.menu.nuevo()
  #fname = open(fileName)
  #refName = self.menu.agregarReferencia()
  #carpeta = AmiraReader(fileName).carpeta
  tab = expedienteOCT()
  tab.setimagen(fileName)
  #tab.setDatosC(refName)
  self.tabs.addTab(tab, "Sin título "+ str(self.tabs.count())) 
  self.tabs.setCurrentWidget(tab)
 
 def agregarReferencia(self):
    refName = self.menu.agregarReferencia()
    tab = self.tabs.currentWidget()
    tab.setDatosC(refName)
    self.tabs.setCurrentWidget(tab)
    
     

  
