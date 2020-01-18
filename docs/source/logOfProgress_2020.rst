.. _rst-logOfProgress_2020:

Log of progress 2020
====================

* **Author**: Felipe Orihuela-Espina
* **Created**: January 16, 2020
* **Revised**: January 18, 2020
* **Copyright** (c) 2018-20 INAOE



Please note that advances indicated at a particular date, may actually refer to
advances in the previous days/weeks.


* :ref:`rst-logOfProgress`



.. _secLogAdvances20191103:

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



Advances 13-Jan-2020
--------------------


* **Version**: v0.3
* **Responsible**: FOE

Summary of changes:

* Benjamin Israel Guillén Paz (BGP) joins the project. He will be working
  in the segmentation algorithm. We have been preparing his project
  document for admin purposes. Right before Christmas break we completed
  his registration in OSF and GitHub.
