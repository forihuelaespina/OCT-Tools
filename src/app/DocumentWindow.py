"""
-*- coding: utf-8 -*-

File: DocumentWindow.py

Class DocumentWindow

.. inheritance-diagram:: DocumentWindow

The main document window for OCTantApp. This is where the current document
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
| 13-Dec-2018 | FOE    | - Updated deprecation package to "deprecation" due   |
|             |        |   compilation problems with package "deprecated".    |
+-------------+--------+------------------------------------------------------+
| 28-Feb-2019 | FOE    | - Adapted to new package OCTant structure.           |
|             |        |   Class rebranded DocumentWindow. The prefix IOT__GUI|
|             |        |   is drop and the class is now separated from the    |
|             |        |   API.                                               |
|             |        | - Previously deprecated get/setDocument function     |
|             |        |   pair have now been fully removed.                  |
+-------------+--------+------------------------------------------------------+
|  3-Mar-2019 | FOE    | - Solved circular importing with UtilitiesDock.      |
|             |        | - Tools window is now included as a child dock using |
|             |        |   QDockWidget. Method connectToolsWindow has been    |
|             |        |   eliminated.                                        |
+-------------+--------+------------------------------------------------------+
| 17-Mar-2019 | FOE    | - Imported menu from Tools Dock.                     |
|             |        | - method openDocument renamed importAmiraFile.       |
|             |        | - New read only property parentapp to link to        |
|             |        |   parent OCTantApp application.                      |
+-------------+--------+------------------------------------------------------+
| 25-Mar-2019 | FOE    | - Method _openImageFile renamed to _importImageFile. |
|             |        |   Also, it now returns and OCTvolume rather than a   |
|             |        |   set of scans or an isolated of scan.               |
|             |        | - Method importAmiraFile updated to call             |
|             |        |   _importImageFile.                                  |
+-------------+--------+------------------------------------------------------+
| 30-Mar-2019 | FOE    | - Opening position relocated, and opens maximized.   |
|             |        | - Utilities dock moved to bottom and left bottom     |
|             |        |   corner conflict resolved.                          |
|             |        | - Property document deprecated in favour of          |
|             |        |   analogous property in OCTantApp.                   |
+-------------+--------+------------------------------------------------------+
| 31-Mar-2019 | FOE    | - Importing file also updates scans carousel in      |
|             |        |   utils dock.                                        |
|             |        | - Bug fixed. Importing image from common image       |
|             |        |   formats in _importImageFile now ensure that the    |
|             |        |   third dimension corresponds to scans and not to    |
|             |        |   RGB filters.                                       |
+-------------+--------+------------------------------------------------------+
|  7-Apr-2019 | FOE    | - New method _openDocument to read OCTant documents. |
|             |        |   Since serialization is not yet ready, by now it    |
|             |        |   yields a warning and returns an empty document.    |
|             |        | - Method importAmiraFile renamed openFile, as it     |
|             |        |   was not actually neither assuming that it was an   |
|             |        |   Amira file, nor that it was an importing operation.|
|             |        |   Further, it now distinguishes OCTant file extension|
|             |        |   to bifurcate execution to call either importFile   |
|             |        |   when the file is in an external format, or         |
|             |        |   _openDocument when it is in OCTant document format.|
|             |        | - Method _getImageFilename renamed _getFilename.     |
|             |        |   Also, Sphinx like comments have been added.        |
|             |        | - Bug fixed. Stitching was still calling "old"       |
|             |        |   method openDocument. This is a double bug; first,  |
|             |        |   the method name should have been importAmiraFile   |
|             |        |   (now openFile), and second, because it assumes     |
|             |        |   that the 2nd document has to be imported from an   |
|             |        |   external format, rather than read from my format.  |
|             |        |   Of course this is fine while we develop the        |
|             |        |   document serialization, but nonetheless, but should|
|             |        |   anticipate.                                        |
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
#from deprecated import deprecated
import deprecation


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.figure import Figure
from matplotlib.backend_bases import KeyEvent, MouseEvent
from skimage import io


from PyQt5.QtCore import Qt #Imports constants
from PyQt5.QtWidgets import QWidget, QMainWindow, QAction, QFileDialog
from PyQt5.QtGui import QMouseEvent

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)


from version import __version__
import octant as octant

from ToolsDock import ToolsDock
from UtilitiesDock import UtilitiesDock
#import UtilitiesDock #Use this formula to avoid circular importing clash


## Class definition
class DocumentWindow(QMainWindow):
    #Sphinx documentation
    """The main document window for OCTantApp.

    The main document window for OCTantApp. This is where the current document
    (i.e. the OCT image) is displayed.

    .. seealso:: None
    .. note:: None
    .. todo:: None

    """

    #Private class attributes shared by all instances
    workingDir = os.getcwd()

    #Class constructor
    def __init__(self, parent = None, theparentapp = None):
        """Class constructor"""

        #The main window should have no parent as QApplication quits
        #when the last primary window (window with no parent) is closed.

        #Call superclass constructor
        super(DocumentWindow, self).__init__(parent)

        #QDockWidget.__init__(self)
        #QMainWindow.__init__(self)
        self.move(50,50)

        #self._toolsWindow = None

        #Initialize private attributes unique to this instance
        from OCTantApp import OCTantApp #Keep this import here to avoid circular importing
                                #See: https://stackabuse.com/python-circular-imports/
#        if type(theparentapp) is not OCTantApp \
#           or type(theparentapp) is not __main__.OCTantApp:
        if type(theparentapp) is not OCTantApp:
            raise TypeError #Do not attempt to create a new application here!
        self.__parentapp = theparentapp #Do not confuse with QMainWindow parent which is a QWidget
        #self.document = None #The current document. Initialize a document
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


        #Menu
        menubar = self.menuBar()
        mArchive = menubar.addMenu('File')

        maImportAmira = QAction('Import Amira', self)
        maImportAmira.setShortcut('Ctrl+O')
        maImportAmira.setStatusTip('Import Amira OCT image')
        maImportAmira.triggered.connect(self.openFile)
        mArchive.addAction(maImportAmira)

        maQuit = QAction('Quit', self)
        maQuit.setShortcut('Ctrl+Q')
        maQuit.setStatusTip('Quite OCTant application')
        maQuit.triggered.connect(self.close)
        mArchive.addAction(maQuit)

        #self.setNativeMenuBar(False) #For Mac and Ubuntu only

        #Tools dock
        self._toolsDock = ToolsDock()
        #self._toolsDock.documentWindow(self) #Connect

        #Utilities dock
        self._utilDock = UtilitiesDock()
        #self._utilDock.documentWindow(self) #Connect


        #And add them to the QMainWindow
        self.setCentralWidget(self._canvas)
        self.addDockWidget(Qt.LeftDockWidgetArea,self._toolsDock)
        self.addDockWidget(Qt.BottomDockWidgetArea,self._utilDock)
        #self.addDockWidget(Qt.RightDockWidgetArea,self._utilDock)
        #Assign the corner to the tools
        self.setCorner(Qt.BottomLeftCorner,Qt.LeftDockWidgetArea)
        self.addToolBar(NavigationToolbar(self._canvas, self))
        #self.layout().addWidget(self._canvas)
        self.statusBar()

        self._flagEditingSegmentation = False
        self._lastMouseEvent = None
        #self.setMouseTracking(True)

        self.setWindowTitle("OCTant App")
        #self._toolsDock.show()
        #self._utilDock.show()
        self.showMaximized()

        return


    #Properties getters/setters
    #
    # Remember: Sphinx ignores docstrings on property setters so all
    #documentation for a property must be on the @property method

    #Do NOT deprecate even if only a wrapper of parentapp.document in prevision
    #of potential growing to a multiple document application.
    @property
    def document(self): #document getter
        """
        The parent application document.

        :getter: Gets the parent application document
        :setter: Sets the parent application document
        :type: class:`octant.data.Document`
        """
        #return self.__document
        return self.parentapp.document

    @document.setter
    def document(self,newDoc): #document setter
#        if newDoc is None:
#            newDoc = octant.data.Document() #Initialize a document
#        if (type(newDoc) is octant.data.Document):
#            self.__document = newDoc
#        else:
#            warnMsg = self.getClassName() + ':document: Unexpected document type.'
#            warnings.warn(warnMsg,SyntaxWarning)
        self.parentapp.document = newDoc
        return None

    @property
    def parentapp(self): #parentapp getter
        """The current "parent" application.

        This is a read only property

        :getter: Gets the current "parent" application
        :type: class:`OCTantApp`
        """
        return self.__parentapp


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



    def _getFilename(self):
        """ Open a Open file dialog window to select a file.

        The file can be in Amira o other image format.

        If the operation is cancelled, then an empty string is returned.

        :returns: The selected filename or an empty string.
        :rtype: str
        """
        #Se captura el nombre del archivo a abrir
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Open OCTant document", self.workingDir, "All Files (*);;Amira Files (*.am)", options=options)
        self.workingDir, _ = os.path.split(fileName)
        print(fileName)
        return fileName



    def _importImageFile(self,fileName):
        """Imports an OCT volume from a file.

        The file must exist or an error is generated.

        The file may be in Amira format or other.

        Regardless of the format, the first scan is automatically selected.

        :param fileName: The file name
        :type fileName: str
        :return: An OCT volume with the read scans
        :rtype: :class:`octant.data.OCTvolume`

        """
        ext = fileName.split(".")
        extension = ext[-1] #Gets the last piece (that's the extension)
        if extension == "am":
            amr = octant.op.AmiraReader()
            img = amr.readAmiraImage(fileName)
                #Reads all scans!

        else:
            img = io.imread(fileName,as_gray=True) #Ensure it is read as grayscale,
                                                    #so that it complies that the
                                                    #third axis of the array is the
                                                    #scans (and not the RGB)
            if img.ndim == 2: #For sure, as we are importing a grayscale flat
                              #image, but just to be precise...
                img = np.expand_dims(img,axis=2) #So that the "scans" dimension exist


        imWidth = img.shape[0]
        imHeight = img.shape[1]
        nScans = img.shape[2]
        print(self.getClassName(),':_openImageFile: Read ',nScans, \
                'sized [w,h]=[', imWidth,',',imHeight,']')

        vol = octant.data.OCTvolume()
        for ii in range(0,nScans,1):
            vol.addScans(octant.data.OCTscan(img[:,:,ii]))

        return vol

    def _openDocument(self,fileName):
        """Reads an OCTant document file.

        The file must exist or an error is generated.

        OCTant document files must have extension .octant

        :param fileName: The file name
        :type fileName: str
        :return: An OCTand document
        :rtype: :class:`octant.data.Document`
        """

        warnMsg = self.getClassName() + ':_openDocument: OCTant serialization not yet ready. Returning new document.'
        warnings.warn(warnMsg,SyntaxWarning)

        doc = octant.data.Document();
        return doc


    def _preparePlottingWindow(self):
        #Initialize the document window
        if self._docWindow is None:
            self._docWindow = DocumentWindow()
        return self._docWindow



    #Public methods

    def getClassName(self):
        """Get the class name as a string.

        Get the class name as a string.

        :returns: The class name.
        :rtype: string
        """
        return type(self).__name__

#    def connectToolsWindow(self,theToolsWindow):
#        self._toolsWindow = theToolsWindow



#    def closeEvent(self,event):
#        """Closes the document window and the application."""
#        print('Closing OCTant')
#        #This is not yet working
#        #self._docWindow.closeEvent(event)
#        self.close()
#        if event:
#            event.accept()
#        #self.close

#    #@deprecated(version='0.2', reason="Deprecated. Acess property .document instead.")
#    def getDocument(self):
#        """Gets the current document.
#
#        :returns: The current document
#        :rtype: :class:`octant.data.Document`
#        """
#        return self.document
#
#    #@deprecated(version='0.2', reason="Deprecated. Acess property .document instead.")
#    @deprecation.deprecated(deprecated_in="0.2", removed_in="0.3",
#                        current_version=__version__,
#                        details="Access property .document instead.")
#    def setDocument(self,d):
#        """Sets the current document.
#
#        :param d: The new document
#        :type d: :class:`octant.data.Document`
#        """
#        self.document = d;
#        return


    def perfilometer(self):
        """Renders the perfilometer"""
        octScan = self.document.getCurrentScan()
        if octScan is not None:
            tmp = octant.op.OpScanPerfilometer()
            tmp.addOperand(octScan)
#            if (self._toolsWindow is not None):
#                settingsGUI = self._toolsWindow._settingsOperationPerfilometer
#                tmp.pixelColumn = settingsGUI.getPixelColumnValue()
#                tmp.windowHalfWidth = settingsGUI.getWidthValue()
            if (self._toolsDock is not None):
                settingsGUI = self._toolsDock._settingsOperationPerfilometer
                tmp.pixelColumn = settingsGUI.getPixelColumnValue()
                tmp.windowHalfWidth = settingsGUI.getWidthValue()
            return tmp.execute()
        else:
            #Return a flat line
            return np.array([0]);

    def refresh(self):
        """Visualizes the selected scan, its perfilometer and its segmentation"""
        octScan = self.document.getCurrentScan()
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
            r= octant.RetinalLayers()
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
        #self._utilDock.scanscarousel.octvolume = self.document.study
        self._utilDock.refresh()

        return





    #Operation methods
    def openFile(self):
        """Open a file and sets the current document.

        Open a file selection dialog, and depending on the selected file,
        it either reads an OCTant document, or import the file content.

        If opening the file succeeds, then it sets the current document.
        If opening the file fails, it initializes the current document to
        an empty one.


        :returns: A document
        :rtype: :class:`octant.data.Document`.
        """

        tmp = self.document #Capture current document
        if tmp is None:
            tmp = octant.data.Document() #Initialize an empty document

        fileName = self._getFilename()
        if fileName: #Empty strings evaluate to false in Python;
                     #If fileName is empty, this skips the attempt to open the file
            #print("OCT-Tools: OCTToolsMainWindow: Opening file ", fileName)

            tmp = octant.data.Document() #Forget current document and initialize a new empty document
            tmp.name = fileName
            tmp.folderName = self.workingDir
            tmp.fileName = fileName

            ext = fileName.split(".")
            extension = ext[-1] #Gets the last piece (that's the extension)
            if extension == "octant":
                tmp.study = self._openDocument()
            else: #Import file in external format
                vol = self._importImageFile(fileName)
                tmp.study = vol



        else:
            #continue with current document
            pass


        self.document = tmp
        #self.show() #Ensure it is visible. Pressing the close button in the document window, only hides the document window
        self._utilDock.scanscarousel.octvolume = self.document.study
        self._utilDock.refresh()
        self.refresh()

        return self.document


    def brush(self):
        """Applies the brush operation over the segmentation.

        :returns: The document segmentation
        :rtype: class:`octant.data.OCTscanSegmentation`
        """
        if self.document.segmentation is None:
            warnMsg = self.getClassName() + ':brush: Scan segmentation not initialized.'
            warnings.warn(warnMsg,SyntaxWarning)
        else:
            tmp = octant.op.OpSegmentationBrush()
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
        """Selects a second scan and applies the stitching step to the current scan.

        The 2nd scan is read from another file (see method openFile).
        If the selected file is an OCTant document the selected scan in the
        document will be used for stitching.
        If the selected file is in an external file, the first scan (default)
        will be used for stitching

        .. todo: Allow selection of scan for stitching.

        :returns: The volume resulting from the stitching
        :rtype: class:`octant.data.OCTscan`
        """
        tmp = octant.op.OpScanStitch()
        tmp.addOperand(self.document.getCurrentScan())
        doc2 = self.openFile()
        tmp.addOperand(doc2.getCurrentScan())
        print('Current scan shape (before stitching): ' + str(self.document.getCurrentScan().shape))
        silly=tmp.execute()
        print(silly.shape)
        #self.document.setCurrentScan(tmp.execute())
        self.document.setCurrentScan(silly)
        print('Current scan shape (after stitching): ' + str(self.document.getCurrentScan().shape))
        self.refresh()
        return self.document.study



    def flatten(self):
        """Applies the flattening step to the study.

        .. todo:
            Return an OCT volume

        :returns: The flattened image
        :rtype: class:`octant.data.OCTscan`
        """
        tmp = octant.op.OpScanFlatten()
        tmp.addOperand(self.document.getCurrentScan())
        self.document.setCurrentScan(tmp.execute())
        self.refresh()
        return self.document.study


    def measureThickness(self):
        """Renders layer thicknesses

        :returns: List of layers thicknesses
        :rtype: list
        """
        theSegmentation = self.document.segmentation
        if theSegmentation is not None:
            tmp = octant.op.OpScanMeasureLayerThickness()
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
            r= octant.data.RetinalLayers()
            layers = r.getAllLayersIndexes()
            thicknesses = [0 for elem in layers]
        return thicknesses


    def segment(self):
        """Applies the segmentation step.

        .. todo:
            Return an OCT segmentation volume

        :returns: The segmentation
        :rtype: class:`octant.data.OCTscanSegmentation`
        """
        seg = octant.op.OpScanSegment()
        tmp.addOperand(self.document.getCurrentScan())
        self.document.segmentation = tmp.execute()
        self.refresh()
        return self.document.segmentation



    def opEditSegmentation(self,theOperation, params = None):
        """Applies some editSegmentation step.

        .. todo:
            Return an OCT segmentation volume

        :param theOperation: The edit operation name. e.g. 'COIDelete'
        :type theOperation: string
        :param params: The params to be passed to the operation

        :returns: The segmentation
        :rtype: class:`octant.data.OCTscanSegmentation`
        """

        #Catch current OCT scan
        tmp = octant.op.OpSegmentationEdit()
        im = self.document.getCurrentScan()
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
