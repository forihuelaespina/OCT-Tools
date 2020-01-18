"""
-*- coding: utf-8 -*-

File: OpSegmentScan.py

Class OpSegmentScan

A class for automatic segmentation of retinal layers from an OCT scan

Initial code isolated from previous file segment.py


:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| Feb-2018    | AACC   | - Class created.                                     |
+-------------+--------+------------------------------------------------------+
| 5-Aug-2018  | FOE    | - Isolated minimal solution.                         |
|             |        | - Encapsulated in class.                             |
+-------------+--------+------------------------------------------------------+
| 22-Aug-2018 | FOE    | - Rebranded to capital "O" in operation;             |
|             |        |   IOT_Operation                                      |
|             |        | - Improved verbosity; now using class name           |
+-------------+--------+------------------------------------------------------+
| 23-Sep-2018 | FOE    | - Updated comments and added Sphinx                  |
|             |        |   documentation to the class                         |
+-------------+--------+------------------------------------------------------+
| 17-Oct-2018 | FOE    | - Adapted to IOT_Operation becoming abstract and new |
|             |        |   capabilities. Added method .execute, integration of|
|             |        |   operands, given operation name, deprecated method  |
|             |        |   segmentar.                                         |
+-------------+--------+------------------------------------------------------+
| 18-Oct-2018 | FOE    | - Now using the classes class:`IOT_OCTscan` and      |
|             |        |   :class:`IOT_OCTscanSegmentation`.                  |
+-------------+--------+------------------------------------------------------+
|  1-Dec-2018 | FOE    | - Adapted to new signature of inherited execute()    |
|             |        |   method to accept parameters.                       |
+-------------+--------+------------------------------------------------------+
| 13-Dec-2018 | FOE    | - Updated deprecation package to "deprecation" due   |
|             |        |   compilation problems with package "deprecated".    |
+-------------+--------+------------------------------------------------------+
| 27-Feb-2019 | FOE    | - Adapted to new package OCTant structure.           |
|             |        |   Class rebranded Operation. The prefix              |
|             |        |   IOT is drop and it is now part of the package.     |
|             |        |   Also, the subprefix Operation is reduced to Op     |
|             |        |   only, the class name extended with the main        |
|             |        |   operand type.                                      |
|             |        | - Importing statements for classes within this	      |
|             |        |   package are now made through package instead       |
|             |        |   of one class at time.                              |
|             |        | - Previously deprecated method segmentar have now    |
|             |        |   been fully removed.                                |
+-------------+--------+------------------------------------------------------+
|  3-Feb-2019 | FOE    | - Debugging of errors left during transition to new  |
|             |        |   package OCTant structure; wrong imports and        |
|             |        |   unupdated classes names.                           |
+-------------+--------+------------------------------------------------------+
| 19-May-2019 | FOE    | - Bug fixed. Method execute was not testing for      |
|             |        |   number of operands correctly.                      |
+-------------+--------+------------------------------------------------------+
| 24-Jun-2019 | FOE    | - Attempted to improve the performance of the        |
|             |        |   segmentation algorithm by substituting the initial |
|             |        |   noise removal step from the current morphological  |
|             |        |   closing of opening to the more specialized         |
|             |        |   **non-linear anisotropic diffusion filter** as     |
|             |        |   first described by [P. Perona and J. Malik, IEEE   |
|             |        |   Trans. Pattern Anal. Mach. Intel. 12, 629 (1990)]  |
|             |        |   and later reported for OCT by [Wang, RK (2005)     |
|             |        |   Proc. SPIE 5690:380-385]. This is still NOT        |
|             |        |   working.                                           |
+-------------+--------+------------------------------------------------------+
|4/6-Jul-2019 | FOE    | - The non-linear anisotropic diffusion filter is now |
|             |        |   working.                                           |
+-------------+--------+------------------------------------------------------+
| 11-Aug-2019 | FOE    | - Comments corrections during Sphyinx compilation.   |
|             |        | - Removal of debugging code, e.g. intermediate       |
|             |        |   figure plotting, display messages, etc for the     |
|             |        |   integration of the diffusion filter in the main    |
|             |        |   GUI. Also, added progress bar.                     |
+-------------+--------+------------------------------------------------------+
|  3-Nov-2019 | FOE    | - Background mask is now extracted.                  |
+-------------+--------+------------------------------------------------------+


.. seealso:: None
.. note:: None
.. todo:: None


.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Arlem Aleida Castillo Avila <acastillo@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""

## Import
import os
import warnings
#from deprecated import deprecated
import deprecation

import math
import numpy as np
from scipy import signal, ndimage #Used for 2D convolution
from skimage import feature, color
from functools import reduce
import cv2 #That's OpenCV
#import matlab.engine
import matplotlib.pyplot as plt

from PyQt5.QtCore import Qt #Imports constants
from PyQt5.QtWidgets import QProgressDialog
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5

#from version import __version__
from octant.data import OCTscan, OCTscanSegmentation, RetinalLayers
from octant.util import segmentationUtils
from .Operation import Operation



class OpScanSegment(Operation):
	#Sphinx documentation
	"""A class for automatic segmentation of retinal layers from an OCT scan.
	
	A class for automatic segmentation of retinal layers from an OCT scan.
	
	The operation represented by this class generates a new
	:class:`octant.data.OCTscanSegmentation` for a :class:`octant.data.OCTscan`.

	.. seealso:: None
	.. note:: None
	.. todo:: None
		
	"""

	#Private class attributes shared by all instances
	
	#Class constructor
	def __init__(self):
		#Call superclass constructor
		super().__init__()

		#Set the operation name
		self.name = "Segmentation"
		
		#Initialize private attributes unique to this instance
		#self._imgin = np.zeros(shape = (0,0,0), dtype = np.uint8 ); #Input image
		#self._imgout = np.zeros(shape = (0,0,0), dtype = np.uint8 ); #The segmented image
	
	
	#Private methods
	@staticmethod
	def anisotropicDiffusionFilter(img):
		"""
		Non-linear anisotropic diffusion filtering
		#Original algorithm in [Perona and Malik, (1990) TPAMI 12(7):629-639]
		#Parameters according to [WangRK2005, Proc. of SPIE 5690:380-385]
		
		:param img: ndarray. The image to be filtered
		:return: the image filtered
		:rtype: ndarray
		"""
		sigma=1
		GaussMask = OpScanSegment.generateGaussianMask2D(shape=(3,3),sigma = sigma)
		#print(GaussMask)
		m=8
		l=10 #contrast parameter; structures with s > λ are regarded as edges,
			 #while with s < λ are assumed to belong to the interior of a region
			 #[Wang2005] uses l=5 for the porcine trachea, but for us that value
			 #does not produce as good results as l=10.
		timestep = 0.24
		niterations = 10 #diffusion time (iteration)
		Cm = 3.31488

		img2 = img #Initialize image
		
		#Get rid of the "large" noise with morphological closing after opening
		morphkernel = np.ones((5,5),np.uint8)
		#img2 = cv2.morphologyEx(img2, cv2.MORPH_OPEN, morphkernel)
		#img2 = cv2.morphologyEx(img2, cv2.MORPH_CLOSE, morphkernel)
		
		if np.max(img2)<=1:
			#Scale parameters
			#m=m/255
			l = l/255
			#Cm = Cm/255
		for tau in range(1,niterations):
#			#Progress bar
#			if progress.wasCanceled():
#				break
#			progress.setValue(round(100*tau/niterations))
			
			#Morphological removal of noise
			#Note that this is NOT part of the original diffusion filter
			#but the results are clearly enhanced!.
			img2 = cv2.morphologyEx(img2, cv2.MORPH_OPEN, morphkernel)
			img2 = cv2.morphologyEx(img2, cv2.MORPH_CLOSE, morphkernel)
			
			#Estimate gradient vector at sigma scale
			gradI=np.gradient(img2)
			tmpGradI = np.add.reduce(gradI) #For illustrations purposes only
			
			#Regularize gradient
			#gradientScaleSigma=math.sqrt(2*(tau*timestep))
			gradientScaleSigma=math.sqrt(2*(tau))
			GaussMask = OpScanSegment.generateGaussianMask2D(shape=(7,7),sigma = gradientScaleSigma)
			#Individually convolve the Gaussian filter with each gradient component
			#s = signal.convolve2d(gradI, GaussMask, boundary='symm', mode='same')
			s=[None] * len(gradI) #Preallocate list
			for dim in range(0,len(gradI)):
				s[dim] = signal.convolve2d(gradI[dim], GaussMask, boundary='symm', mode='same')
			s = np.linalg.norm(s,ord = 2, axis =0) #Norm of the gradient.

			#Calculate diffusivity
			tmp = ((s/l)**m)
			tmp = np.divide(-Cm,tmp, out= np.zeros(tmp.shape) , where=tmp!=0) #Avoid division by 0 when estimating diffusivity
			#D = 1-np.exp(-Cm/((s/l)**m)) #diffusivity or conduction coefficient
			D = 1-np.exp(tmp) #diffusivity or conduction coefficient
			
			#Update image
			img2 = img2+ OpScanSegment.divergence(np.multiply(D,gradI)) #Update the image
				#Reminder> The divergence of gradient is the Laplacian operator
				#See: https://math.stackexchange.com/questions/690493/what-is-divergence-in-image-processing
		return img2

	@staticmethod
	def divergence(f):
		#"""Compute the divergence of n-D SCALAR field `f`."""
		#See: https://stackoverflow.com/questions/11435809/compute-divergence-of-vector-field-using-python
		#return reduce(np.add,np.gradient(f))
		"""
		Computes the divergence of the VECTOR field f, corresponding to dFx/dx + dFy/dy + ...
		:param f: List of ndarrays, where every item of the list is one dimension of the vector field
		:return: Single ndarray of the same shape as each of the items in f, which corresponds to a scalar field
		"""
		num_dims = len(f)
		return np.ufunc.reduce(np.add, [np.gradient(f[i], axis=i) for i in range(num_dims)])

	@staticmethod
	def generateGaussianMask2D(shape=(3,3),sigma=0.5):
		"""
		Generates a 2D gaussian mask
		It should give the same result as MATLAB's
		fspecial('gaussian',[shape],[sigma])
		See: https://stackoverflow.com/questions/17190649/how-to-obtain-a-gaussian-filter-in-python
		"""
		m,n = [(ss-1.)/2. for ss in shape]
		y,x = np.ogrid[-m:m+1,-n:n+1]
		h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
		h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
		sumh = h.sum()
		if sumh != 0:
			 h /= sumh
		return h
	
	#Public methods
	def execute(self,*args,**kwargs):
		"""Executes the operation on the :py:attr:`operands`.
		
		Executes the operation on the :py:attr:`operands` and stores the outcome
		in :py:attr:`result`. Preload operands using method
		:func:`addOperand()`.
		
		:returns: Result of executing the operation.
		:rtype: :class:`octant.data.OCTscanSegmentation`
		"""
		#Ensure the operand has been set.
		if (len(self.operands) <1):
			warnMsg = self.getClassName() + ':execute: Operand not set.'
			warnings.warn(warnMsg,SyntaxWarning)
			return None
		
		#Establish mode of operation
		#NOT WORKING YET... :(
		#Now, it always detect:
		#	Terminal for the stdin
		#	GUI for the stdout
		mode = 'terminal'
		if os.isatty(0):
			mode = 'gui'
		print('Executing segmentation in mode ' + mode + '.')
		
		if (mode == 'gui'):
			MainWindow = QtWidgets.QWidget()
			progress = QProgressDialog("Segmentation...", "Cancel", 0, 100, MainWindow)
			progress.setWindowModality(Qt.WindowModal)
			progress.setAutoReset(True)
			progress.setAutoClose(True)
			progress.setMinimum(0)
			progress.setMaximum(100)
			progress.setWindowTitle("Automatic segmentation")
			progress.setLabelText('Progress:')
			progress.setMinimumDuration(0)
			progress.resize(500,100)
			progress.forceShow()
			progress.setValue(0)
		
		
		imgin = self.operands[0]
		if type(imgin) is OCTscan:
			imgin=imgin.data

		#Define a default output
		segmentedImage = np.zeros(shape = (0,0,0), dtype = np.uint8 );
		
		
		#Check whether the image is in RGB (ndim=3) or in grayscale (ndim=2)
		#and convert to grayscale if necessary
		#img = cv2.cvtColor(self._imgin, cv2.COLOR_BGR2GRAY)
		if imgin.ndim == 2:
			#Dimensions are only width and height. The image is already in grayscale.
			img=imgin
		elif imgin.ndim == 3:
			#Image is in RGB. Convert.
			img=color.rgb2gray(imgin);
		else: #Unexpected case. Return warning
			print(self.getClassName(),": Unexpected image shape.")
			return None
		
		
		## Algoritmo 1: Basado en el código de Matlab CASeReL
		# https://pangyuteng.github.io/caserel/
		#
		# Llama externamente a retSegment.exe
		#
		# Requiere de Matlab Runtime environment 
		
		
		#  #Remove external noise from image
		#  img = segmentationUtils.ejecuta_close(img,4,4) #Clausura
		#  #segmentationUtils.mostrar_imagen(img)
		#  
		#  #Generate temporal intermediate image file to be processed externally
		#  tmpFilename = "paso2.tiff"
		#  cv2.imwrite(tmpFilename, img)
		#  
		#  #Rely externally on the matlab algorithm for segmentation
		# # eng = matlab.engine.start_matlab()
		# # eng.retSegment(img)
		#  #segmentationUtils.mostrar_imagen(img)
		#  
		#  #Delete the intermediate image file
		#  segmentationUtils.elimina_imagen(tmpFilename)
		
		
		## Algoritmo 3 Felipe
		
		#Step 1) Non-linear anisotropic diffusion filtering
		#Original algorithm in [Perona and Malik, (1990) TPAMI 12(7):629-639]
		#Parameters according to [WangRK2005, Proc. of SPIE 5690:380-385]
		if (mode == 'gui'):
			progress.setLabelText('Applying diffusion filter:')
		img2 = OpScanSegment.anisotropicDiffusionFilter(img)
			#The output of the anisotropic filter is a float64 2D array
			#with values between [0 1] (although note that IT MAY not
			#include the segment boundaries 0 and/or 1, so for instance
			#while testing I was getting [0,0.85]). Anyway, in this
			#range, anything below 1% (~0.099) is background, and the
			#rest is tissue.
		if (mode == 'gui'):
			progress.setValue(100)
			if progress.wasCanceled():
				return img #Return the original image


		#print('Diffusion Filter output range: ['+str(np.amin(img2))+','+str(np.amax(img2))+']')

		#Detect background mask
		BGmask = np.where(img2 <= 0.099,True,False)
			#See above for threshold 0.099 on anisotropic diffusion filter
			#output.
			#Note that there might be "background" pixels
			#found somewhere within the tissue. This is VERY LIKELY fluid!
			#Note as well that the lower part also include a bit of the
			#choroid with this threshold.
			#Finally, the top part should be the vitreous.
		#print(BGmask)
		#Just to see the mask
		#img2 = np.where(BGmask,10,OCTscanSegmentation._BACKGROUND)

#		#Plot histogram of image
#		binSize = 0.01
#		bins=np.arange(0,np.amax(img2)+binSize,binSize)
#		hist = np.histogram(img2, bins=bins)
#		hfig, ax = plt.subplots(1, 1)
#		ax.hist(img2.flatten(),bins)
#		ax.set_yscale('log')
#		hfig.show()

		#PENDING
		#Assign intratissue BG pixels to fluid.
		


		#Normalize
		img2 = np.floor(255*(img2/np.amax(img2))).astype(int)
		img2 = np.where(BGmask==True,OCTscanSegmentation._BACKGROUND,img2)
		
		#Assign integers to nRetinalLayers
		r = RetinalLayers();
		nRetinalLayers = r.getLayerIndex('RPE');
			#Note that I'm not counting for choroid or fluid.
		#I can't use pixel intensity alone here for segmenting as several
		#(separated) layers exhibit similar reflectivity, so segmentation
		#criteria has to be a mix of location and intensity.
		
		#Estimate upper and lower boundary by checking first and last
		#non-BG pixels per column
		#UNFINISHED.
		#upperBoundary = 
		

		#[uVals,uIdx,uInv,uCounts] = np.unique(img2, \
		#						return_index=True, \
		#						return_inverse=True, \
		#						return_counts=True)
		#print(len(uVals))

#		## Algoritmo 2: Arlem
#		img2 = img
#		print(np.amax(img2))
#		tmp=np.reshape(img2,(np.size(img2),1))
#		print(type(tmp))
#		print(np.size(tmp))
#		print(np.amax(tmp))
#		
#		
#		hfig, ax = plt.subplots(1, 1)
#		ax.hist(tmp,255)
#		hfig.show()
#
#		#Elimina ruido
#		img = segmentationUtils.ejecuta_close(img,4,4)
#		
#		#Amplifica capas
#		img = segmentationUtils.ejecuta_dilate(img,5,20,1)
#		
#		#Tensor
#		Axx, Axy, Ayy = feature.structure_tensor(img)
#		
#		#Elimina mas ruido
#		Ayy = segmentationUtils.ejecuta_close(Ayy,6,1)
#		
#		#Resalta las capas que sean mayores a la media
#		Ayy = segmentationUtils.resalta_bordes(Ayy,True,0)
#		
#		#Elimina aun mas ruido
#		Ayy = segmentationUtils.ejecuta_open(Ayy,1,1)
#		
#		#Binarizacion
#		binary = segmentationUtils.ejecuta_OTSU(Ayy)
#		
#		#elimina ruido del posible borde superior
#		binary = segmentationUtils.ejecuta_elimina_ruido_extremos(True,0,0,binary)
#		
#		#elimina ruido del posible borde inferior
#		binary = segmentationUtils.ejecuta_elimina_ruido_extremos(False,0,0,binary)
#		
#		#obtiene bordes exteriores
#		arraySuperior, arrayInferior = segmentationUtils.obten_bordes_externos(binary)
#		
#		#elimina ruido a la imagen original
#		img2 = segmentationUtils.elimina_desde_arreglos(img2, arraySuperior, arrayInferior)
#		img2 = segmentationUtils.ejecuta_close(img2,2,1)
#		img2 = feature.canny(img2,sigma = 2.5)
#		img2 = segmentationUtils.elimina_ruido_canny(img2,1)

		#Hide and close progress bar.
		if (mode == 'gui'):
			progress.hide()
		
		#if isinstance(imgin,(OCTscan,)):
		if type(imgin) is OCTscan:
			self.result=OCTscanSegmentation(imgin)
		else:
			self.result=OCTscanSegmentation(OCTscan(imgin))
		self.result.data = img2

		return self.result




#	#@deprecated(version='0.2', reason="Deprecated. Use method execute() instead.")
#	@deprecation.deprecated(deprecated_in="0.2", removed_in="0.3",
#						current_version=__version__,
#						details="Use method execute() instead.")
#	def segmentar(self,image):
#		#Encapsulate the image as an OCTscan
#		tmp=OCTscan(image)
#		self.clear()
#		self.addOperand(tmp)
#		#Execute
#		self.execute()
#		return None



