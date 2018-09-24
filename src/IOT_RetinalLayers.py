"""
-*- coding: utf-8 -*-

File: IOT_RetinalLayers.py

Class IOT_RetinalLayers

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

.. seealso:: None
.. note:: None
.. todo:: None


.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""


## Import



## Class definition
class IOT_RetinalLayers():
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
    
    * Choroid

    .. seealso:: 
    .. note:: 
    .. todo:: 
        
    """
    
    
    #Private class attributes shared by all instances
    
    
    #Class constructor
    def __init__(self):
        #Initialize attributes

        #Layer constants
        self.layerIndex = {'Inner Limiting Membrane': 1, 
            'Nerve Fiber Layer': 2, 
            'Ganglion Cell Layer': 3, 
            'Inner Plexiform Layer': 4, 
            'Inner Nuclear Layer': 5, 
            'Outer Plexiform Layer': 6, 
            'Outer Nuclear Layer': 7, 
            'External Limiting Membrane': 8, 
            'Rods and Cones Layers': 9, 
            'Retinal Pigment Epithelium': 10, 
            'Choroid': 20}
            
        #...and so that one can have different names for each layer
        self.layerNames = {'ilm': self.layerIndex['Inner Limiting Membrane'],
            'innerlimitingmembrane': self.layerIndex['Inner Limiting Membrane'],
            'nfl': self.layerIndex['Nerve Fiber Layer'],
            'nervefiberlayer': self.layerIndex['Nerve Fiber Layer'],
            'gcl': self.layerIndex['Ganglion Cell Layer'],
            'ganglioncelllayer': self.layerIndex['Ganglion Cell Layer'],
            'ipl': self.layerIndex['Inner Plexiform Layer'],
            'innerplexiformlayer': self.layerIndex['Inner Plexiform Layer'],
            'inl': self.layerIndex['Inner Nuclear Layer'],
            'innernuclearlayer': self.layerIndex['Inner Nuclear Layer'],
            'opl': self.layerIndex['Outer Plexiform Layer'],
            'outerplexiformlayer': self.layerIndex['Outer Plexiform Layer'],
            'onl': self.layerIndex['Outer Nuclear Layer'],
            'outernuclearlayer': self.layerIndex['Outer Nuclear Layer'],
            'elm': self.layerIndex['External Limiting Membrane'],
            'externallimitingmembrane': self.layerIndex['External Limiting Membrane'],
            'rcl': self.layerIndex['Rods and Cones Layers'],
            'rodsandconeslayers': self.layerIndex['Rods and Cones Layers'],
            'rpe': self.layerIndex['Retinal Pigment Epithelium'],
            'retinalpigmentepithelium': self.layerIndex['Retinal Pigment Epithelium'],
            'choroid': self.layerIndex['Choroid']}
 
        #Layer acronyms
        self.layerAcronyms = {self.layerIndex['Inner Limiting Membrane']: 'ILM',
            self.layerIndex['Nerve Fiber Layer']: 'NFL',
            self.layerIndex['Ganglion Cell Layer']: 'GCL',
            self.layerIndex['Inner Plexiform Layer']: 'IPL',
            self.layerIndex['Inner Nuclear Layer']: 'INL',
            self.layerIndex['Outer Plexiform Layer']: 'OPL',
            self.layerIndex['Outer Nuclear Layer']: 'ONL',
            self.layerIndex['External Limiting Membrane']: 'ELM',
            self.layerIndex['Rods and Cones Layers']: 'RCL',
            self.layerIndex['Retinal Pigment Epithelium']: 'RPE',
            self.layerIndex['Choroid']: 'Choroid'}
  
        return
        
    #Private methods
    
    #Public methods
    def getClassName(self):
        return type(self).__name__
    
    def getAllLayersIndexes(self):
    #Retrieves a list of layer indexes
        return list(self.layerIndex.values())

    def getAllLayersNames(self):
    #Retrieves a list of layer keys
        return list(self.layerIndex.keys())

    def getLayerAcronym(self,idx):
    #Return the acronym of a layer idenfied by its index
        lacronym = 'NaN'
        try:
            lacronym= self.layerAcronyms[idx]
        except:
            lacronym='Unknown'
            print(self.getClassName(),':getLayerAcronym: Unexpected layer index. Returning name "',lacronym,'"')
        return lacronym
        
    def getLayerIndex(self,layerName):
    #Return the index of a layer
        r = -1
        try:
            layerName = layerName.replace(" ", "") #Remove whitespaces
            r= self.layerNames[layerName.lower()] #Ignore case
        except:
            print(self.getClassName(),':getLayerIndex: Unknown layer name. Returning index ',r)
        return r
  
        
    def getLayerName(self,idx):
    # Retrieve the layer name
        lname = 'Default'
        try:
            #There is no 'direct' method to access the keys given the value.
            lname= list(self.layerIndex.keys())[list(self.layerIndex.values()).index(idx)]
        except:
            lname='Unknown'
            print(self.getClassName(),':getLayerName: Unexpected layer index. Returning name "',lname,'"')
        return lname   
        
        
    def getNumLayers(self):
    #Return the number of known layers (please note that this also include known non-retinal layers like the choroid)
        return len(self.layerIndex)
        
        
       
             