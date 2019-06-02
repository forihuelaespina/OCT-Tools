.. _rst-toDo:

TO DO: Tasks pending for future versions
========================================

# Please, remove from here once attended.


.. _secTaskForV0.4:

Tasks pending for v0.4
----------------------

New features:

* Document serialization. See either JSON or pickle ( https://docs.python.org/3.4/library/pickle.html )
* Allow selection of scan for stitching. Currently stitching is
  made against default selected scan.



.. _secTaskForV0.3:

Tasks pending for v0.3
----------------------

New features:

* Improve segmentation algorithm
* Assign arbitrary colors to tissue layers.
* Incorporation of segmentation edition suboperation of merge ROIs
  and shifting ROIs should be incorporated. These are not aplicable
  to COI.
* Improving manual edition of segmentation borders.
* Perfilometer axis should resize with main scan axis
* Add scan navigation panel

Documentation:

* Update documentation in Eclipse for architecture (following the separation of
  foundational classes).

Miscellaneous:

* Check Duke images set to check whether they are useful to test the segmentation
  algorithm.
* Attend dependency on OpenCV (remove dependency on panorama for stitching?)
* Panorama Stitching operation to work on only 2 images at a time. One may
  still join as many as desired, but it will have to be done in pairs. For instance,
  if 3 images have to be stitched; you will have to make first 2, and then to the
  result add the 3rd. Although this works, but it is not a desirable situation.
  Note however that this is not a bug but a limitation of panorama itself. See 
  summary section Adrian Rosebrock's (creator of python's panorama code) article:

  https://www.pyimagesearch.com/2016/01/11/opencv-panorama-stitching/



  .. _secBugsKnown:


Bugs known
----------

* Although loading of scans is correct but rendering of the thumbnails is not.

