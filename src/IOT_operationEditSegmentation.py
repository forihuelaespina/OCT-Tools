# -*- coding: utf-8 -*-

# File: IOT_operationEditSegmentation.py
#
# Operation EditSegmentation
# 
# This class permits manual manipulation of a segmentation of retinal layers from an OCT image
#
#
#
# @dateCreated: Feb-2018
# @authors: Arlem Aleida Castillo Avila, Felipe Orihuela-Espina
# @dateModified: 5-Aug-2018
#
# See also:
# 


#
# LOG:
#
# 5-Aug-2018: FOE:
#   * Isolated minimal solution.
#   * Encapsulated in class.
#


# Import packages
from IOT_operation import IOT_operation

import numpy as np
#from skimage import feature, color
#import cv2 #That's OpenCV
#import segmentationUtils
from pynput import mouse


class IOT_operationEditSegmentation(IOT_operation):

    #Private class attributes shared by all instances
    
    #Class constructor
    def __init__(self):
        #Call superclass constructor
        super().__init__(1) #Set operation arity to 1.
        #Initialize private attributes unique to this instance
        self._imgin = np.zeros(shape = (0,0,0), dtype = np.uint8 ); #Input image
        self._imgout = np.zeros(shape = (0,0,0), dtype = np.uint8 ); #The segmented image
        self._flagListening = False #Flag for listening to mouse events
    
    
    #Private methods


    #Mouse listening methods
    def on_move(self,x, y):
        #Do nothing
        #print('Pointer moved to {0}'.format((x, y)))
        return True
    
    def on_click(self,x, y, mouseButton, pressed):
        print('{0} at {1}'.format(
            'Pressed' if pressed else 'Released',
            (x, y)))
            
        if pressed:
            if mouseButton == mouse.Button.left:
                #Starts dragging segmentation line (if one is sufficiently close)
                print("Starts dragging segmentation line")
            elif mouseButton == mouse.Button.right:
                #Starts shifting whole segmentation line (if one is sufficiently close)
                print("Starts shifting segmentation line")

            return True
            
        if not pressed: #Released
            if mouseButton == mouse.Button.left:
                #Stops dragging segmentation line
                print("Stop dragging segmentation line")
            elif mouseButton == mouse.Button.right:
                #Stops shifting whole segmentation line
                print("Stops shifting segmentation line")
                # Stop listener
            return False
    
    def on_scroll(self,x, y, dx, dy):
        #Do nothing
        # print('Scrolled {0} at {1}'.format(
        #     'down' if dy < 0 else 'up',
        #     (x, y)))
        return True


  #     def on_press(self,mouseButton):
    #     #Do nothing
    #     if mouseButton == mouse.Button.left:
    #         #Starts dragging segmentation line (if one is sufficiently close)
    #         print("Starts dragging segmentation line")
    #     elif mouseButton == mouse.Button.right:
    #         #Starts shifting whole segmentation line (if one is sufficiently close)
    #         print("Starts shifting segmentation line")

   #       return True


    def on_release(self,mouseButton):
        #Do nothing
        if mouseButton == mouse.Button.left:
            #Stops dragging segmentation line
            print("Stop dragging segmentation line")
        elif mouseButton == mouse.Button.right:
            #Stops shifting whole segmentation line
            print("Stops shifting segmentation line")
            
        return True


        

    #Public methods 
    # See: https://pypi.org/project/pynput/
    def startEditSegmentation(self,image,imageSegmented = None):
        #Starts editing segmentation though listening the mouse
        
        #print("OCT-Tools: IOT_operationSegmentation: segmentar: Starting manual editing of retinal layer segmentation")
        self._imgin = image
        if imageSegmented is None:
            #print("OCT-Tools: IOT_operationSegmentation: Segmentation not found.")
            return

        if not self._flagListening:
            # Collect mouse events until stop listening (mouse.Listener.stop) 
            with mouse.Listener(
                    on_move=self.on_move,
                    on_click=self.on_click,
                    on_scroll=self.on_scroll) as listener:
                listener.join()        

        self._flagListening = True
        self._imgout = imageSegmented
        return self._imgout    






    def stopEditSegmentation(self):
        #Stops editing segmentation though stop listening the mouse
        
        #print("OCT-Tools: IOT_operationSegmentation: segmentar: Starting manual editing of retinal layer segmentation")
        mouse.Listener.stop
        self._flagListening = False
        
        return self._imgout    


