.. _rst-logOfProgress_2018:

Log of progress 2018
====================

* **Author**: Felipe Orihuela-Espina
* **Created**: December 17, 2018
* **Revised**: January 21, 2018
* **Copyright** (c) 2018 INAOE



Please note that advances indicated at a particular date, may actually refer to
advances in the previous days/weeks.

* :ref:`rst-logOfProgress`



.. _secLogAdvances20181217:

Advances 17-Dec-2018
--------------------

* **Version**: v0.2
* **Responsible**: FOE

Summary of changes:

* Incorporation of the measuring of thickness to the GUI finished.
* Depuration of the technical documentation with Sphinx. This affected
  documentation in most classes. As far as I can tell, it is now up-to-date,
  and ready for v0.2 delivery.
* Integration of the informal reports to the Sphinx documentation done.
* Started working on the translation of matlab's code for manual
  edition of segmentation borders. This is yet unfinished.

.. _secLogAdvances20181213:

Advances 13-Dec-2018
--------------------

* **Version**: v0.2
* **Responsible**: FOE

Summary of changes:

* Incorporation of the measuring of thickness to the GUI started but
  unfinished. This has involved among other things;

  * Definition of two new classes; :class:`src.IOT_GUI_MeasureThicknessParameterSettings`
    for the controls and :class:`src.IOT_GUI_UtilitiesDock` for the panel dock
    of the main window.
  * Adjustments of several methods spread throughout several classes.



.. _secLogAdvances20181203:

Advances 3-Dec-2018
--------------------

* **Version**: v0.2
* **Responsible**: FOE

Summary of changes:

* Intensive testing: +20 bugs captured including syntax and logic. All
  sorted except for one of the logical ones. Initialization of a class
  attribute depends on the value of another attribute. Even if the later
  is declared in advance, it is *non-existent* until the object is created
  and thus, trying to check its value in the property methods yields an
  error.
* Substantial changes to class :class:`src.IOT_Document`, including
  encapsulation of attributes, and links with GUI, deprecation of all
  pairs get/set, the study is now an :class:`src.IOT_OCTscan` (it cannot
  further be an `np-array`) affording greater consistency, and rebranding
  of attributes e.g. `scanSegmented` to `segmentation` (even though this
  might sound trivial, but it helps to avoid conceptual "link" to scans
  instead of volumes).

  * Marked task for v0.3: Upgrade to :class:`src.IOT_OCTvolume`

* New attribute `.shape` for :class:`src.IOT_OCTscanSegmentation` for
  further internal consistency checks
* The layer thickness measurement has been even further improved with just
  a trick. This algorithm although ready, is not yet available through the
  GUI.
* Redefinition of the signature of the abstract method `execute()`
  in class :class:`src.IOT_Operation` to permit the pass of parameters.
  Also, the return value changes from `None` to the result of the
  operation (this nevertheless remains to be stored in the attribute
  `.result`, but capturing it on the fly improves efficiency and code
  readability).




.. _secLogAdvances20181116:

Advances 16-Nov-2018
--------------------

* **Version**: v0.2
* **Responsible**: FOE

NOTE: Rodrigo has reported today that all basic functions in v0.1 are
working correctly.

Summary of changes:

* Attendance to urgent demands from Rodrigo:

  * Longitudinal reflectivity profiles (a.k.a. perfilometer): Ready and
    activated in the GUI. Either pixel or window can be chosen.
  * Segmentation lines modification: The spline base edition remains ready
    in matlab from ACA but pending translation to python and adaptation to
    the new data model by FOE. **This is of outmost priority**
  * Zoom: Ready and active. This function is automatically provided by
    `matplotlib` but we have it hidden for testing purposes. Acknowledging
    Rodrigo's request, this has now been liberated.

    * This also include the option to save the images to `.png`, `.ps/eps`,
      `.pdf` and `.svd`. Since these are plain images and not our file format
      the saved image loses the document information. In reopening the file,
      this will therefore, be a plain picture, not an OCT segmentation.
    * Both the main OCT scan canvas and the perfilometer respond to the Zoom
      but they do it separatedly. It may be convenient to have these to respond
      in synchrony.
    * This also includes panning.

* Improved measuring of layer thicknesses. If the pixel size is in the
  Amira file, then the pixel width is height from there, otherwise a default
  value is assumed.
* Dummy segmentation has been largely improved. Now it covers the whole
  segmentation -which is what one should expect in segmentation- and it has
  a better handling of the `BACKGROUND` label.
* Improved documentation of classes' logs.




.. _secLogAdvances20181114:

Advances 14-Nov-2018
--------------------

* **Version**: v0.2 beta
* **Responsible**: FOE

Summary of changes:

* New tabbed settings panel in the tools window. This will hold other
  parameter settings.
* GUI controls for perfilometer settings have been added.
* New :class:`src.IOT_GUI_PerfilometerParameterSettings` for separated
  managing of GUI controls for the different operations. In the next weeks
  the panels for other operations will be added.
* Communication between the main window and the tools window is now
  bidirectional.
* Further testing on the improved stitching operation.
* Annotated a task to "concentrate" the mail reports formally in the
  documentation for easier historical documentation.

Bug found:

* Stitching works for the first execution (first 2 images), but crashes if
  a second execution is attempted (third image is stitched).


In addition to the above:

* FOE has consumed the available quota of Git LFS. This will be a problem
  when the time comes to upload the new installers to GitHub. No clear
  solution is now available.




.. _secLogAdvances20181107:

Advances 7-Nov-2018
--------------------

* **Version**: v0.2 beta
* **Responsible**: FOE

Summary of changes:

* Data model for v0.2 is now finished.
* Improved stitching; no black stripes. Further, the resulting image now
  adapts its output size to the image size. Initial testing looks good, but
  more testing is needed.
* Debugging of all classes inheriting from :class:`IOT_Operation`
* Loading of images now works from the GUI with the new data model. Now,
  a :class:`IOT_OCTscan` is loaded instead of an `nd.array`.
* Perfilometer is also responding now to the new data model. In the GUI,
  only the global behaviour is currently available. FOE will implement
  access to Perfilometer settings in the GUI asap.

* Bug fixing:

  * Found and circumvented a bug in the `panorama` external library. This library
    does not work well with grayscale images, so I force an artificial
    conversion to RGB prior to calling panorama functions.





.. _secLogAdvances20181023:

Advances 23-Oct-2018
--------------------

* **Version**: v0.2 beta
* **Responsible**: FOE

Summary of changes:

* Some tasks have been reorganized to give priority to things that are
  more pressing for Rodrigo (e.g. those less urgent delayed to v0.3, and
  those more urgent bring forward to v0.2)
* Parameters of the perfilometer operation have been encapsulated so that
  they can be made accesible through the GUI. GUI access has yet to be
  implemented though.
* Improvements to the data model; new class :class:`src.IOT_OCTscanSegmentation`
  to support segmentation maps.

  * As a corollary, we have to revisit the rendering of the segmentation.

* Migration of all operation to used the abstract method `execute()` has now
  been completed. This provides a uniform call for operations. Further,
  this has been made already considering classes :class:`src.IOT_OCTscan`
  and :class:`src.IOT_OCTscanSegmentation`. Initial testing is showing
  excellent performance.

  * All original operation specific methods have been declared deprecated.

* String representation (method `__str__`) for some further classes have
  been created. Some others still remains. Those which inherit from
  :class:`src.IOT_Operation` are presenting a bug due to some recursive
  calling.
* Code cleaning. Some unnecessary `import` have been removed.
* Bug fixing:

  * "leakage" of the algorithm for measuring the layers thickness has now
    been attended. Some further testing is needed.



.. _secLogAdvances20181001:

Advances 1-Oct-2018
--------------------

* **Version**: v0.2 beta
* **Responsible**: FOE

Summary of changes:

* New classes :class:`src.IOT_OCTscan` e :class:`src.IOT_OCTvolume` for
  a more homogeneuous and extensible data model. Before this, we were working
  directly over the separated images which resulted in a code poor in
  efficiency and difficult to maintain and extend. These two classes are now
  ready but testing is needed.
* Yet another large cleaning of code. Although without inmeadiate effects
  this is expected to be critical for forthcoming changes and implementation
  of new features.
* Substantial improvement of the technical and user documentation. This is
  now available through readthedocs.

  * https://oct-tools.readthedocs.io/en/latest/

* Improve error control with the `warnings` library.
* Incorporation of the string representation (implementaiton of method
  `__str__`) for some of the classes. Others will follow.
* Improved encapsulation through the use of decorator `@property` in
  several classes. Others will follow.
* Attention to one of the pendings from v0.1; Class :class:`src.IOT_operation`
  is now abstract. The abstract method `execute()` must be implemeted by child
  classes. Operands has been moved to superclass :class:`src.IOT_operation`
  and arity is now calculated on the fly.
  A few operations have already been updated to deal with this new
  method, and the rest will follow soon.
* Code for the :class:`src.AmiraReader` has been liberated to return all
  scans again. Although this was available at earlier versions, but it was
  disabled while we develop v0.1 for the sake of sanity. Support for dealing
  with different scans has yet to be added to the GUI.





.. _secLogAdvances20180913:

Advances 13-Sep-2018
--------------------

* **Version**: v0.1
* **Responsible**: FOE

Summary of changes:

* New installer for v0.1 ready and sent to Rodrigo. See :ref:`installation
  instructions <rst-installation>`.



.. _secLogAdvances20180906:

Advances 6-Sep-2018
--------------------

* **Version**: v0.1
* **Responsible**: FOE

Summary of changes:

* The installer appears to be working, but the installed `.pyw` (python's
  equivalent to `.exe`) is not. The problem seems to be in the "linking"
  with `pytonw.exe` (python's equivalent to `command.com` in Windows). JHV
  and FOW are now looking at this.


.. _secLogAdvances20180904:

Advances 4-Sep-2018
--------------------

* **Version**: v0.1
* **Responsible**: FOE

Summary of changes:

* Version compiler and installer working. FOE opted for packing
  python on the installation to minimize risks of the application not
  working at Rodrigo's machine. The price to pay is a very large
  installer (almost 600Mb -84Mb zipped-). Overhead is brutal! Over 450Mb!
  ...but hopefully worth it.
* JHV and SMH are now testing.



.. _secLogAdvances20180902:

Advances 2-Sep-2018
--------------------

* **Version**: v0.1 alpha
* **Responsible**: FOE

Summary of changes:

* Improved separation of model (:class:`src.IOT_Document`), view
  (:class:`src.IOT_GUI_\*` classes)  and controllers
  (:class:`src.IOT_Operation` and subclasses)
* Polished GUI does no longer depend on QTDesigner
* Mouse control is now working
* All :class:`src.IOT_operations` are now correctly connected to Document through the GUI
* New class :class:`src.IOT_RetinalLayers` for easier control of retinal layer informations
* Connected GUI with basic delect and changeLabel EditSegmentation operations for ROI and COI.

Known issues:

* The stitching algorithm still leaves the "black" regions
* :class:`src.IOT_Document` only follows one scan at a time. Liberate
  all scans in the Amira reader
* Transformation from screen pixels to image pixels is missing. Algorithms
  for which the input depend on the mouse work as long as the document window
  is not resized. Upon resizing, there is risk of "index out of bounds".
* Dummy segmentation "only" paints default edges instead of a full image. This
  will make the :class:`src.IOT_OperationMeasureLayerThickness` class to measure
  incorrectly. It is necessary to separate the segmentation map itself (all
  pixels in layer painted) from its representation (only top edge painted)
* Document saving not released. Pictures can be saved by print screen only
  at this moment.
* Advanced segmentation editing tools e.g. cubic splines line modification
  not yet incorporated.
* Color of layers fixed. We need to provide a tool for selecting color layers
* There is a need for an :class:`src.IOT_Settings` class to store settings,
  both application-wide and study-specific. A simple map will do the job.
  We need one instance of this :class:`src.IOT_Settings` for application
  settings and the another for the study. JSON can be used to save these
  to a `.txt` file if we do not want to get a full XML parser.


.. _secLogAdvances20180828:

Advances 28-Aug-2018
--------------------

* **Version**: v0.1 beta
* **Responsible**: FOE

Summary of changes:

* The suboperations for edition of segmentation; remove and change label
  have been added to the GUI. This has been made both for COI (class of
  interest -global changes-) and ROI (region of interest -local changes-)
  based operations. Some testing is needed.
* To avoid a third window with the operations settings/options the GUI
  has been modified.
* Dependence on Qt's **Designer** and on `.ui` files have been eliminated.
* Class :class:`src.IOT_RetinalLayers` has been created. This provides a
  better manipulation of tissue layers.



.. _secLogAdvances20180824:

Advances 24-Aug-2018
--------------------

* **Version**: v0.1 beta
* **Responsible**: FOE

Summary of changes:

* Finally cracked on the mouse listening problem! A dummy ``matplotlib``
  embedded in Qt window example has been prepared. The solution did not
  came from using ``QMouseEvent`` -this listens to events
  within the window, but NOT within the matplotlib canvas axes-. The
  solution required bypassing the matplotlib own events
  ( https://matplotlib.org/users/event_handling.html ) so that they
  can be listen by the container window. Now that the solution has been
  found, this should be incorportated to the application in the next
  few days.

GitHub commit/pull/push should be made as soon as this is attended.



.. _secLogAdvances20180817:

Advances 17-Aug-2018
--------------------

* **Version**: v0.1 beta
* **Responsible**: FOE

Summary of changes:

* Not good news. The problem with the listening to mouse events freezing
  the application after just a few clicks remains open. Yesterday, JHV
  and FOE work on this for a while without spotting anything obvious.
  In the next few days we will be trying a plan B using Qt class
  ``QMouseEvent``.


.. _secLogAdvances20180813:

Advances 13-Aug-2018
--------------------

* **Version**: v0.1 beta
* **Responsible**: FOE

Summary of changes:

* Work on the issue of the listening to mouse events leaving the application
  frozen. This is a well known issue of ``pynput`` library for **Windows*** as
  reported in:

  https://pynput.readthedocs.io/en/latest/mouse.html#monitoring-the-mouse

  “The listener callbacks are invoked directly from an operating thread
  on some platforms, notably Windows. This means that long running procedures
  and blocking operations should not be invoked from the callback, as this
  risks freezing input for all processes. A possible workaround is to just
  dispatch incoming messages to a queue, and let a separate thread handle them.”

  ...ergo, FOE has started to work on isolating the thread (done!) and queue
  messages (working on it). Hopefully it willbe sort out soon.



.. _secLogAdvances20180809:

Advances 9-Aug-2018
-------------------

* **Version**: v0.1 beta
* **Responsible**: FOE

Summary of changes:

* The problem with the compilation remains open. Error on modules have
  been addressed and fixed. It seems to be working on console mode (it
  prints the message "OCT-Tools Initiating..." but there seems to be a
  problem with importing ``Qt``.



.. _secLogAdvances20180806:

Advances 6-Aug-2018
-------------------

* **Version**: v0.1 beta
* **Responsible**: FOE

Summary of changes:

* All operations have been now encapsulated and are working from the GUI.
* There is no longer need to operate the steps in sequence (except of course
  opening the image for obvious reasons). Once the image is open, the work
  flow steps can be done in any order that fits the clinician. This sorts
  out the issue that operations have to be carried out step-by-step.
* If an editSegmentation operation is attempted when there is still no "automatic"
  operation, an automatic default dummy segmentation is generated on the fly. This
  is important for Rodrigo who needs NOT to depend on an automatic segmentation.
* Mouse monitoring for the manipulation of segmentation has noe been included
  over ACA functions. Nevertheless, this is currently disabled as it seems that
  listening to mouse events freezes the application.

  * We are currently using pynput but we should not discard alternative solutions.

* A full set of labelled images from Duke university has been downloaded. It may
  be convenient to test the segmentation algorithm.
* FOE has attempted a first full compilation with ``pyinstaller``.
* Bug fixing:

  * Alteration of the colour pallete by the perfilometer operation has been fixed.


The performance of the segmentation operation is pauper! Although, not a bug in the sense
that it works, but this is not acceptable.


Pending for v1.0:

* Manual manipulation is ready from ACA functions. From code, things can
  be manipulated, but without access to these from a GUI and with adequate mouse
  support, this is still insufficient. For practical matters, still useless.
* Compilation; The distribution folder is created and the `.exe` is generated
  (sized >200Mb), but errors are reported during the generation of the .exe.

  * An alternative is to pack miniconda on the distribution and prepare a batch
    file that calls the python interpreter and executes ``run.py``.

* The executable of the advanced segmentation algorithm prepared by ACA in
  **Matlab** requires Matlab Runtime environment to be executed. Obviously, we
  CANNOT  force the user to buy Matlab, and hence we must find a alternative;
  whether compile so that it can be run without Matlab Runtime environment
  (not sure if this is possible), or translate it to python, but this may not
  be trivial.




.. _secLogAdvances20180805:

Advances 5-Aug-2018
-------------------

* **Version**: v0.1 beta
* **Responsible**: FOE

Summary of changes:

* All hardcoded paths have now been cleaned. As far as I can tell there is none
  remaining.
* I have generated a minimal version where I have eliminated much of the code with
  a lot of internal tests that we have.
* The processing functions (flattening, stitching and perfilometer) have been
  encapsulated. Still pending are segmentation and editSegmentation.
* Bugs fixing:

  * File opening
  * Exiting from the menu option

* Added button "0" to open the initial imagen
* Revised and updated the AmiraReader which has now been encapsulated in a class.
* Improved and enlarged code comments.
* I have force the stitching operation to work on only 2 images at a time. One may
  still join as many as desired, but it will have to be done in pairs. For instance,
  if 3 images have to be stitched; you will have to make first 2, and then to the
  result add the 3rd. Although this works now, but it is not a desirable situation.


The above changes have improve this version a lot, although still some work
is pending on the segmentation and editSegmentation operations. No commit
to GitHub should be done until the version is fully functional.

* Bugs found:

  * The perfilometer function does not get the image size correctly. The
    problem appears to be that Python's ``skimage`` stores the images "linearized"
    (as ACA has previously warned FOE!).
  * I have forced the Amira reader to return only the first scan. RGB images
    for ``skimage`` are <width, height, filter(x3)> and typed uint8, whereas Amira
    images are grayscaled scans sized <width, height, scan(xn)> and typed
    float. Casting is needed here. Ideally, we should store in;
    <width, height, filter(x3), scan(xn)>
  * Flattening distorts the colour palette. I think I have provoked this during
    code cleaning.




.. _secLogAdvances20180803:

Advances 3-Aug-2018
-------------------

* **Version**: v0.1 beta
* **Responsible**: FOE

Summary of changes:

* After some adjustements, the program now runs in my machine (under Windows)
  and still using the interpreter. For compilation, a few other issues have
  to be attended.

    * NOTE: FOE is using **Pyzo** with **Miniconda**, whereas ACA uses **PyCharm**
      which gives some problems because uses some non-standard libraries.

* We have dependencies on **Qt5** (for the interface), but also with *SciPy*
  (this is not too serious as it is a standard library of Python, yet it must
  be installed in the interpreter).
* We have dependencies on **OpenCV** for the stitching operation which currently
  relies on external algorithm **Panorama**. While this is not ideal, but it works
  by now.
* Hardcoded path in the perfilometer function has been removed.
* Hardcoded paths in the mosaic function have been removed.
* Bugs found

  ** Upon attempting to open a new image (menu File->New) but the open file
  operation is cancelled, you get an "out of index" error. This is easy to
  removed, it only requires a parameter checking (``If ... is None``) but I did
  not have the time to finish it today.
  ** The exit option on the File menu is not working. To exit the application,
  right now it is only possible using the "x" button on the window.


Right now, the operations flow works but separatedly; each operation on its
in own. It would be convenient to modify the function ``emergentes`` so that
it stores the working image, so that this is passed down from one step to
the next. Although, this is not critical from the point of view of the
algorithms actually working, but it is very inconvenient for the user.
We CANNOT force the clinician to manually call every operation separatedly.



.. _secLogAdvances20180731:

Advances 31-Jul-2018
--------------------

* **Version**: v0.1 beta
* **Responsible**: ACA/FOE

Summary of changes:

* Still unsolved the issue with hard paths.


.. _secLogAdvances20180717:

Advances 17-Jul-2018
--------------------

* **Version**: v0.1 beta
* **Responsible**: ACA/PHW

Summary of changes:

* Reported by Rodrigo that the program does not starts up. This was found to
  be due to some remaining hard "paths".




.. _secLogAdvances20180711:

Advances 11-Jul-2018
--------------------

* Version: v0.1 beta
* Responsible: ACA

Summary of changes:

* Uploaded first version of the program and report to OSF. This version
  still has severe integration issues.
