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
| 24-Sep-2018 | FOE    | - Adjusted to accept all scans from the Amira but    |
|             |        |   contained to the first scan while I enable a       |
|             |        |   scan selector.                                     |
+-------------+--------+------------------------------------------------------+
| 14-Nov-2018 | FOE    | - New method connectToolsWindow so that this class   |
|             |        |   can now "know" the tools window.                   |
+-------------+--------+------------------------------------------------------+
| 16-Nov-2018 | FOE    | - Canvas navigation toolbar (for zooming, panning    |
|             |        |   saving has been enabled)                           |
+-------------+--------+------------------------------------------------------+
|  2-Dec-2018 | FOE    | - Encapsulated the document properties and deprecated|
|             |        |   get/set pair for that property.                    |
|             |        | - Minor debugging                                    |
+-------------+--------+------------------------------------------------------+
| 12-Dec-2018 | FOE    | - Internal methods are now named in English          |
|             |        |   e.g. 'openDocument' instead of 'abrir'             |
|             |        | - Added method measureThickness to call for the      |
|             |        |   corresponding operation to be executed.            |
|             |        | - Minor debugging                                    |
+-------------+--------+------------------------------------------------------+
| 20-Jan-2019 | FOE    | - Added support for the class:`IOT_OperationBrush`   |
|             |        |   operation.                                         |
+-------------+--------+------------------------------------------------------+


.. seealso:: None
.. note:: None
.. todo:: 
    * Add a scan selector
    * Encapsulate remaining attributes as properties


.. sectionauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>
.. codeauthor:: Arlem Aleida Castillo Avila <acastillo@inaoep.mx>
.. codeauthor:: Felipe Orihuela-Espina <f.orihuela-espina@inaoep.mx>

"""


## Import
import os

import warnings
from deprecated import deprecated

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.figure import Figure
from matplotlib.backend_bases import KeyEvent, MouseEvent
from skimage import io


from PyQt5.QtCore import Qt #Imports constants
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
from IOT_OCTscan import IOT_OCTscan

from IOT_OperationPerfilometer import IOT_OperationPerfilometer
from IOT_OperationMeasureLayerThickness import IOT_OperationMeasureLayerThickness
from IOT_OperationBrush import IOT_OperationBrush
from IOT_OperationEditSegmentation import IOT_OperationEditSegmentation
from IOT_OperationFlattening import IOT_OperationFlattening
from IOT_OperationSegmentation import IOT_OperationSegmentation
from IOT_OperationStitch import IOT_OperationStitch
from IOT_RetinalLayers import IOT_RetinalLayers

from IOT_GUI_UtilitiesDock import IOT_GUI_UtilitiesDock



## Class definition
class IOT_GUI_DocumentWindow(QMainWindow):
    #Sphinx documentation
    """The main document window for OCT-Tools.
    
    The main document window for OCT-Tools. This is where the current document
    (i.e. the OCT image) is displayed.
    
    .. seealso:: None
    .. note:: None
    .. todo:: None
        
    """
     
    #Private class attributes shared by all instances
    workingDir = os.getcwd()

    #Class constructor
    def __init__(self):
        """Class constructor"""
        #Call superclass constructor
        #QDockWidget.__init__(self)
        QMainWindow.__init__(self)
        
        self._toolsWindow = None
        
        #Initialize private attributes unique to this instance
        self.document = None #The current document. Initialize a document
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
        
        
        #Utilities dock
        self._utilDock = IOT_GUI_UtilitiesDock()
        
        #And add them to the QMainWindow
        self.setCentralWidget(self._canvas)
        self.addDockWidget(Qt.BottomDockWidgetArea,self._utilDock)
        self.addToolBar(NavigationToolbar(self._canvas, self))
        #self.layout().addWidget(self._canvas)
        self.statusBar()
        
        self._flagEditingSegmentation = False
        self._lastMouseEvent = None
        #self.setMouseTracking(True)
        
        self.setWindowTitle("OCT Tools App")
        self._utilDock.show()
        
        return
        
        
    #Properties getters/setters
    #
    # Remember: Sphinx ignores docstrings on property setters so all
    #documentation for a property must be on the @property method
    @property
    def document(self): #document getter
        """
        The current open document.

        :getter: Gets the current document
        :setter: Sets the current document 
        :type: class:`IOT_Document`
        """
        return self.__document

    @document.setter
    def document(self,newDoc): #document setter
        if newDoc is None:
            newDoc = IOT_Document() #Initialize a document
        if (type(newDoc) is IOT_Document):
            self.__document = newDoc
        else:
            warnMsg = self.getClassName() + ':document: Unexpected document type.'
            warnings.warn(warnMsg,SyntaxWarning)
        return None
       
    #Private methods
        
        
    def _getSemiTransparentColormap(self, N = 10):
        """Creates a semi-transparent colormap.
        
        :param N: Number of elements in the colormap.
        :type N: int
        :returns: A colormap
        :rtype: ndarray
        """
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
        fileName, _ = QFileDialog.getOpenFileName(self,"Open OCT scan", self.workingDir, "All Files (*);;Amira Files (*.am)", options=options)
        self.workingDir, _ = os.path.split(fileName)
        print(fileName)        
        return fileName
    
 

    def _openImageFile(self,fileName):
        #Open a new image file. The file must exist!
        ext = fileName.split(".")
        extension = ext[-1] #Gets the last piece (that's the extension)
        if extension == "am":
            amr = AmiraReader()
            img = amr.readAmiraImage(fileName)
                #Reads all scans!

        else:
            img = io.imread(fileName)


        imWidth = img.shape[0]
        imHeight = img.shape[1]
        nScans = img.shape[2]
        print(self.getClassName(),':_openImageFile: Read ',nScans, \
                'sized [w,h]=[', imWidth,',',imHeight,']')
        
        #Intentionally keep only first scan by now.
        if (nScans > 1):
            img = img[:,:,0];
            print(self.getClassName(),':_openImageFile: Keeping just 1st scan.')

        return img
            


    def _preparePlottingWindow(self):
        #Initialize the document window
        if self._docWindow is None:
            self._docWindow = IOT_GUI_DocumentWindow()
        return self._docWindow
        








    #Public methods
    
    def getClassName(self):
        """Get the class name as a string.

        Get the class name as a string.

        :returns: The class name.
        :rtype: string
        """
        return type(self).__name__
    
    def connectToolsWindow(self,theToolsWindow):
        self._toolsWindow = theToolsWindow
    
    
    
    def closeEvent(self, event):
        """Closes the document window and the application."""
        print('Closing OCT-Tools')
        #This is not yet working
        #self._docWindow.closeEvent(event)
        self.close()
        event.accept()
        
    @deprecated(version='0.2', reason="Deprecated. Acess property .document instead.")
    def getDocument(self):
        """Gets the current document.
        
        :returns: The current document
        :rtype: :class:`IOT_Document`
        """
        return self.document

    @deprecated(version='0.2', reason="Deprecated. Acess property .document instead.")
    def setDocument(self,d):
        """Sets the current document.
        
        :param d: The new document
        :type d: :class:`IOT_Document`
        """
        self.document = d;
        return


    def perfilometer(self):
        """Renders the perfilometer"""
        octScan = self.document.study
        if octScan is not None:
            tmp = IOT_OperationPerfilometer()
            tmp.addOperand(octScan)
            if (self._toolsWindow is not None):
                settingsGUI = self._toolsWindow._settingsOperationPerfilometer
                tmp.pixelColumn = settingsGUI.getPixelColumnValue()
                tmp.windowHalfWidth = settingsGUI.getWidthValue()
            return tmp.execute()
        else:
            #Return a flat line
            return np.array([0]);

    def refresh(self):
        """Visualizes the selected scan, its perfilometer and its segmentation"""
        octScan = self.document.study
        octScanSegmentation = self.document.segmentation
        
        #The following is a bug. It should be capture "on the fly" and
        #clearing axes rather than reset, but I cannot make it work :(
        #_,ax = self._preparePlottingWindow()
        ax = self._fig.axes
        
        #Plot 1: The image
        ax[0].clear()
        if octScan is not None:
            ax[0].imshow(octScan.data, cmap = plt.get_cmap('gray'))
        
        #Overlay segmentation if available (with a semitransparent colormap)
        if octScanSegmentation is not None:
            r= IOT_RetinalLayers()
            mycmap = self._getSemiTransparentColormap(N = r.getNumLayers())
            ax[0].imshow(octScanSegmentation.data, cmap=mycmap)
        
        
        #Plot 2: The perfilometer
        perfil = self.perfilometer()  #Updates the perfilometer
        ax[1].clear()
        ax[1].plot(perfil, np.arange(0,len(perfil)))

        #Update
        #plt.draw()
        #self._fig.draw()
        self._fig.canvas.draw()
        self._fig.canvas.flush_events()
        
        #Refresh the Docked widgets
        self._utilDock.layerThicknesses = self.measureThickness()
        self._utilDock.refresh()

        return
        
    

    

    #Operation methods
    def openDocument(self):
        """Initializes an :class:`IOT_Document` and opens a OCT image to work on.
        
        :returns: An new document
        :rtype: :class:`IOT_Document`
        """
        
        tmp = self.document #Capture current document
        if tmp is None:
            tmp = IOT_Document() #Initialize an empty document
        
        fileName = self._getImageFilename()
        if fileName: #Empty strings evaluate to false in Python;
                     #If fileName is empty, this skips the attempt to open the file
            #print("OCT-Tools: OCTToolsMainWindow: Opening file ", fileName)
            
            img = self._openImageFile(fileName)
            
            tmp = IOT_Document() #Forget current document and initialize a new empty document
            tmp.name = fileName
            tmp.folderName = self.workingDir
            tmp.fileName = fileName
            tmp.study = IOT_OCTscan(img)
                        
        else:
            #continue with current document
            pass
            
        
        self.document = tmp
        #self.show() #Ensure it is visible. Pressing the close button in the document window, only hides the document window
        self.refresh()
        
        return self.document


    def brush(self):
        """Applies the brush operation over the segmentation.
                
        :returns: The document segmentation 
        :rtype: class:`IOT_OCTscanSegmentation`
        """
        if self.document.segmentation is None:
            warnMsg = self.getClassName() + ':brush: Scan segmentation not initialized.'
            warnings.warn(warnMsg,SyntaxWarning)
        else:
            tmp = IOT_OperationBrush()
            tmp.addOperand(self.document.segmentation)
            if (self._toolsWindow is not None):
                settingsGUI = self._toolsWindow._settingsOperationBrush
                tmp.color = settingsGUI.getColorValue()
                tmp.radius = settingsGUI.getRadiusValue()
            
            print(self.getClassName(),": brush: Left click on main canvas to " \
                    + "start brushing. Right click to stop.")
            mEvent = self.waitForMouseButtonPress()    
            
            #while mEvent.name != 'button_release_event':
                #NOT WORKING; Not all release events are captured
            while mEvent.button != 3: #While not right click
                #print(mEvent.name)
                #print(mEvent.button)
                
                #MousePos holds the coordinates relative to the window
                #MouseCoords holds the coordinates relative to the canvas
                # try:
                #     #mousePos = (int(mEvent.x), int(mEvent.y))
                #     mouseCoords = (int(mEvent.xdata), int(mEvent.ydata))
                # except:
                #     warnMsg = self.getClassName() + ':execute: Unable to convert ' \
                #                 + 'mouse coordinates. Setting coordinates to (0,0).'
                #     warnings.warn(warnMsg,SyntaxWarning)
                #     #mousePos = (0,0)
                #     mouseCoords = (0,0)
                mouseCoords = (int(mEvent.xdata), int(mEvent.ydata))
                #Assign the new segmentation label
                newVoxel = (mouseCoords[1],mouseCoords[0])
                    #IMPORTANT: Note the "invertion" of indexing of coordinates
                    #this is because in screen coordinates the convention is to
                    #associate x to the abscissa, which is the column in an array
                VOIlist = list()
                VOIlist.append(newVoxel)
                tmp.setOperand(self.document.segmentation,0) #Update the first (0-th) operand
                self.document.segmentation = tmp.execute(VOIlist)
                    #Although in this case only 1 voxel is passed at a time,
                    #the nesting into voxel list facilitates generalization
                self.refresh()
                mEvent = self.getLastMouseEvent()
                
        return self.document.segmentation
        

    def stitch(self):
        """Selects a second image and applies the stitching step to the study.
        
        .. todo:
            Return an OCT volume
        
        :returns: The image resulting from the stitching
        :rtype: class:`IOT_OCTscan`
        """
        tmp = IOT_OperationStitch()
        tmp.addOperand(self.document.study)
        image2 = self.openDocument()
        tmp.addOperand(image2.study)

        self.document.study = tmp.execute()
        self.refresh()
        return self.document.study
    
     
     
    def flatten(self):
        """Applies the flattening step to the study.
        
        .. todo:
            Return an OCT volume
        
        :returns: The flattened image
        :rtype: class:`IOT_OCTscan`
        """
        tmp = IOT_OperationFlattening()
        tmp.addOperand(self.document.study)
        self.document.study = tmp.execute()
        self.refresh()
        return self.document.study
        
     
    def measureThickness(self):
        """Renders layer thicknesses
        
        :returns: List of layers thicknesses
        :rtype: list
        """
        theSegmentation = self.document.segmentation
        if theSegmentation is not None:
            tmp = IOT_OperationMeasureLayerThickness()
            tmp.addOperand(theSegmentation)
            if (self._toolsWindow is not None):
                settingsGUI = self._toolsWindow._settingsOperationMeasureThickness
                tmp.pixelColumn = settingsGUI.getPixelColumnValue()
                tmp.windowHalfWidth = settingsGUI.getWindowHalfWidthValue()
                tmp.pixelWidth = settingsGUI.getPixelWidthValue()
                tmp.pixelHeight = settingsGUI.getPixelHeightValue()
            thicknesses = tmp.execute()
        else:
            #Return a list of thickness<es of 0.
            r= IOT_RetinalLayers()
            layers = r.getAllLayersIndexes()
            thicknesses = [0 for elem in layers]
        return thicknesses

    
    def segment(self):
        """Applies the segmentation step.
        
        .. todo:
            Return an OCT volume
        
        :returns: The segmentation
        :rtype: class:`IOT_OCTscanSegmentation`
        """
        seg = IOT_OperationSegmentation()
        tmp.addOperand(self.document.study)
        self.document.segmentation = tmp.execute()
        self.refresh()
        return self.document.segmentation
        
        

    def opEditSegmentation(self,theOperation, params = None):
        """Applies some editSegmentation step.
        
        .. todo:
            Return an OCT volume

        :param theOperation: The edit operation name. e.g. 'COIDelete'
        :type theOperation: string
        :param params: The params to be passed to the operation
        
        :returns: The segmentation
        :rtype: class:`IOT_OCTscanSegmentation`
        """
        
        #Catch current OCT scan
        tmp = IOT_OperationEditSegmentation()
        im = self.document.study
        imSegmented = tmp.initEditSegmentation(im,self.document.segmentation)
        self.document.segmentation = imSegmented #Sync, in case a dummy
                                                 #one has been generated.

        #Indirect call to the operation
        #See: https://stackoverflow.com/questions/3061/calling-a-function-of-a-module-by-using-its-name-a-string    
        theOp = getattr(tmp, theOperation) 
        if params is None:
            imSegmented = theOp()
        else:
            imSegmented = theOp(*params)
        
        if not isinstance(imSegmented,bool):
            self.document.segmentation = imSegmented
        self.refresh()
            
        return self.document.segmentation
        







    #Mouse listening methods
    
    def mouseMoveEvent(self, event: MouseEvent):
        # if self._flagEditingSegmentation:
        #     #Editing segmentation
        #     # mousePos = [event.x, event.y]
        #     # mouseCoords = [event.xdata, event.ydata]
        #     # mouseInAxes= event.inaxes
        #     # print(self.getClassName(),": MouseMoveEvent: ", mousePos)
        # 
        #     # self.document.setScanSegmentation(imSegmented)
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
    
        #self.document.setScanSegmentation(imSegmented)
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
    
        #self.document.setScanSegmentation(imSegmented)
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



