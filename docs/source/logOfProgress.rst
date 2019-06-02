.. _rst-logOfProgress:

Log of progress
===============

* **Author**: Felipe Orihuela-Espina
* **Created**: December 17, 2018
* **Revised**: January 21, 2018
* **Copyright** (c) 2018 INAOE


This file attempts to gather all the reporting of progress that until
17-Dec-2018 was occurring through e-mails sent to Rodrigo Matsui. After that
date, we more or less succeeded in maintain this log up-to-date. Please, note
however, that this account does not cover the very first part of the project,
and that we may have missed some of the e-mails in the chain. This is
a bit more wordly and descriptive than updates to the GitHub.


Authors acronyms:

* ACA: Arlem Aleida Castillo Ávila
* FOE: Felipe Orihuela-Espina
* PHW: Patrick Heyer-Wollenberg

Testers acronyms:
* JHV: Javier Herrera-Vega
* SMH: Samuel Montero Hernández







.. _secProgressLog:

Progress Log
============

Please note that advances indicated at a particular date, may actually refer to
advances in the previous days/weeks.



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
