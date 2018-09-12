# Test.py
import os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.figure import Figure
#from matplotlib.backend_bases import KeyEvent, MouseEvent
from skimage import io

from IOT_Document import IOT_Document
from IOT_GUI_DocumentWindow import IOT_GUI_DocumentWindow
from IOT_OperationEditSegmentation import IOT_OperationEditSegmentation


def _getSemiTransparentColormap(nLayers = 10):
#Creates semi-transparent colormap
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


def myInitFigure():
    #Prepare the matplotlib figure area to render the current OCT scan
    #theFig = Figure(figsize=(10, 8))
    theFig = plt.figure()
    
    #Prepare the grid
    gs = gridspec.GridSpec(1, 2, width_ratios=[5, 1])
    #ax = list() #Create an empty list
    #tmp = self._fig.add_subplot(gs[0]) #The OCT image
    #ax.append(tmp)
    #tmp = plt.subplot(gs[1]) #The perfilometer
    #tmp = self._fig.add_subplot(gs[1]) #The perfilometer
    #ax.append(tmp)
    # theFig.add_subplot(gs[0]) #The OCT image
    # theFig.add_subplot(gs[1]) #The perfilometer
    plt.subplot(gs[0])
    plt.subplot(gs[1])
    
    #make ticklabels invisible
    for i, axs in enumerate(plt.gcf().axes):
        axs.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
        axs.tick_params(labelbottom=False, labelleft=False)
    
    
    plt.show()    
    return theFig

def myPaint(theFig,doc):
#Visualizes the selected scan, its perfilometer and its segmentation
    octScan = doc.getStudy()
    octScanSegmentation = doc.getScanSegmentation()
    

    #theCanvas = FigureCanvas(theFig) #first link the figure to the FigureCanvas 
    #theFig.set_canvas(theCanvas); #Then, inform the figure who is its cointainer
    ax = theFig.axes
    
    #Plot 1: The image
    ax[0].clear()
    if octScan is not None:
        ax[0].imshow(octScan, cmap = plt.get_cmap('gray'))
    
    #Overlay segmentation if available (with a semitransparent colormap)
    if octScanSegmentation is not None:
        mycmap = _getSemiTransparentColormap(nLayers = 10)
        ax[0].imshow(octScanSegmentation, cmap=mycmap)
    
    
    # #Plot 2: The perfilometer
    # perfil = self.perfilometro()  #Updates the perfilometer
    # ax[1].clear()
    # ax[1].plot(perfil, np.arange(0,len(perfil)))

    #Update
    plt.draw()
    #theFig.draw()
    # theFig.canvas.draw()
    # theFig.canvas.flush_events()

    return
    



##MAIN
print("Init testing...")        
print("Loading image.")        
fileName = '../image3.png'
img = io.imread(fileName)

print("Creating document.")        
doc = IOT_Document() #Initialize a document
doc.setName(fileName)
tmp, _ = os.path.split(fileName)
doc.setFolderName(tmp)
doc.setFileName(fileName)
doc.setStudy(img)

print("Plot raw document.")        
#Catch current OCT scan
im = doc.getStudy()
imSegmented = doc.getScanSegmentation()

seg = IOT_OperationEditSegmentation()
imSegmented = seg.initEditSegmentation(im,imSegmented)
doc.setScanSegmentation(imSegmented)


hFig = myInitFigure()
myPaint(hFig,doc) #Plot raw with dummy segmentation

#Apply here some segmentation edit operation

pos=(3,35)
#seg.ROISelect(pos)
#imSegmented2 = seg.ROIChangeLabel(4)
imSegmented2 = seg.ROIChangeLabel(4,pos)
doc.setScanSegmentation(imSegmented2)


myPaint(myInitFigure(),doc) #Plot edited





# _docWindow = IOT_GUI_DocumentWindow()
# _docWindow.setDocument(doc)
# 
# 
# #Get parameters
# x = 3
# y = 3
# pos=(x,y)
# 
# params=list()
# params.append(pos)
# 
# # _docWindow.opEditSegmentation('ROISelect',params)
# # _docWindow.opEditSegmentation('ROIDelete') #Since there is no memory of the selection this shall pass... 
# # _docWindow.opEditSegmentation('ROIDelete',params)
# 
# params.append(4)
# _docWindow.opEditSegmentation('ROIChangeLabel',params)
# 
# #Show the windows
# _docWindow.show()


# from skimage import morphology
# b = np.zeros((6,6), dtype=np.int)
# b[2:4, 2:4] = 1
# b[4, 4] = 1
# b[:2, :3] = 2
# b[0, 5] = 3
# b[5, 4:7] = 7
# print(b)
# #Select COI
# coiIdx = np.nonzero(b==1)
# print(coiIdx)
# #Select ROI
# region_labels,nr_labels = morphology.label(b, neighbors=4,background=0,return_num=True) #Get connected components
# cIdx = region_labels[2,2] #Find component index associated to active ROI
# roiIdx=np.nonzero(region_labels==cIdx)#Retrieve indexes
# print(roiIdx)
# region_labels[roiIdx]
# #...but when the ROI is BG, morphology.label it does not split BG regions
# cIdx = region_labels[2,0] #Find component index associated to active ROI
# roiIdx=np.nonzero(region_labels==cIdx)#Retrieve indexes
# print(roiIdx)
# len(roiIdx[0])
# #...so I need to trick him into believing the background is NOT the backgrond
# #Prepare a dummy binary image where all foreground is grouped under a single label
# theBG = 0
# tmpDummy = b==theBG
# tmpDummy = tmpDummy.astype(np.int) #Now change from boolean to integers
# #...and now operate over the dummy image instead
# region_labels2,nr_labels2 = morphology.label(tmpDummy, neighbors=4,background=0,return_num=True) #Get connected components
# cIdx = region_labels2[2,0] #Find component index associated to active ROI
# roiIdx=np.nonzero(region_labels2==cIdx)#Retrieve indexes
# print(roiIdx)
# print(len(roiIdx[0]))


print("Done.")        
