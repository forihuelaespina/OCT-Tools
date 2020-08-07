.. _rst-logOfProgress_2020:

Log of progress 2020
====================

* **Author**: Felipe Orihuela-Espina
* **Created**: January 16, 2020
* **Revised**: February 18, 2020
* **Copyright** (c) 2018-20 INAOE



Please note that advances indicated at a particular date, may actually refer to
advances in the previous days/weeks.


* :ref:`rst-logOfProgress`




.. _secLogAdvances20200316:

Advances 16-Mar-2020
--------------------


* **Version**: v0.3
* **Responsible**: FOE, BGP

Summary of changes:

* Testing of the algorihtm in raster mode. Measurements of pixel distances.
* Improved raster mode for faster execution.
* Testing the code for non-squared matrices.

Bug fixing

* The implementation of the raster mode was incorrectly indexing the
  output matrix.




.. _secLogAdvances20200309:

Advances 9-Mar-2020
--------------------


* **Version**: v0.3
* **Responsible**: FOE, BGP

Summary of changes:

* Working on the implementation of the structural element, including the
  raster and anti-raster modes on a given matrix.
* Analysis of the algorithm version that uses the general distance.




.. _secLogAdvances20200225:

Advances 25-Feb-2020
--------------------


* **Version**: v0.3
* **Responsible**: FOE, BGP

Summary of changes:

* Working over structural elements and morphological operations (erosion
  and dilation, opening and closure).
* Implementation of the endpoint matrix (one of the steps of the segmentation
  algorithm).
* A bit of testing with the colour palette.
* Working of the gradient weighting



.. _secLogAdvances20200218:

Advances 18-Feb-2020
--------------------


* **Version**: v0.3
* **Responsible**: FOE, BGP

Summary of changes:

* Code analysis (Compilation path directions). Benjamin is looking to
  an automatic configuration that might not need resetting after every
  restart.

* Distance calculation under rastering and anti-rastering for supporting
  minimal path (one of the steps of the segmentation algorithm in Chapter 3
  of [1]). The minimal path is found with Dijkstra algorithm:

  * [1] Villanueva Coello, B. (2017). Análisis de imágenes oftalmológicas
      de Tomografía por Coherencia Óptica OCT.

* A bit of manual testing with Dijkstra algorithm.



.. _secLogAdvances20200121:

Advances 21-Jan-2020
--------------------


* **Version**: v0.3
* **Responsible**: FOE, BGP

Summary of changes:

* **Commit executed** : "Anisotropic diffusion filter" with the following description:

  * Added anisotropic diffusion filter
  * Better integration of the stitch and flattening operations with
    the segmentation. These operations are now also applied to the
    segmentation.
  * Class RetinalLayers now encodes fluid as a new layer.
  * Layers colors can be configured in configuration Files.
  * Perfilometer axis now correctly resizes with main scan axis.
  * Detection of the background mask now working properly.



* Bug fixing. Several classes of the `data` package were having
   issues of cyclic importing octant. In particular, import line:

  .. code-block:: Python

     import octant.data as octant

   was causing error:

   .. code-block:: Python

      AttributeError: module 'octant' has no attribute 'data'

   It has now been updated to:

   .. code-block:: Python

      from octant import data as octant

   The following files were affected:

     * `data.Document.py`
     * `data.OCTscanSegmentation.py`
     * `data.OCTvolume.py`
     * `data.OCTvolumeSegmentation.py`

Documentation

  * The log of progress for 2020 was initiated. Files affected include
    `logOfProgress_2020` and `logOfProgress`.
  * Revision date of `logOfProgress_2019` corrected


BGP adaptation

* Installation of Python and its different libraries references to the OCTan project.
* Configuration for Opencv implementation in anaconda for Python 3.7
  (https://www.youtube.com/watch?v=vePJ19ZesZk)
* Configuration of the redirection routes of the OCTan project.
* Documentation of segmentation methods for OCT images:

  * Long, J., Shelhamer, E., & Darrell, T. (2015). Fully convolutional networks
    for semantic segmentation. In Proceedings of the IEEE conference on computer
    vision and pattern recognition (pp. 3431-3440).
  * Markus A. Mayer, Joachim Hornegger, Christian Y. Mardin, and Ralf P. Tornow.
   Retinal nerve fiber layer segmentation on fd-oct scans of normal subjects and
   glaucoma patients. Biomed. Opt. Express, 1(5):1358–1383, Dec 2010.

* Familiarization with the OSF platform and documentation.
* Familiarization with the opScanSegment.py code of the OCTan project.



.. _secLogAdvances20200113:

Advances 13-Jan-2020
--------------------


* **Version**: v0.3
* **Responsible**: FOE

Summary of changes:

* Benjamin Israel Guillén Paz (BGP) joins the project. He will be working
  in the segmentation algorithm. We have been preparing his project
  document for admin purposes. Right before Christmas break we completed
  his registration in OSF and GitHub.
