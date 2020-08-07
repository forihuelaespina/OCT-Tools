.. _rst-logOfProgress_2019:

Log of progress 2019
====================

* **Author**: Felipe Orihuela-Espina
* **Created**: December 17, 2018
* **Revised**: January 21, 2018
* **Copyright** (c) 2018-9 INAOE



Please note that advances indicated at a particular date, may actually refer to
advances in the previous days/weeks.


* :ref:`rst-logOfProgress`



.. _secLogAdvances20191103:

Advances 3-Nov-2019
--------------------

* **Version**: v0.3
* **Responsible**: FOE

Summary of changes:

The project has suffered a 2 months period of inactivity due to
other commitments. Activity is now being retaken.

* Segmentation algorithm progress;

  * Detection of the background mask now working properly.
  * Advanced in the assigment of tissue pixels to retinal layers.

* GUI

  * Detection of console/terminal or gui mode for showing a progress
    bar during segmentation annotated as a pending task. FOE have
    made some progress here, but this is not yet working.

Documentation

  * Class :class:`octant.data.RetinalLayers` Added some comments
    about sublayers.






. _secLogAdvances20190819:

Advances 19-Aug-2019
--------------------

* **Version**: v0.3
* **Responsible**: FOE

Summary of changes:


* Segmentation algorithm progress;

  * Started updating the detection of the background mask.
  * The output of the anisotropic diffusion filter has been normalized and
    discretized so that the values can be related to retinal layers, but
    this is not yet clear. I'm still looking at the histogram.
  * The anisotropic diffusion filter is now a static function for
    greater flexibility.

* GUI:

  * With the new graphical progress bar in method :func:`execute` of
    class :class:`octant.op.OpScanSegment`, matplotlib backend was no longer
    automatically launching inline in the IPython console. Now it
    requires explicit call to:

    * `%matplotlib` to activate the backend
    * `%matplotlib inline` to make it work interactively in the IPython console.

  * I have tried to automatically detect whether the program is being
    executed from the terminal or from the GUI using `os.isatty` and
    `sys.stdin.isatty` but none can really make the distinction. Thus,
    by now I have "disconnected" the progress bar, while I work, but
    the code is there to be activated whenever is needed.


Documentation

* Log of progress split by year for easier management. Collaterally it also
  improves the indexing of the main table of contents, as it moves one
  level down the weekly progress sections.




.. _secLogAdvances20190812:

Advances 12-Aug-2019
--------------------

* **Version**: v0.3
* **Responsible**: FOE

Summary of changes:

* The perfilometer axis now correctly resizes with main scan axis.
* Integration of the diffusion filter in the main GUI, that is, removed
  intermediate figure plotting, debugging code, etc. Also added a
  progress bar.

Documentation

* Documentation update. Sphynx documentation recompiled.
* Updating of the versioning, planning and toDo.

  * Reorganization of the `toDo <toDo.rst#section>`__  list to act also
    for monitoring task progress, kinda 'tiny' software manager tool.
    Not the best option, but the options for software management that I
    know are all proprietary software. So it will do by now.
  * Reassignment of tasks to version as appropriate.

Bug Fixing

* `DocumentWindow.refresh`: Perfilometer was plot "upside down". It now
   renders adequately.



.. _secLogAdvances20190808:

Advances 8-Aug-2019
--------------------

* **Version**: v0.3
* **Responsible**: FOE

Summary of changes:

* Worked on making the perfilometer axis to resize with main scan axis.
  Although, it does it transiently, but it flickers and goes back to a
  different size. So not fully working yet.



.. _secLogAdvances20190708:

Advances 8-Jul-2019
--------------------

* **Version**: v0.3
* **Responsible**: FOE

Summary of changes:

* Automatic segmentation; diffusion filtering. Finally working!
  In the end there was not a single but several errors, including;

  * Inadequate parameterization for human retina. [WangRK2005] Parameters
    were for the porcine trachea.
  * Regularization Gaussian mask was increased from 3x3 to 7x7 and Updated
    every integration.
  * Update of the image on each iteration was not being done properly.
  * The morphological filter has been recovered but with a twist.
    It is now applied on every iteration of the diffusion filter.




.. _secLogAdvances20190704:

Advances 4-Jul-2019
--------------------

* **Version**: v0.3
* **Responsible**: FOE

Summary of changes:

NOTE: Progress this week was hindered due to problems with FOE's laptop.

* Automatic segmentation; diffusion filtering. After several attempts to
  check for errors in the programming without success in preventing the
  diluting of the gradient, an alternative hypothesis is that since the
  parameterization in [WangRK2005] is for the porcine trachea, these
  parameter values may not be good for the human retina. I have started
  to look for parameterization in human retina, but so far no joy.





.. _secLogAdvances20190624:

Advances 24-Jun-2019
--------------------

* **Version**: v0.3
* **Responsible**: FOE

Summary of changes:

* Attempted to improve the performance of the segmentation algorithm by
  substituting the initial noise removal step from the current morphological
  closing of opening to the more specialized **non-linear anisotropic diffusion filter**
  as first described by [P. Perona and J. Malik, IEEE Trans. Pattern Anal.
  Mach. Intel. 12, 629 (1990)] and later reported for OCT by [Wang, RK
  (2005) Proc. SPIE 5690:380-385].

  * This is still NOT working. Unfortunately, the gradient seem to be
    diluting to quickly, and thus output image is distorted in scale. After,
    some thinking and testing I think the error can be in our gray images being
    scaled [0,1] but [WangRK2005] perhaps using a [0,255] scale. Another,
    potential explanation is the iterative nature of the Gaussian mask
    (see [Salinas and Cabrera-Fernandez (2007) TMI, 26(6):761-771].




.. _secLogAdvances20190618:

Advances 18-Jun-2019
--------------------

* **Version**: v0.3
* **Responsible**: FOE

Summary of changes:

* Added codification of fluid as an additional segmentation layer in
  :class:`RetinalLayers` for pathological cases.
* Added colormap of retinal layers to settings in configuration file as
  settings `retinallayerscolormap`. The chosen default
  colormap is according to [ChiuSJ2015_BOE] with the minor unfolding
  of the GCL-ILM layers and the consideration of choroid.

* Documentation

  * Prepared report on the flattening algorithm and uploaded to OSF.io
    in the Results component.
  * Uploaded several new references to OSF.io
  * Fixed link to OCTant in GitHub from OSF.io. It was still pointing to
    old oct-tools.
  * OSF.io main project component renamed to also include OCTant in the
    title.
  * Initial check on Duke dataset [ChiuSJ2015_BOE]. Exploration thus
    far is being made in MATLAB (as this is the original format in which
    the dataset is released). Advances so far are being reported in file
    DukeOCTDataset_2015_BOE_Chiu_README.txt, but further work is still
    necessary to fully decode how the dataset is encoded.



.. _secLogAdvances20190610:

Advances 10-Jun-2019
--------------------

* **Version**: v0.3
* **Responsible**: FOE

Summary of changes:


* First attempts to improve the segmentation algorithm in v0.3. Created a
  minimal sandbox for fast testing. In this process;

  * Added import of individual classes to make the `app` available as a package.
  * We learn that python
    doesn't make on demand deep copies of objects but that these have to
    be made explicitly. No big deal (although a bit unexpected since it does
    on demand deep copies of the built-in objects) but it puts
    us in the cross-road to whether we need to provide all classes with
    a copy constructor or a copyobject class method. By now the sandbox
    will continue using the package `copy` and method `deepcopy`.




.. _secLogAdvances20190601:

Advances 1-Jun-2019
--------------------

* **Version**: v0.3
* **Responsible**: FOE

Summary of changes:


* **Commit executed** : "Operations model based on OCTvolume stable"
* Added several new properties (ratio, projThresh and showMatches) to
  :class:`Stitcher` in panorama. It now keeps track of whether the operands
  were switched, and also remembers parameterization.
* New method readFile in :class:`octant.data.Document` preparation for
  persistence. Still naive though.
* Class :class:`octant.op.OpScanStitch` underwent several changhes;

  * Added property switchedOperands to flag whether switching the order
    of the operands was needed during stitching.
  * Added property sparedCols to mark the size of the "black" spared region.
  * Added method applyStitch to repeat a known sticthing to operands. This
    can be used to apply the same stitch to a different set of scans. In
    practical terms, it can be used to apply the same panoramic
    stitching to segmentation scans after it has been precalculated to
    anatomical scans.

* Class :class:`octant.op.OpScanFlatten` underwent several changhes;

  * New read only property deformation map to store the deformation map
    associated with the flattening operation.
  * New method applyOperation to repeat a known flatenning operation to
    operands. This can be used to apply the same flattening to a different set
    of scans. In practical terms, it can be used to
    apply the same flatenning to segmentation scans
    after it has been precalculated to anatomical scans.



* Class :class:`octant.app.DocumentWindow` underwent several changhes;

  * Operation to stitch now also stitches the segmentation.
  * Operation to flatten now also flattens the segmentation.
  * New method _readOCTantFile for reading OCTant files
  * Method _openDocument deprecated in favour of method `_readOCTantFile`
    to avoid confusion with new method openDocument.
  * Method openFile is now static and does not modify the current document.
    Instead, new method `openDocument` wraps openFile and absorbs the non
    static operation, modifying the current document.
  * Method _importImageFile is now static.
  * Method _getSemiTransparentColormap is now static.
  * Method _getFilename is now deprecated.



Bug fixing

* :class:`OpScanMeasureLayerThickness`

  * Indexing of window was being made from from rows instead of columns.

* Class :class:`octant.app.DocumentWindow`

  * Reading second document during stitching was also modifying
    the current document segmentation because of side effect from `openFile`
    not being static.

* Class :class:`octant.app.ToolsDock`

  * Upon enabling the segmentation edit, a new dummy segmentation was always
    being created even if one already existed.



.. _secLogAdvances20190519:

Advances 19-May-2019
--------------------

* **Version**: v0.3
* **Responsible**: FOE

Summary of changes:


Currently implementing the collateral stitching of the segmentations, but
yet unfinished.


New features

* class:`octant.data.Document`

  * Properties `study` and `segmentation` are now initialized to
    :class:`OCTvolume` and :class:`OCTvolumeSegmentation` respectively.

* :class:`DocumentWindow`

  * Importing scans from an external file format now also initializes
    the document segmentation property with an empty segmentation volume
    of the same size that the imported `OCTvolume`.

* Added new property `homographyMatrix` in :class:`octant.op.OpScanStitch`.
  This permits transmitting the stitching to the segmentation scans.

  * This has required making this information accesible in panorama. Hence,
    I have also added an analogous new property `homographyMatrix` to
    :class:`octant.util.Stitcher`.


Bug fixing

* :class:`DocumentWindow`

  * Call to segment operation was assigning operand of
    :class:`octant.op.OpScanSegment` to the wrong object.
  * Reference to the :class:`octant.data.RetinalLayers` class constructor
    in the :func:`refresh` method was not indicating the subpackage.
  * Retrieval of current segmentation scan the `refresh` method was
    incorrectly pointing to the wrapping volume.
  * Remaining references to old attribute _toolsWindow updated to _toolsDock.
  * Method `measureThickness` was setting the segmentation volume instead
    of the segmentation scan as the operand for operation
    :class:`octant.op.OpScanMeasureLayerThickness`


* class:`octant.op.OpScanSegment`

  * Method :func:`execute` was not testing for number of operands correctly.

* class:`octant.data.OCTvolumeSegmentation`

  * The flag for testing all inputs in method :func:`addScanSegmentation` to
    be of type OCTscans was not being correctly initialized.

* class:`octant.data.Document`

  * Segmentation property setter was incorrectly setting property study.
  * Segmentation property setter was attempting to assert the number of
    scans against the study reference using shape instead of len.
  * Methods `getCurrentScan' and `getCurrentScanSegmentation` were not
    checking for empty scan lists.


.. _secLogAdvances20190513:

Advances 13-May-2019
--------------------

* **Version**: v0.3
* **Responsible**: FOE

Summary of changes:


Miscellaneous

* Data model with document based on :class:`octant.data.OCTvolume` is now considered
  stable.
  * **Commit executed** : "Data model based on OCTvolume stable"

Bug fixing

* Class :class:`app.ToolsDock` no longer import :class:`app.DocumentWindow`
  breaking the circular import.
* Class :class:`app.UtilitiesDock` no longer import :class:`app.DocumentWindow`
  breaking the circular import.


Documentation

* Recompiled documentation.

  * Bug fixed. Sys.paths in Sphynx `Conf.py` for package `app` was unable
    to find the path `..\..\src\app` because `\a` is a escape character.
    This was causing that the documentation of some of the classes in
    this package were not being built correctly.
  * Fixed some minor Sphinx related typos/mistakes in several files, including
    this one, `util\segmentationUtils.py`, `intro.rst`
  * Added inheritance diagrams to classes in package `app`



.. _secLogAdvances20190506:

Advances 6-May-2019
--------------------

* **Version**: v0.3
* **Responsible**: FOE

Summary of changes:

New features of the app:

* Operands passed to stitching can now be given in an arbitrary order.
  Before, the first image always had to be the right most in the mosaic.

Bug fixing

* The "bug" in panorama apparently related to an issue with images depth,
  and that happened to open Pandora's box with changes coming from the
  latest OpenCV v4.0, and that we have been dealing with in the last several
  weeks has finally been solved! Last week, we were already in the right
  path by switching to ORB features, and the updating of the syntax to
  OpernCV v4.0 but depth conversion to uint8 although mathematically
  responsive (it yielded no error) but was not giving correct results and
  thus the ORB feature detector failed to detect any features. Finally,
  This week, we succeded in getting the depth conversion right (anecdotically
  we almost got it right last week but we were scaling by 255 after downcasting
  instead of before downcasting). So in summary, the bug a mixture of a real
  issue with images depth (necessitating scaling followed by downcasting),
  new syntax in OpenCV v4.0, the disappearing of SIFT feature detector as
  a free option in OpenCV (requiring adaptation to a different feature
  detector), and finally some parameter tuning (e.g. new value for parameters
  on the feature detection and matching given the new feature detector
  algorithm). The latest parameters are:

  * nfeatures=100000 (this degrades speed a bit, so may be worth
    adjusting a bit more to the smallest number we can).
  * number pyramid levels = 16
  * fastThreshold=10
  * scoreType=cv2.ORB_FAST_SCORE
  * ratio for keypoint matching = 0.9






.. _secLogAdvances20190429:

Advances 29-Abr-2019
--------------------

* **Version**: v0.3
* **Responsible**: FOE

Summary of changes:

Bug fixing (or not)

* A new bug appear in module panorama with the upgrade to OpenCV v4.0. At first
  sight, it looks like a simple problem of panorama not being to handle
  depth of 64 bits in the images, but then
  that's only the tip of the iceberg. SIFT feature descriptors are no
  longer free, and the syntax to create the feature detector has changed
  with the new version of OpenCV. We have tried several things, but yet
  without full success;

  * Added support to panorama for OpenCV v4.0.
  * Changed the feature detector from SIFT to ORB.
  * Depth of images has been brought down to uint8 from float64. That
    permits running the mosaicing without error, but the descriptor
    then produces no features. Tested on a NON retinal image, ORB seems
    to be working fine. So perhaps ORB is not good for retinal images.
  * Changed the feature detector to BRISK. Same results as with ORB;
    no descriptors on the retinal image.
  * Attempted image normalization, but then panorama crashes again.


.. _secLogAdvances20190409:

Advances 9-Abr-2019
--------------------

* **Version**: v0.3
* **Responsible**: FOE

Summary of changes:

New features of the data model:

* New methods `getCurrentScanSegmentation` and `setCurrentScanSegmentation`
  in :class:`octant.data.Document`

New features of the app:
* Several changes to :class:`octant.app.DocumentWindow`

  * New method `_openDocument` to read OCTant documents. Since serialization
    is not yet ready, by now it yields a warning and returns an empty document.
  * Method `importAmiraFile` renamed `openFile`, as it was not actually neither
    assuming that it was an Amira file, nor that it was an importing operation.
    Further, it now distinguishes OCTant file extension to bifurcate execution
    to call either importFile when the file is in an external format, or
    `_openDocument` when it is in OCTant document format.
  * Method `_getImageFilename` renamed `_getFilename`. Also, Sphinx styled
    comments have been added.
  * Bug fixed. Stitching was still calling "old" method `openDocument`. This
    is a double bug; first, the method name should have been `importAmiraFile`
    (now `openFile`), and second, because it assumes that the 2nd document has
    to be imported from an external format, rather than read from my format.
    Of course this is fine while we develop the document serialization, but
    nonetheless, but should anticipate. Now it calls either `_openDocument` or
    `_importImageFile` as appropriate.

* Method `importAmiraFile` renamed `importFile` in :class:`octant.app.ToolsDock`


Documentation

* Added pending feature for v0.4: Allow selection of scan for stitching.
  Currently stitching is made against default selected scan.
* Annotated in toDo list detected bug in panorama.py regarding unsupported
  color depth.


Bug fixing

* References to :class:`octant.data.OCTscan` in :class:`octant.op.OpScanFlatten`
  updated.
  updated.
  * References to :class:`octant.data.OCTscan` in :class:`octant.op.OpSegmentationEdit`
* Method editSegmentation in :class:`octant.app.ToolsDock` was still
  using "old" property `documentWindow`. In now calls method parent().
* Constructor in :class:`octant.data.OCTscanSegmentation` was still
  making reference to :class:`IOT_OCTScan`.
* Call update from OpEditSegmentation._BACKGROUND to
  OpSegmentationEdit._BACKGROUND in method `_generateDummySegmentation`
  in :class:`octant.data.OCTscanSegmentation`
* Subpackage `octant.data` was not exporting :class:`octant.data.OCTscanSegmentation`
  in `__init__.py`
* Call to `study.addScanSegmentations` updated from `study.addScanSegmentation`
  in method :func:`octant.data.Document.segmentation`. Also, parameter passed
  is now correct.


.. _secLogAdvances20190401:

Advances 1-Abr-2019
--------------------

* **Version**: v0.3
* **Responsible**: FOE

Summary of changes:

New features of the data model:

* Property `currentScan` in :class:`octant.data.Document` replaced by
  methods `getCurrentScan` and `setCurrentScan`.

New features of the app:

* Button `bOpenImage` in :class:`octant.app.ToolsDock` renamed to `bImportImage`
  and relabelled to `Import image`
* Main window now opens maximized
* Utilities dock moved to bottom and left bottom corner conflict resolved.
* Started class :class:`octant.app.ScansCarousel` for visualization of
  OCT scans in a :class:`octant.data.OCTvolume` and selection of current
  scan.

  * Bug pending. Although loading of scans is correct but rendering
    of the thumbnails is not.

* Added tab to :class:`UtilitiesDock` to hold the :class:`octant.app.ScansCarousel`
* :class:`octant.app.DcoumentWindow`: Importing file also updates scans
  carousel in utils dock.

Documentation

* Added log to module `segmentationUtils`
* Fixed comments of property docwindow in :class:`octant.app.OCTantApp` which
  were referring to property settings.

Bug fixing

* Attribute `__version__` now imports correctly from :class:`octant.data.Document`
  and :class:`octant.data.OCTvolume` .
* :class:`octant.data.OCTvolume` now correctly imports deprecation.
* :class:`octant.data.OCTvolume` flagAllOCTScans in method addScans is now
  correctly returned in all cases.
* :class:`octant.app.DocumentWindow` Importing image from common image
  formats in _importImageFile now ensure that the third dimension corresponds
  to scans and not to RGB filters.




.. _secLogAdvances20190325:

Advances 25-Mar-2019
--------------------

* **Version**: v0.3
* **Responsible**: FOE

Summary of changes:

New features of the data model:

* Class :class:`octant.data.OCTvolume` has seen several changes;

  * Changed calls to isinstance for calls to type.
  * Added method getClassName.
  * Added method addScans.
  * Added method getNScans.
  * Deprecated method addScan.

* New class :class:`octant.data.OCTvolumeSegmentation`.
* Class :class:`octant.data.Document` has seen several changes;

  * Added properties docsettings.
  * Started migration to OCTvolume based document.
  * Added new docsetting .selectedScan
  * Added read only property currentScan
  * Added method pickScan.


New features of the app:

* Class :class:`octant.app.DocumentWindow` has seen several changes;

  * Method _openImageFile renamed to _importImageFile.
  * Also, it now returns and OCTvolume rather than a set of scans or
    an isolated of scan.
  * Method importAmiraFile updated to call _importImageFile.




.. _secLogAdvances201903018:

Advances 18-Mar-2019
--------------------

* **Version**: v0.3
* **Responsible**: FOE

Summary of changes:

Landmarks reached for v0.3:

* Create support for application-wide Settings

New features:

* Class :class:`octant.data.Settings` can now read and write files. JSON
  file format has been chosen for settings files.

  * Note that new dependencies `re` and `json` for reading/writing JSON files
    are both built-in features of python, and hence do not need to be
    declared in installer.cfg

* Added JSONminify module to package `octant:util`
* Class :class:`octant.app.OCTandApp` new properties :func:`.appsettings`
  and :func:`.appsettingsfile`
* New file `resources/OCTantApp.config` for persistency of application settings.
  Currently, only `workingdirectory` property has been set.
* Launching BAT file renamed to `OCTantApp.bat` and updated.
* `installer.cfg` updated for new BAT, link to new icons and new config file.
* Menu previously in tools window, has now been moved to application
  main window in :class:`octant.app.DocumentWindow`
* Method :func:`openDocument` in class :class:`octant.app.DocumentWindow`
  renamed :func:`importAmiraFile`.
* New property :func:`parentapp in class :class:`octant.app.DocumentWindow`
  connecting with the main application object.
* Class :class:`app.OCTantApp` now becomes a `QApplication` (previously
  we had 2 separated objects; one for the QApplication and another just
  for "holding" the main window.) and underwent several changes:

    * Added properties appsettings and appsettingsfile.
    * docWindow attribute converted to docwindow property.
    * Cleaner exit with call to deleteLater
    * Removed method show. Now the document window show is called accesing
      the docwindow property.


.. _secLogAdvances201903012:

Advances 12-Mar-2019
--------------------

* **Version**: v0.3
* **Responsible**: FOE

Summary of changes:

New features:

* New class :class:`octant.data.Settings` for handling document settings.

    * The dynamic struct aspect appears to be working fine.
    * :func:`read` method advanced but unfinished.

* Given initial considerations to web-based implementation with Django (thanks
  PHW for the tips!)

Bug fixing:

* Fixed: Attempting to open a new scan when one is already open, will launch
  the opening dialog, but this will be freezed. The opening dialog does no
  longer freezes and the new scan is loaded correctly.
* Attended bug regarding stitching more than 2 images as well as panorama attribute
  error;

  * panorama.py, line 67: AttributeError: module 'cv2.cv2' has no attribute 'FeatureDetector_create'

  It turns out, both issues were related. The source of the problem was that
  since OpenCV version 3.0 algorithms that are either patented or in
  experimental development (which is the case of ``FeatureDetector_create``)
  were not included/installed by default with package ``opencv-python`` and
  instead required package ``opencv-contrib-python`` (see:
  https://www.pyimagesearch.com/2015/07/16/where-did-sift-and-surf-go-in-opencv-3/ ).
  Further, packages ``opencv-contrib-python`` and ``opencv-python``
  are incompatible hence requiring uninstalling package ``opencv-python``
  before uninstalling ``opencv-contrib-python`` containing the contrib
  modules. Finally, to make things worst, the::

    pip uninstall opencv-python

  in my case left a corrupted package
  leaving pip itself in a corrupt state (``pip list`` will crash), and without
  any error message indicating the offending corrupt package causing the issue.
  It turns out, that although the latest version of ``pip`` already resolves this
  issue, "people might still be experiencing this issue because of directories
  that were corrupted before (or getting corrupted for a completely different
  reason)" (see https://github.com/pypa/pip/issues/6194 ). As indicated in
  this reference, finding the corrupt package has to be done "by hand".
  This requires going to ``C:\ProgramData\Anaconda3\lib\site-packages\``
  and looking for packages folders with a leading '-' in their names,
  and manually removed them. After this, ``pip`` comes back to life and
  ``opencv-contrib-python`` can be now installed::

    pip install opencv-contrib-python

  After successful installation of ``opencv-contrib-python`` both of the
  above issues were resolved.

  Please note that this refer the bug when trying to stitch the 3rd image
  **in pairs of 2**. The fixing does not attend the desired feature for
  stitching several images at once (as this is NOT a bug but a limitation
  of panorama as indicated in the summary section Adrian Rosebrock's
  (creator of python's panorama code) article:

    https://www.pyimagesearch.com/2016/01/11/opencv-panorama-stitching/


Documentation

* Reorganized toDo.rst in sections
* Added new pending features e.g. document class defaulting to volume
  and need for scan navigation panel.


.. _secLogAdvances20190305:

Advances 5-Mar-2019
--------------------

* **Version**: v0.3
* **Responsible**: FOE

Summary of changes:

* OCT-tools officially rebranded as OCTant. GitHub repository name updated,
  and application rebranded as OCTantApp.
* The versioning of the GUI shell and of the API are now separated. For
  simplicity however both the API and App have been assigned v0.3, but
  they will evolve separatedly from here onwards.
* New logo and icon designed.
* New package architecture in development. The previous prefix IOT in
  class names is now abandoned as classes are packaged. The new package
  structure now clearly separates the API from the app, and within they
  API, the data model classes are further separated from the operational
  classes. The folder structure is left as follows::

    src/
     |- app - The application. This is just a shell over the API.
     |- octant - The API
      |- data - Classes of the data model
      |- op - Operational classes. These are the classes that provide functionality to the package.
      |- util - A misceallaneous of additional functions and external dependencies

* All classes have been moved to their corresponding folder. The classes
  corresponding to operations are suggested to follow a naming convention
  indicating the main operand type before the operation name.
* All classes have now been migrated to the new architecture
  pending testing:

  +-------------------------------------------+-------------------------------------------+
  | **Old class name**                        | **New class name**                        |
  +===========================================+===========================================+
  | IOT_Document                              | octant.data.Document                      |
  +-------------------------------------------+-------------------------------------------+
  | IOT_OCTscan                               | octant.data.OCTscan                       |
  +-------------------------------------------+-------------------------------------------+
  | IOT_OCTvolume                             | octant.data.OCTvolume                     |
  +-------------------------------------------+-------------------------------------------+
  | IOT_OCTscanSegmentation                   | octant.data.OCTscanSegmentation           |
  +-------------------------------------------+-------------------------------------------+
  | IOT_RetinalLayers                         | octant.data.RetinalLayers                 |
  +-------------------------------------------+-------------------------------------------+
  | IOT_Operation                             | octant.op.Operation                       |
  +-------------------------------------------+-------------------------------------------+
  | IOT_OperationFlattening                   | octant.op.OpScanFlatten                   |
  +-------------------------------------------+-------------------------------------------+
  | IOT_OperationMeasureLayerThickness        | octant.op.OpScanMeasureLayerThickness     |
  +-------------------------------------------+-------------------------------------------+
  | IOT_OperationSegmentation                 | octant.op.OpScanSegment                   |
  +-------------------------------------------+-------------------------------------------+
  | IOT_OperationStitch                       | octant.op.OpScanStitch                    |
  +-------------------------------------------+-------------------------------------------+
  | IOT_OperationPerfilometer                 | octant.op.OpScanPerfilometer              |
  +-------------------------------------------+-------------------------------------------+
  | IOT_OperationBrush                        | octant.op.OpSegmentationBrush             |
  +-------------------------------------------+-------------------------------------------+
  | IOT_OperationEditSegmentation             | octant.op.OpSegmentationEdit              |
  +-------------------------------------------+-------------------------------------------+
  | OCTToolsApp                               | app.OCTantApp                             |
  +-------------------------------------------+-------------------------------------------+
  | IOT_GUI_DocumentWindow                    | app.IOT_GUI_DocumentWindow                |
  +-------------------------------------------+-------------------------------------------+
  | IOT_GUI_ToolsWindow                       | app.ToolsDock                             |
  +-------------------------------------------+-------------------------------------------+
  | IOT_GUI_UtilitiesDock                     | app.UtilitiesDock                         |
  +-------------------------------------------+-------------------------------------------+
  | IOT_GUI_EditSegmentationTools             | app.OpSegmentationEditToolsPanel          |
  +-------------------------------------------+-------------------------------------------+
  | IOT_GUI_BrushParameterSettings            | app.SettingsGUIOpSegmentationBrush        |
  +-------------------------------------------+-------------------------------------------+
  | IOT_GUI_MeasureThicknessParameterSettings | app.SettingsGUIOpScanMeasurementThickness |
  +-------------------------------------------+-------------------------------------------+
  | IOT_GUI_PerfilometerParameterSettings     | app.SettingsGUIOpPerfilometer             |
  +-------------------------------------------+-------------------------------------------+

* The class octant.op.Operation now provides support for parameters.
* The previously deprecated "original" methods for calling the operation
  have now been fully removed. The use of method :func:`execute` is now compulsory.
* Several calls to :func:`isinstance` have been changed by calls to
  :func:`type`.
* Tools window is now a child dock of DocumentWindow which is left as the
  only QMainWindow of the app.

* Documentation updates:

  * Updated project README.md
  * Updated intro.rst
  * Updated toDo.rst
  * Updated conf.py
  * Updated installation.rst
  * Updated technical.rst

* **Commit executed** : "OCTant Rebranding and repackaging"


.. _secLogAdvances20190225:

Advances 25-Feb-2019
--------------------

* **Version**: v0.3
* **Responsible**: FOE

Summary of changes:

* Reading about subpackaging.
* Planning separation of foundational classes to a separate project
  because, in giving priority to Rodrigo's request, OCT-tools has naturally
  departed from them and hence the project is not using them. Consequently,
  the following folders and files have been removed from GitHub repository:

    * docs/EclipseModelling/
    * docs/source/sciMethFileFormatSpec

  Older versions of these files can still of course be found in previous
  commit history. Documentation of the new architecture is needed. New
  Eclipse documentation will be now move to `OSF project site <https://osf.io/by79t/>`_.

* List of pending tasks has been moved to :ref:`To Do <rst-toDo>`.


* **Version**: v0.2beta
* **Responsible**: FOE

Summary of changes:

* Refreshed Sphinx documentation.
* The project will no longer be using Git LFS to avoid incurring in charges.
  As a result, Git LFS is being uninstalled. Instead, as from now, installers
  will be hosted in the `OSF project site <https://osf.io/by79t/>`_.
* For a more correct use of GitHub, the following directories have been
  declared in .gitignore to be no longer tracked, and hence are neither
  committed/pushed:

    * __pycache__/
    * obsoleteOrTestingCode/
    * docs/build/

* Version v0.2 is now considered stable and fully released.


.. _secLogAdvances20190219:

Advances 19-Feb-2019
--------------------

* **Version**: v0.2beta
* **Responsible**: FOE

Summary of changes:

* Version v0.2 beta has been committed and pushed to GitHub
* Installer generation tested on additional computer with a previous version
  of conda. It failed to compile because of an issue with packages
  certificates. A simple certificate update did not fixed the problem. A full
  update of miniconda might be needed.
* Upgraded version of python set in the installer.cfg from v3.6.5 to v3.7.1.
  This additionally demanded new wheeled versions of packages:

  * wrapt 1.11.1 - Our previous version was compiled for python v3.6.5
  * imutils 0.5.1 - Updated to v0.5.2

* New installer for python v3.7.1 ready and shared with Rodrigo.




.. _secLogAdvances20190213:

Advances 13-Feb-2019
--------------------

* **Version**: v0.2alpha
* **Responsible**: FOE

Summary of changes:

* Transitioned to package "deprecation" (from "deprecated"). This requires finer
  control of package version. Modified classes are:

  * class:`src:OCTToolsApp`
  * class:`src:IOT_Document`
  * class:`src:IOT_GUI_DocumentWindow`
  * class:`src:IOT_OCTvolume`
  * class:`src:IOT_OperationBrush`
  * class:`src:IOT_OperationFlattening`
  * class:`src:IOT_OperationMesureLayerThickness`
  * class:`src:IOT_OperationPerfilometer`
  * class:`src:IOT_OperationSegmentation`
  * class:`src:IOT_OperationStitch`

* Version control is now in version.py (instead of setup.py), and loaded in __init__.py

    * Package version control in Python is not easy with over 7 different
      potential ways to do it (https://packaging.python.org/guides/single-sourcing-package-version/#single-sourcing-the-version).
      Another additonal option is to use package pbr which I may consider in
      the future as explained here:
      https://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package
      But for now I opted for the simplest option.

* Comments in setup.py and __init__.py updated to Sphinx style
* Opening message now informs of version.
* First version of the installer is FINALLY compiling. Installer is now being tested.
* We are now in v0.2beta, but release to GitHub is pending


.. _secLogAdvances20190205:

Advances 5-Feb-2019
--------------------

* **Version**: v0.2alpha
* **Responsible**: FOE

Summary of changes:


* New attempts to generate the installer; now under Anaconda, have failed. The library “deprecated” continues to give problems for compiling in either versions 1.2.3 and 1.2.4.
* We’re now seeking alternatives:

  * Package deprecation 2.0.6
  * A shortcut by now may be to defer all deprecations to the next version.

* Deprecation in general seems to be a more general problem in python; https://www.python.org/dev/peps/pep-0004/ which might partially explain the difficulties in compiling the deprecated module.



.. _secLogAdvances20190127:

Advances 27-Jan-2019
--------------------

* **Version**: v0.2
* **Responsible**: FOE

Summary of changes:

* Version v0.2 alpha released and commited to GitHub.
* Installer.cfg updated for new package versions.

  * wrapt 1.10.11 -> wrapt 1.11.1
  * deprecated 1.2.3 -> deprecated 1.2.4

* Generation of installer in progress. The library "deprecated" which works
  well when interpreted is giving some troubles during compilation. This has
  been tested in two Windows 10 machines (FOE_INAOE laptop and CHOLULA desktop).
  Currently, investigating a solution.



.. _secLogAdvances20190120:

Advances 20-Jan-2019
--------------------

* **Version**: v0.2
* **Responsible**: FOE

Summary of changes:

* New class :class:`src.IOT_GUI_BrushParameterSettings` to support
  GUI control of the brush operation parameters.
* Modified classes :class:`src.IOT_GUI_DocumentWindow` with new method
  brush to support mouse controlled brush operation.
* Modified class :class:`src.IOT_GUI_EditSegmentationTools`: Added button
  for executing Brush operation.
* Modified class :class:`src.IOT_GUI_ToolsWindow`: Added tab in parameter
  settings panel for hold :class:`src.IOT_GUI_BrushParameterSettings`.
* New method setOperand in :class:`src.IOT_Operation`. The direct benefit
  is a faster response of the brush. But it is easy to foresee additional
  uses.

Bug fixing:

* Major debugging of :class:`src.IOT_OperationBrush`.
* Bug fixed in :class:`src.IOT_OperationBrush`:  Assigment of property
  classMap in property setter was being "assigned" to cm.

Bug detected:

* Attempting to open a new scan when one is already open, will launch
  the opening dialog, but this will be freezed.


.. _secLogAdvances20190117:

Advances 17-Jan-2019
--------------------

* **Version**: v0.2
* **Responsible**: FOE

Summary of changes:

* New class :class:`src.IOT_OperationBrush` defined for supporting the manual
  modification of the segmentation. It will act as a painting brush.
  Behaviour ready but pending testing and incorporation of controls to
  the GUI.

  NOTE; This class is using an algorithm that is different from the
  one proposed by Arlem in MATLAB.

* Bugs corrected in :class:`src.IOT_OperationEditSegmentation` whereby the output
  of the method was not returning the OCT scan. Although I have not
  experienced further errors, but I suspect that the fixing is still
  not fully correct. Some further testing is necessary.
* Bug corrected in the generation of the dummy segmentation where
  no background scan was associated to object :class:`src.IOT_OCTscanSegmentation`
  even when the :class:`src.IOT_OCTscan` was present.
