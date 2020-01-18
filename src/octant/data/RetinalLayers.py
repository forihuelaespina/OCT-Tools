"""
-*- coding: utf-8 -*-

File: RetinalLayers.py

Class RetinalLayers

A collection of constants for identifying retinal layers.

Initial code isolated from previous file segment.py


:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 26-Aug-2018 | FOE    | - Class created.                                     |
+-------------+--------+------------------------------------------------------+
| 23-Sep-2018 | FOE    | - Updated comments and added Sphinx                  |
|             |        |   documentation to the class                         |
+-------------+--------+------------------------------------------------------+
| 27-Feb-2019 | FOE    | - Adapted to new package OCTant structure.           |
|             |        |   Class rebranded RetinalLayers. The prefix          |
|             |        |   IOT is drop and it is now part of the package.     |
|             |        | - Importing statements for classes within this       |
|             |        |   package are now made through package instead       |
|             |        |   of one class at time.                              |
+-------------+--------+------------------------------------------------------+
| 15-Jun-2018 | FOE    | - Added codification for fluid for pathological      |
|             |        |   images.                                            |
+-------------+--------+------------------------------------------------------+
|  3-Nov-2019 | FOE    | - Added some comments about the layers.              |
+-------------+--------+------------------------------------------------------+



.. seealso:: None
.. note:: None
.. todo:: None


.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""


## Import



## Class definition
class RetinalLayers(object):
	#Sphinx documentation
	"""A collection of constants for identifying retinal layers.
	
	A collection of constants for identifying retinal layers.
	
	It is basically a dictionary of pairs key:value
	
	
	The following retinal layers are considered:
	
	* Inner Limiting Membrane (ILM)
	* Nerve Fiber Layer (NFL)
	* Ganglion Cell Layer (GCL)
	* Inner Plexiform Layer (IPL)
	* Inner Nuclear Layer (INL)
	* Outer Plexiform Layer (OPL)
	* Outner Nuclear Layer (ONL)
	* External Limiting Membrane (ELM)
	* Rods and Cones layers (RCL)
	* RetinalPigmentEpithelium (RPE)
	
	Also the non-retinal layer is indexed:
	
	* Choroid (CHR)
	
	For pathological conditions, the following is also encoded:
	
	* Fluid (FLD)
	
	
	
	.. seealso:: None
	.. note:: None
	.. todo:: None
	
	"""
	
	
	#Private class attributes shared by all instances
	
	
	#Class constructor
	def __init__(self):
		"""The class constructor.

		The class constructor.

		tmp = RetinalLayers() - Creates an RetinalLayers object.
		
		"""
		#Initialize attributes

		#Layer constants
		self.layers = {'Inner Limiting Membrane': 1, 
			'Nerve Fiber Layer': 2, 
			'Ganglion Cell Layer': 3, 
			'Inner Plexiform Layer': 4, 
			'Inner Nuclear Layer': 5, 
			'Outer Plexiform Layer': 6, 
			'Outer Nuclear Layer': 7, 
			'External Limiting Membrane': 8, 
			'Rods and Cones Layers': 9, 
			'Retinal Pigment Epithelium': 10, 
			'Choroid': 20, 
			'Fluid': 1001}
			#Currently:
			# RPE includes Bruch's membrane even though most books will
			#	consider BM as part of the choroid already.
			# ONL includes Henle’s layer
			# ELM is also known as Inner Segment Layer
			# The RCL includes connecting cilia (CL), outer segment layer (OSL) and Verhoeff membrane (VM)
			
		#...and so that one can have different names for each layer
		self.layerNames = {'ilm': self.layers['Inner Limiting Membrane'],
			'innerlimitingmembrane': self.layers['Inner Limiting Membrane'],
			'nfl': self.layers['Nerve Fiber Layer'],
			'nervefiberlayer': self.layers['Nerve Fiber Layer'],
			'gcl': self.layers['Ganglion Cell Layer'],
			'ganglioncelllayer': self.layers['Ganglion Cell Layer'],
			'ipl': self.layers['Inner Plexiform Layer'],
			'innerplexiformlayer': self.layers['Inner Plexiform Layer'],
			'inl': self.layers['Inner Nuclear Layer'],
			'innernuclearlayer': self.layers['Inner Nuclear Layer'],
			'opl': self.layers['Outer Plexiform Layer'],
			'outerplexiformlayer': self.layers['Outer Plexiform Layer'],
			'onl': self.layers['Outer Nuclear Layer'],
			'outernuclearlayer': self.layers['Outer Nuclear Layer'],
			'elm': self.layers['External Limiting Membrane'],
			'externallimitingmembrane': self.layers['External Limiting Membrane'],
			'rcl': self.layers['Rods and Cones Layers'],
			'rodsandconeslayers': self.layers['Rods and Cones Layers'],
			'rpe': self.layers['Retinal Pigment Epithelium'],
			'retinalpigmentepithelium': self.layers['Retinal Pigment Epithelium'],
			'chr': self.layers['Choroid'],
			'fld': self.layers['Fluid']}
 
		#Layer acronyms
		self.layerAcronyms = {self.layers['Inner Limiting Membrane']: 'ILM',
			self.layers['Nerve Fiber Layer']: 'NFL',
			self.layers['Ganglion Cell Layer']: 'GCL',
			self.layers['Inner Plexiform Layer']: 'IPL',
			self.layers['Inner Nuclear Layer']: 'INL',
			self.layers['Outer Plexiform Layer']: 'OPL',
			self.layers['Outer Nuclear Layer']: 'ONL',
			self.layers['External Limiting Membrane']: 'ELM',
			self.layers['Rods and Cones Layers']: 'RCL',
			self.layers['Retinal Pigment Epithelium']: 'RPE',
			self.layers['Choroid']: 'Choroid',
			self.layers['Fluid']: 'Fluid'}
  
		return
		
	#Private methods
	
	#Public methods
	def getClassName(self):
		"""Gets the class name

		return: The class name
		rtype: string
		"""
		return type(self).__name__
	
	def getAllLayersIndexes(self):
		"""Gets the list of layer values

		return: The list of layers values
		rtype: list
		"""
		return list(self.layers.values())

	def getAllLayersNames(self):
		"""Gets the list of layer keys

		return: The list of layers keys
		rtype: list
		"""
	#Retrieves a list of layer keys
		return list(self.layers.keys())

	def getLayerAcronym(self,idx):
		"""Gets the acronym of the i-th layer

		return: The layer acronym e.g. NFL
		rtype: string
		"""
		lacronym = 'NaN'
		try:
			lacronym= self.layerAcronyms[idx]
		except:
			lacronym='Unknown'
			print(self.getClassName(),':getLayerAcronym: Unexpected layer index. Returning name "',lacronym,'"')
		return lacronym
		
	def getLayerIndex(self,layerName):
		"""Retrieve the index of a given layer

		return: The index of the layer
		rtype: int
		"""
		r = -1
		try:
			layerName = layerName.replace(" ", "") #Remove whitespaces
			r= self.layerNames[layerName.lower()] #Ignore case
		except:
			print(self.getClassName(),':getLayerIndex: Unknown layer name. Returning index ',r)
		return r
  
		
	def getLayerName(self,idx):
		"""Retrieve the i-th layer name

		return: The name of the i-th layer
		rtype: string
		"""
		lname = 'Default'
		try:
			#There is no 'direct' method to access the keys given the value.
			lname= list(self.layers.keys())[list(self.layers.values()).index(idx)]
		except:
			lname='Unknown'
			print(self.getClassName(),':getLayerName: Unexpected layer index. Returning name "',lname,'"')
		return lname   
		
		
	def getNumLayers(self):
		"""Return the number of known layers.

		Return the number of known layers. Please note that this also
		include known non-retinal layers like the choroid.

		return: Length of property map :func:`octant.data.OCTvolume.layers`
		rtype: int	
		"""
		return len(self.layers)
		
		
		
		