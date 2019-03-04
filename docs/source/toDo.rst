.. _rst-toDo:

TO DO: Tasks pending for future versions
========================================

# Please, remove from here once attended.


.. _secTaskForV0.3:

Tasks pending for v0.3
----------------------

* Improve segmentation algorithm
* Attend dependency on OpenCV (remove dependency on panorama for stitching?)
  Related to this, panorama is now throwing the following error in line 67

  * AttributeError: module 'cv2.cv2' has no attribute 'FeatureDetector_create'

* Stitching operation to work on only 2 images at a time. One may
  still join as many as desired, but it will have to be done in pairs. For instance,
  if 3 images have to be stitched; you will have to make first 2, and then to the
  result add the 3rd. Although this works now, but it is not a desirable situation.
* Check Duke images set to check whether they are useful to test the segmentation
  algorithm.
* Assign arbitrary colors to tissue layers.
* Create support for application-wide Settings
* Update documentation in Eclipse for architecture (following the separation of
  foundational classes).
* Incorporation of segmentation edition suboperation of merge ROIs
  and shifting ROIs should be incorporated. These are not aplicable
  to COI.
* Improving manual edition of segmentation borders.
* Bug pending for the stitching of more than 3 scans.
* Attempting to open a new scan when one is already open, will launch
  the opening dialog, but this will be freezed.
