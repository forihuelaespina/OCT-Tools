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
  result add the 3rd. Although this works now, but it is not a desirable situation.
  Note however that this is a limitation of panorama itself. See summary
  section Adrian Rosebrock's (creator of python's panorama code) article:

  https://www.pyimagesearch.com/2016/01/11/opencv-panorama-stitching/



  .. _secBugsKnown:


Bugs known
----------

* Although loading of scans is correct but rendering of the thumbnails is not.
* Opening a second image for stitching will do the operation incorrectly
  but will raise an internal error in panorama;

  Traceback (most recent call last):

    File "C:\Users\felip\OneDrive\Git\OCTant\src\app\ToolsDock.py", line 401, in stitch
      self.parent().stitch()

    File "C:\Users\felip\OneDrive\Git\OCTant\src\app\DocumentWindow.py", line 726, in stitch
      self.document.setCurrentScan(tmp.execute())

    File "..\octant\op\OpScanStitch.py", line 200, in execute
      (result, vis) = stitcher.stitch([imageA, imageB], showMatches=True)

    File "..\octant\util\panorama.py", line 22, in stitch
      (kpsA, featuresA) = self.detectAndDescribe(imageA)

    File "..\octant\util\panorama.py", line 55, in detectAndDescribe
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  error: OpenCV(4.0.0) c:\projects\opencv-python\opencv\modules\imgproc\src\color.hpp:261: error: (-2:Unspecified error) in function '__cdecl cv::CvtHelper<struct cv::Set<3,4,-1>,struct cv::Set<1,-1,-1>,struct cv::Set<0,2,5>,2>::CvtHelper(const class cv::_InputArray &,const class cv::_OutputArray &,int)'
  > Unsupported depth of input image:
  >     'VDepth::contains(depth)'
  > where
  >     'depth' is 6 (CV_64F)
