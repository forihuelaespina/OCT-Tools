"""
-*- coding: utf-8 -*-

File: IOT_GUI_DocumentWindow.py

Class IOT_GUI_DocumentWindow

IOT stands for INAOE OCT Tools

The main document window for OCT-Tools. This is where the current document
(i.e. the OCT image) is displayed.

:Log:

+-------------+--------+------------------------------------------------------+
| Date        | Author | Description                                          |
+=============+========+======================================================+
| 21-Aug-2018 | FOE    | - Class created. This class was created as a wrapper |
|             |        |   to host the OCT image figure canvas.               |
+-------------+--------+------------------------------------------------------+
| 30-Aug-2018 | FOE    | - New instance attribute _lastMouseEvent now keeps   |
|             |        |   track of mouseEvents so that other classes to have |
|             |        |   access to it. A get method is also added.          |
+-------------+--------+------------------------------------------------------+
| 1-Sep-2018  | FOE    | - There is no longer a _flagEditSegmentation to keep |
|             |        |   track of when editing is possible.                 |
|             |        | - Method editSegmentar is no longer needed, and      |
|             |        |   opEditSegmentation exhibits a behaviour more       |
|             |        |   analogous to other operations.                     |
|             |        | - Mouse listening methods, now are only respoonsible |
|             |        |   for storing the last event.                        |
|             |        | - Some cleaning. Removal of unused code              |
+-------------+--------+------------------------------------------------------+
| 23-Sep-2018 | FOE    | - Updated comments and added Sphinx documentation to |
|             |        |   the class                                          |
+-------------+--------+------------------------------------------------------+

.. seealso:: None
.. note:: None
.. todo:: None



@dateCreated: 21-Aug-2018
@dateModified: 23-Sep-2018

.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Arlem Aleida Castillo Avila <acastillo@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""


## Import
import os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.figure import Figure
from matplotlib.backend_bases import KeyEvent, MouseEvent
from skimage import io


from PyQt5.QtWidgets import QWidget, QMainWindow, QFileDialog
from PyQt5.QtGui import QMouseEvent

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)


from AmiraReader import AmiraReader 
from IOT_Document import IOT_Document

from IOT_OperationPerfilometer import IOT_OperationPerfilometer
from IOT_OperationEditSegmentation import IOT_OperationEditSegmentation
from IOT_OperationFlattening import IOT_OperationFlattening
from IOT_OperationSegmentation import IOT_OperationSegmentation
from IOT_OperationStitch import IOT_OperationStitch
from IOT_RetinalLayers import IOT_RetinalLayers




## Class definition
class IOT_GUI_DocumentWindow(QMainWindow):
    #Sphinx documentation
    """The main document window for OCT-Tools.
    
    The main document window for OCT-Tools. This is where the current document
    (i.e. the OCT image) is displayed.
    
    .. seealso:: 
    .. note:: 
    .. todo:: 
        
    """
     
    #Private class attributes shared by all instances
    workingDir = os.getcwd()

    #Class constructor
    def __init__(self):
        #Call superclass constructor
        #QDockWidget.__init__(self)
        QMainWindow.__init__(self)
        
        
        #Initialize private attributes unique to this instance
        self._document = None #The current document. Initialize a document
        #self._perfil = None #The perfilometer image
        
        #Prepare the matplotlib figure area to render the current OCT scan
        self._fig = Figure(figsize=(10, 8))
        
        #Prepare the grid
        gs = gridspec.GridSpec(1, 2, width_ratios=[5, 1])
        self._fig.add_subplot(gs[0]) #The OCT image
        self._fig.add_subplot(gs[1]) #The perfilometer
        
        
        #make ticklabels invisible
        for i, axs in enumerate(self._fig.axes):
            axs.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
            axs.tick_params(labelbottom=False, labelleft=False)

        #Render
        #plt.show() #Do not "show" the plot directly. It will "create" another
                    #window on its own.
                    #Instead, first it is necessary to encapsulate the
                    #matplotlib figure into a Qt widget FigureCanvas, and
                    #then call the window QMainWindow.show()
                    #method after creation.
        
        #Encapsulate the matplotlib figure into a Qt widget FigureCanvas   
        self._canvas = FigureCanvas(self._fig) #first link the figure to the FigureCanvas 
        self._fig.set_canvas(self._canvas); #Then, inform the figure who is its cointainer
        
        #Link to pass matplotlib.MouseEvent to this class so that mouse
        #events can be controlled from here.
        #For a complete list of events, please refer to:
        #https://matplotlib.org/users/event_handling.html
        #
        # Event name	        | Class         - Description
        #=======================+===============+===========================
        #'button_press_event'   | MouseEvent    - mouse button is pressed
        #'button_release_event' | MouseEvent    - mouse button is released
        #'motion_notify_event'  | MouseEvent    - mouse motion
        #'scroll_event'         | MouseEvent    - mouse scroll wheel is rolled
        #'draw_event'           | DrawEvent     - canvas draw (but before screen update)
        #'key_press_event'      | KeyEvent      - key is pressed
        #'key_release_event'    | KeyEvent      - key is released
        #'pick_event'           | PickEvent     - an object in the canvas is selected
        #'resize_event'         | ResizeEvent   - figure canvas is resized
        #'figure_enter_event'   | LocationEvent - mouse enters a new figure
        #'figure_leave_event'   | LocationEvent - mouse leaves a figure
        #'axes_enter_event'     | LocationEvent - mouse enters a new axes
        #'axes_leave_event'     | LocationEvent - mouse leaves an axes
        self._cid=list() #Initialize empty list
        tmpCid = self._fig.canvas.mpl_connect('motion_notify_event', self.mouseMoveEvent)
        self._cid.append(tmpCid)
        tmpCid = self._fig.canvas.mpl_connect('button_press_event', self.mousePressEvent)
        self._cid.append(tmpCid)
        tmpCid = self._fig.canvas.mpl_connect('button_release_event', self.mouseReleaseEvent)
        self._cid.append(tmpCid)
        tmpCid = self._fig.canvas.mpl_connect('scroll_event', self.mouseWheelEvent)
        self._cid.append(tmpCid)
        
        #And add it to the QMainWindow
        self.setCentralWidget(self._canvas)
        #self.addToolBar(NavigationToolbar(self._canvas, self))
        #self.layout().addWidget(self._canvas)
        self.statusBar()
        
        self._flagEditingSegmentation = False
        self._lastMouseEvent = None
        #self.setMouseTracking(True)
        
        return
        
        
        
    #Private methods
        
        
    def _getSemiTransparentColormap(self, nLayers = 10):
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



    def _getImageFilename(self):
        #Chooses a new image to work on.
        #The image can be in Amira o other image format.
        #If the operation is cancelled, then an empty string is returned
        #Se captura el nombre del archivo a abrir
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Abrir OCT image", self.workingDir, "All Files (*);;Amira Files (*.am)", options=options)
        self.workingDir, _ = os.path.split(fileName)
        print(fileName)        
        return fileName
    
 

    def _openImageFile(self,fileName):
        #Open a new image file. The file must exist!
        ext = fileName.split(".")
        extension = ext[-1] #Gets the last piece (that's the extension)
        if extension == "am":
            #carpeta = AmiraReader(fileName).carpeta
            #fileName = (carpeta+"scan1.png") #THIS IS A BUG!!!! We should be reading the AMIRA file!
            #self._img = np.zeros(0);
            amr = AmiraReader()
            img = amr.readAmiraImage(fileName)
        else:
            img = io.imread(fileName)

        return img
            


    def _preparePlottingWindow(self):
        #Initialize the document window
        if self._docWindow is None:
            self._docWindow = IOT_GUI_DocumentWindow()
        return self._docWindow
        








    #Public methods
    
    def getClassName(self):
        return type(self).__name__
    
    
    
    
    def closeEvent(self, event):
        print('Closing OCT-Tools')
        #This is not yet working
        #self._docWindow.closeEvent(event)
        self.close()
        event.accept()
        
    def getDocument(self):
        return self._document

    def setDocument(self,d):
        if d is None:
            d = IOT_Document() #Initialize a document
        self._document = d;
        self.refresh()
        return


    def perfilometro(self):
        #Renders the perfilometer
        perf = IOT_OperationPerfilometer()
        return perf.perfilometry(self._document.getStudy())

    def refresh(self):
    #Visualizes the selected scan, its perfilometer and its segmentation
        octScan = self._document.getStudy()
        octScanSegmentation = self._document.getScanSegmentation()
        
        #The following is a bug. It should be capture "on the fly" and
        #clearing axes rather than reset, but I cannot make it work :(
        #_,ax = self._preparePlottingWindow()
        ax = self._fig.axes
        
        #Plot 1: The image
        ax[0].clear()
        if octScan is not None:
            ax[0].imshow(octScan, cmap = plt.get_cmap('gray'))
        
        #Overlay segmentation if available (with a semitransparent colormap)
        if octScanSegmentation is not None:
            r= IOT_RetinalLayers()
            mycmap = self._getSemiTransparentColormap(nLayers = r.getNumLayers())
            ax[0].imshow(octScanSegmentation, cmap=mycmap)
        
        
        #Plot 2: The perfilometer
        perfil = self.perfilometro()  #Updates the perfilometer
        ax[1].clear()
        ax[1].plot(perfil, np.arange(0,len(perfil)))

        #Update
        #plt.draw()
        #self._fig.draw()
        self._fig.canvas.draw()
        self._fig.canvas.flush_events()

        return
        
    

    

    #Operation methods
    def abrir(self):
        #Open an OCT image to work on.
        
        tmp = self._document #Capture current document
        if tmp is None:
            tmp = IOT_Document() #Initialize an empty document
        
        fileName = self._getImageFilename()
        if fileName: #Empty strings evaluate to false in Python;
                     #If fileName is empty, this skips the attempt to open the file
            #print("OCT-Tools: OCTToolsMainWindow: Opening file ", fileName)
            
            img = self._openImageFile(fileName)
            
            tmp = IOT_Document() #Forget current document and initialize a new empty document
            tmp.setName(fileName)
            tmp.setFolderName(self.workingDir)
            tmp.setFileName(fileName)
            tmp.setStudy(img)
                        
        else:
            #continue with current document
            pass
            
        
        self._document = tmp
        #self.show() #Ensure it is visible. Pressing the close button in the document window, only hides the document window
        self.refresh()
        
        return self._document


    def stitching(self):
        #Selects a second image and applies the stitching step
        #self.abrir() overwrites self._img so I need to make a copy of the current self._img
        image1 = self._document.getStudy()
        image2 = self.abrir()
        st = IOT_OperationStitch()
        image3 = st.stitch(image1, image2)
        self._document.setStudy(image3)
        #self._docWindow.setDocument(self._document)
        #self._docWindow.refresh()
        self.refresh()
        return image3
    
     
     
    def rectificar(self):
        #Applies the flattening step
        fl = IOT_OperationFlattening()
        im= self._document.getStudy()
        im = fl.flattening(im)
        self._document.setStudy(im)
        #self._docWindow.setDocument(self._document)
        self.refresh()
        return im
        
     
     
    def segmentar(self):
        #Applies the segmentation step
        seg = IOT_OperationSegmentation()
        im = self._document.getStudy()
        imSegmented = seg.segmentar(im)
        self._document.setScanSegmentation(imSegmented)
        self.refresh()
        return imSegmented
        
        

    def opEditSegmentation(self,theOperation, params = None):
        #Applies some editSegmentation step
        #
        # theOperation: A string with the edit operation name. e.g. 'COIDelete'
        # params: The params to be passed to the operation
        
        #Catch current OCT scan
        seg = IOT_OperationEditSegmentation()
        im = self._document.getStudy()
        imSegmented = self._document.getScanSegmentation()
        imSegmented = seg.initEditSegmentation(im,imSegmented)
        self._document.setScanSegmentation(imSegmented) #Sync, in case a dummy
                                                        #one has been generated.

        #Indirect call to the operation
        #See: https://stackoverflow.com/questions/3061/calling-a-function-of-a-module-by-using-its-name-a-string    
        theOp = getattr(seg, theOperation) 
        if params is None:
            imSegmented = theOp()
        else:
            imSegmented = theOp(*params)
        
        if not isinstance(imSegmented,bool):
            self._document.setScanSegmentation(imSegmented)
        self.refresh()
            
        return self._document.getScanSegmentation()
        







    #Mouse listening methods
    
    def mouseMoveEvent(self, event: MouseEvent):
        # if self._flagEditingSegmentation:
        #     #Editing segmentation
        #     # mousePos = [event.x, event.y]
        #     # mouseCoords = [event.xdata, event.ydata]
        #     # mouseInAxes= event.inaxes
        #     # print(self.getClassName(),": MouseMoveEvent: ", mousePos)
        # 
        #     # self._document.setScanSegmentation(imSegmented)
        #     # self.refresh()
        #     
        #     self._lastMouseEvent = event
        # else:
        #     #Not editing segmentation
        #     pass
        
        #print(self.getClassName(),": MouseMoveEvent: Saving current event.")
        self.setLastMouseEvent(event)
        return




    def mousePressEvent(self, event: MouseEvent):
        # mousePos = [event.x, event.y]
        # mouseCoords = [event.xdata, event.ydata]
        # mouseButton = event.button #1 -Left, 2 - Middle, 3 - Right
        # if mouseButton == 1:
        #     print(self.getClassName(),": MousePressEvent: Left clicked at ",mousePos)
        # elif mouseButton == 3:
        #     print(self.getClassName(),": MousePressEvent: Right clicked at ",mousePos)
        
        #print(self.getClassName(),": MousePressEvent: Saving current event.")
        self.setLastMouseEvent(event)
        return




    def mouseReleaseEvent(self, event: MouseEvent):
        # mousePos = [event.x, event.y]
        # mouseCoords = [event.xdata, event.ydata]
        # mouseButton = event.button #1 -Left, 2 - Middle, 3 - Right
    
        #self._document.setScanSegmentation(imSegmented)
        #self.refresh()
        
        #print(self.getClassName(),": MouseReleaseEvent: Saving current event.")
        self.setLastMouseEvent(event)
        return



    def mouseWheelEvent(self, event: MouseEvent):
        # mousePos = [event.x, event.y]
        # mouseCoords = [event.xdata, event.ydata]
        # mouseButton = event.button #'up' or 'down'
        # print(self.getClassName(),": mouseWheelEvent: Wheel ", mouseButton ," at ",mousePos)
        
        # consume the event so it will do nothing
        #pass
    
        #self._document.setScanSegmentation(imSegmented)
        #self.refresh()
        
        #print(self.getClassName(),": MouseWheelEvent: Saving current event.")
        self.setLastMouseEvent(event)
        return


    def getLastMouseEvent(self):
    #So that other windows can "listen" to events in this one
        return self._lastMouseEvent


    def setLastMouseEvent(self, event: MouseEvent):
    #Set the last mouse event and update the status bar.
    
        #Watch out! Events controlled by matplotlib will be passed as
        #matplotlib.MouseEvents (these are; move, button pressed, button
        #released, and wheel operation within the figure), but events
        #in the window but not in the figure (e.g. corner click to resize)
        #will be passed as a QMouseEvent
        
        if isinstance(event,QMouseEvent): #QMouseEvent event
            msg = "Detected QMouseEvent."


        elif isinstance(event,MouseEvent): #matplotlib event
            self._lastMouseEvent = event
            
            #...and update the status bar
            mousePos = (int(event.x), int(event.y))
            mouseCoords = [event.xdata, event.ydata]
            mouseButton = event.button #'up' or 'down'
            
            #note that at this point there is no way to distinguish a move event from
            #a release event (both have the mouse.button to none)
            msg= ""
            if mouseButton == 1:
                msg = msg + "Left click at " + str(mousePos)
            elif mouseButton == 2:
                msg = msg + "Middle click at " + str(mousePos)
            elif mouseButton == 3:
                msg = msg + "Right click at " + str(mousePos)
            elif mouseButton == 'up':
                msg = msg + "Wheel up at " + str(mousePos)
            elif mouseButton == 'down':
                msg = msg + "Wheel down at " + str(mousePos)
            else:
                msg = msg + str(mousePos)
        
        else: #Unknown event type 
            msg = "Unknown event type. Ignoring"

        #print(event)
        #print(self.getClassName(),": setLastMouseEvent: ",msg)
        self.statusBar().showMessage(msg)
        
        return self._lastMouseEvent


    def waitForMouseButtonPress(self):
    #Wraps the waitforbuttonpress from matplotlib
        
        #matplotlib.waitforbuttonpress returns:
        #   True is a key was pressed,
        #   False if a mouse button was pressed
        #   None if timeout was reached (with negative timeout, it does not timeout
        mouseButtonPressed = False
        while not mouseButtonPressed:
            tmp=self._fig.waitforbuttonpress(timeout=-1)
            mouseButtonPressed = (tmp == False)
        return self._lastMouseEvent



