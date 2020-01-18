# Test.py
import os
import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.figure import Figure
#from matplotlib.backend_bases import KeyEvent, MouseEvent
from skimage import io

import copy #Permits deep copying objects

import octant as oc
#Add paths
if not sys.path[0] == './app':
	sys.path.insert(0, './app')

import app as ocapp
#from app import *


def myInitFigure():
	#Prepare the matplotlib figure area to render the current OCT scan
	#theFig = Figure(figsize=(10, 8))
	theFig = plt.figure(figsize=(12, 10))
	
	#Prepare the grid
	#gs = gridspec.GridSpec(1, 2, width_ratios=[5, 1]) #With perfilometer
	gs = gridspec.GridSpec(1, 1) #Without perfilometer
	plt.subplot(gs[0]) #The OCT image
	#plt.subplot(gs[1]) #The perfilometer
	
	#make ticklabels invisible
	for i, axs in enumerate(plt.gcf().axes):
		axs.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
		axs.tick_params(labelbottom=False, labelleft=False)
	
	#plt.show()
	#theFig.canvas.draw()
	return theFig

def myPaint(theFig,doc):
	#Visualizes the selected scan, its perfilometer and its segmentation
	if type(doc) is oc.data.Document: 
		octScan = doc.getCurrentScan()
		octScanSegmentation = doc.getCurrentScanSegmentation()
	elif type(doc) is oc.data.OCTscan:
		octScan = doc
		octScanSegmentation = oc.data.OCTscanSegmentation(octScan)

	#theCanvas = FigureCanvas(theFig) #first link the figure to the FigureCanvas 
	#theFig.set_canvas(theCanvas); #Then, inform the figure who is its cointainer
	ax = theFig.axes
	
	#Plot 1: The image
	ax[0].clear()
	if octScan is not None:
		ax[0].imshow(octScan.data, cmap = plt.get_cmap('gray'))
	
	#Overlay segmentation if available (with a semitransparent colormap)
	if octScanSegmentation is not None:
		mycmap = ocapp.DocumentWindow._getSemiTransparentColormap(N = 12)
		ax[0].imshow(octScanSegmentation.data, cmap=mycmap)
	
	# #Plot 2: The perfilometer
	# perfil = self.perfilometro()  #Updates the perfilometer
	# ax[1].clear()
	# ax[1].plot(perfil, np.arange(0,len(perfil)))

	#Update
	#plt.draw()
	#theFig.draw()
	theFig.canvas.draw()
	# theFig.canvas.flush_events()

	return theFig
	



##MAIN
def main():

##Test the AmiraReader
#from AmiraReader import AmiraReader
#import random
#r=AmiraReader()
##fileName = 'C:\\Users\\Felipe\\OneDrive\\Documentos\\Research\\OCT\\experimentalData\\Triton\\wetransfer-f56351\\TUV86_20180214_133911_3DOCT00_R_01.am'
#fileName = 'E:\\Felipe\\OneDrive\\Documentos\\Research\\OCT\\experimentalData\\Triton\\wetransfer-f56351\\TUV86_20180214_133911_3DOCT00_R_01.am'
#img = r.readAmiraImage(fileName)
#print(img.shape)
#theScan = IOT_OCTscan(img)
#theSegmentation =IOT_OCTscanSegmentation(theScan)

# imWidth = img.shape[0]
# imHeight = img.shape[1]
# nScans = img.shape[2]
# rnd = list()
# 
# tmpScans = 10
# for x in range(tmpScans):
#   print(x)
#   rnd.append(random.randint(0,nScans))
# rnd.sort() #Watch out! this modifies the list itself. If I want to keep the list, use sorted(rnd) instead
# print(rnd)
# 
# theFig = plt.figure()
# gs = gridspec.GridSpec(int(round(tmpScans/2)), 2, width_ratios=[1, 1])
# for i in range(tmpScans):
#	 plt.subplot(gs[i])
#	 ax = theFig.axes
#	 ax[i].imshow(img[:,:,rnd[i]], cmap = plt.get_cmap('gray'))
# plt.show()	




	print("Init testing...")
	print("Loading image.")
	fileName = '../sampleImages/image3.png'
	img = io.imread(fileName)
	scan = oc.data.OCTscan(img);
	scanSegmentation = oc.data.OCTscanSegmentation(scan);

	print("Creating document.")
	study = oc.data.OCTvolume() #Initialize a document
	study.addScans(scan)
	segmentationVol = oc.data.OCTvolumeSegmentation() #Initialize a document
	segmentationVol.addScanSegmentations(scanSegmentation)
	doc = oc.data.Document() #Initialize a document
	doc.name = fileName
	tmp, _ = os.path.split(fileName)
	doc.folderName = tmp
	doc.fileName= fileName
	doc.study = study
	doc.segmentation = segmentationVol

	#Keep reference image.
	print("Replicating image.")
	doc2 = copy.deepcopy(doc)
	#Flattening
	print("-- Flattening.")
	flt = oc.op.OpScanFlatten()
	flt.addOperand(doc2.getCurrentScan())
	imFlattened = flt.execute()
	doc2.setCurrentScan(imFlattened)
	#Segmentation
	print("-- Segmenting.")
	doc3 = copy.deepcopy(doc2)
	seg = oc.op.OpScanSegment()
	seg.addOperand(doc3.getCurrentScan())
	imSegmented = seg.execute()
	doc3.setCurrentScanSegmentation(imSegmented)
	

	#Load colormap
	print("-- Plotting.")
	appsettings = oc.data.Settings()
	appsettingsfile = '..\\resources\\OCTantApp.config'
	appsettings.read(appsettingsfile)
	cmap=appsettings.retinallayerscolormap
	# hFig = myInitFigure()
	# myPaint(hFig,doc) #Plot raw with dummy segmentation
	#hFig = myPaint(myInitFigure(),doc) #Plot raw
	hFig = myPaint(myInitFigure(),doc2) #Plot flattened
	hFig = myPaint(myInitFigure(),doc3) #Plot segmented


	# pos=(3,35)
	# #seg.ROISelect(pos)
	# #imSegmented2 = seg.ROIChangeLabel(4)
	# imSegmented2 = seg.ROIChangeLabel(4,pos)
	# doc.setScanSegmentation(imSegmented2)
	#
	#
	# myPaint(myInitFigure(),doc) #Plot edited
	#

if __name__ == "__main__":
	#With the new graphical progress bar in method :func:`execute` of
    #class :class:`OpScanSegment`, matplotlib backend was no longer
    #automatically launching inline in the IPython console.
	#Remember to run in the console BEFORE launching this script
	# 1) Activate matplotlib backend (Qt5Agg)
	#%matplotlib
	# 2) Make it work inline, that is within the IPython console
	#%matplotlib inline
	#
	# You might not need it though becuase I left the progress bar
	#disconnected using the var `mode` to 'terminal'.
	
	main()
	print("Done.")		
