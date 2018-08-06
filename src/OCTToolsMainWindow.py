# -*- coding: utf-8 -*-

# File: OCTToolsMainWindow.py
#
# Main window for OCT-Tools.
# 
# Initial code isolated from previous file emergentes.py
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
# 3-Aug-2018: FOE: 
#  * Explicit declaration of attributes
#  * "Nuevo": Ahora captura el caso de que se "cancele" la operación de abrir
#
# 4/5-Aug-2018: FOE:
#   * Isolated minimal solution.
#   * menuHerramientas now rebranded menuTools
#   * Function nuevo now rebranded abrir (because that its what it actually does
#   * Desactivate not programmes menu options
#   * Added menu File->Exit functionality
#   * Revised image rendering algorithm. It is now open from the beginning and
#       automatically updates the perfilometer with every change in the main
#       figure. Also the gridding of the subplots has been improved.
#


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QPushButton, QGraphicsView, QLabel, QAction, QFileDialog, QMenuBar, QMenu
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from skimage import io

from AmiraReader import AmiraReader 
from IOT_operationStitch import IOT_operationStitch
from IOT_operationFlattening import IOT_operationFlattening
from IOT_operationPerfilometer import IOT_operationPerfilometer
from IOT_operationSegmentation import IOT_operationSegmentation
from IOT_operationEditSegmentation import IOT_operationEditSegmentation

#import segment as seg
#import time



###################################################################################

#Clase del menú de herramientas (actions sequence in the main window)
class menuTools(QWidget):
 #Class constructor
 def __init__(self):
  #Iniciar el objeto QMainWindow
  QWidget.__init__(self)
  #Cargar la configuración del archivo .ui en el objeto
  uic.loadUi("GUI/menuTools.ui", self)




###################################################################################


#Clase heredada de QMainWindow (Constructor de ventanas)
class OCTToolsMainWindow(QMainWindow):
 
    #Private class attributes shared by all instances

    #Class constructor
    def __init__(self):
        #Call superclass constructor
        QMainWindow.__init__(self)
        #Cargar la configuración del archivo .ui en el objeto
        uic.loadUi("GUI/OCTToolsMainWindow.ui", self)
            #The .ui resource file contains the menu and status bars
        self.move(50,50)
    
        #Initialize private attributes unique to this instance
        self._img = None #The image being processed
        self._imgSegmented = None #The image segmentation
        self._fig = None #The image rendering plot
        self._perfil = None #The perfilometer image
        self._menuTools = menuTools() #Buttons of actions sequence in the main window
        
        
        #Add functionality to buttons and menu options
        #self.actionNuevo.setShortcut('Ctrl+a')
        self.actionAbrir.setShortcut('Ctrl+o')
        self._img = self.actionAbrir.triggered.connect(self.abrir)
        self.actionSalir.triggered.connect(self.close)
        
        self._img = self._menuTools.paso0.clicked.connect(self.abrir)
        self._img = self._menuTools.paso1.clicked.connect(self.stitching)
        self._img = self._menuTools.paso2.clicked.connect(self.rectificar)
        self._img = self._menuTools.paso3.clicked.connect(self.segmentar)
        self._img = self._menuTools.paso4.clicked.connect(self.editSegmentar)
        
        self._menuTools.paso0.setEnabled(True)
        self._menuTools.paso1.setEnabled(False)
        self._menuTools.paso2.setEnabled(False)
        self._menuTools.paso3.setEnabled(False)
        self._menuTools.paso4.setEnabled(False)
        
        
        #  
        #  self.tabs = QTabWidget()
        #  inicio = expedienteOCT()
        #  self.tabs.addTab(inicio, "Bienvenido")
        #  
        self.menuVertical.addWidget(self._menuTools) 
        #  self.panelPrincipal.addWidget(self.tabs)
    
        #Prepare the plotting area
        self._preparePlottingWindow()


    #Private methods
    def _getImageFilename(self):
        #Chooses a new image to work on.
        #The image can be in Amira o other image format.
        #If the operation is cancelled, then an empty string is returned
        #Se captura el nombre del archivo a abrir
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Nuevo expediente OCT", "\imagenes","All Files (*);;Amira Files (*.am)", options=options)
        print(fileName)
        return fileName
    
 

    def _openImageFile(self,fileName):
        #Open a new image file. The file must exist!
        ext = fileName.split(".")
        extension = ext[-1] #Gets the last piece (that's the extension)
        #print(extension)
        if extension == "am":
            #carpeta = AmiraReader(fileName).carpeta
            #fileName = (carpeta+"scan1.png") #THIS IS A BUG!!!! We should be reading the AMIRA file!
            #self._img = np.zeros(0);
            amr = AmiraReader()
            self._img = amr.readAmiraImage(fileName)
        else:
            self._img = io.imread(fileName)



    def _preparePlottingWindow(self):
        #Close the previous figure
        plt.close('all')
        
        #Open the new figure
        self._fig = plt.figure()
        #Prepare the grid
        gs = gridspec.GridSpec(1, 2, width_ratios=[5, 1])
        ax = list()
        tmp = plt.subplot(gs[0])
        ax.append(tmp)
        tmp = plt.subplot(gs[1])
        ax.append(tmp)
        
        
        #make ticklabels invisible
        for i, axs in enumerate(self._fig.axes):
            axs.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
            axs.tick_params(labelbottom=False, labelleft=False)

        #Render
        plt.show()
        
        return ax


    def _getSemiTransparentColormap(self, nLayers = 10):
        N=nLayers
        base = plt.cm.get_cmap('jet')
        color_list = base(np.linspace(0, 1, N+1))
        cmap_name = base.name + str(N+1)
        mycmap=base.from_list(cmap_name, color_list, N+1)
        mycmap._init()
        #mycmap._lut[:,-1] = np.linspace(0, 0.8, N+4)
        tmp = [] #Create an empty array
        tmp.append(0)
        tmp.extend(np.ones(N+3))
        mycmap._lut[:,-1] = tmp #Transparent background, but fully visible layers
        return mycmap


    def _render(self):
    #Visualizes the main image and its perfilometer
        
        #The following is a bug. It should be capture "on the fly" and
        #clearing axes rather than reset, but I cannot make it work :(
        ax = self._preparePlottingWindow()
        #ax = self._fig.axes
       
        #Plot 1: The image
        ax[0].clear()
        ax[0].imshow(self._img, cmap = plt.get_cmap('gray'))
        
        #Overlay segmentation if available (with a semitransparent colormap)
        if self._imgSegmented is not None:
            mycmap = self._getSemiTransparentColormap(nLayers = 10)
            ax[0].imshow(self._imgSegmented, cmap=mycmap)
        
        
        #Plot 2: The perfilometer
        self._perfil = self.perfilometro()  #Updates the perfilometer
        ax[1].clear()
        ax[1].plot(self._perfil, np.arange(0,len(self._perfil)))

        #plt.show()



    def _generateDummySegmentation(self,height,width,nLayers = 10):
        print("OCT-Tools: IOT_operationEditSegmentation: Generating dummy segmentation.")
        #Define a default output (simple 10 lines (one per layers))
        imageSegmented = np.zeros((height,width), dtype = np.uint8 )
        stepHeight = round(height/(nLayers+1))
        for ii in range(1,nLayers):
            kk = ii*stepHeight
            imageSegmented[kk-2:kk+2,:] = ii #5 pixels thick
                #Watch out! Lines thinner than 3-5 pixels thick may not
                #be visible when rendered on the screen (depending on
                #the resolution).
            #print(kk, ii)
        return imageSegmented


    

    #Public methods
    def abrir(self):
        #Open an image to work on.
        fileName = self._getImageFilename()
        if fileName: #Empty strings evaluate to false in Python;
                     #If fileName is empty, this skips the attempt to open the file
            print("OCT-Tools: OCTToolsMainWindow: Opening file ", fileName)
            self._openImageFile(fileName)
        self._render()

        self._menuTools.paso1.setEnabled(True)
        self._menuTools.paso2.setEnabled(True)
        self._menuTools.paso3.setEnabled(True)
        self._menuTools.paso4.setEnabled(True)

        return self._img


    def stitching(self):
        #Selects a second image and applies the stitching step
        #self.abrir() overwrites self._img so I need to make a copy of the current self._img
        image1 = self._img
        image2 = self.abrir()
        st = IOT_operationStitch()
        image3 = st.stitch(image1, image2)
        self._img = image3
        self._render()
        return image3
    
     
     
    def rectificar(self):
        #Applies the flattening step
        fl = IOT_operationFlattening()
        im = fl.flattening(self._img)
        self._img = im
        self._render()
        return im
        
     
     
    def perfilometro(self):
        #Renders the perfilometer
        perf = IOT_operationPerfilometer()
        self._perfil = perf.perfilometry(self._img)
        return self._perfil
     
        
    def segmentar(self):
        #Applies the segmentation step
        seg = IOT_operationSegmentation()
        imSegmented = seg.segmentar(self._img)
        self._imgSegmented = imSegmented
        self._render()
        return imSegmented
        
        
    def editSegmentar(self):
        #Starts/Stops manual segmentation step
        if self._imgSegmented is None:
            tmpImgSize = self._img.shape
            self._imgSegmented = self._generateDummySegmentation(tmpImgSize[0],tmpImgSize[1])

        seg = IOT_operationEditSegmentation()
            
        tmp = self._menuTools.paso4.text()
        if tmp.find("Start")==-1:
            #If "Start" is no found, then it is currently segmenting
            #Stop segmenting
            #imSegmented = seg.stopEditSegmentation()
            self._menuTools.paso4.setText("4. Start manual edit segmentation")
            
        else:
            #Start segmenting
            #imSegmented = seg.startEditSegmentation(self._img,self._imgSegmented)
            self._menuTools.paso4.setText("4. Stop manual edit segmentation")
        
        #self._imgSegmented = imSegmented
        self._render()
        return self._imgSegmented
                                                
  
