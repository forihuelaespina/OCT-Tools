.. _rst-toDo:

TO DO: Tasks, milestones and progress pending for future versions
=================================================================

.. LOG:
..
.. As from 11-Aug-2019 the initial simple toDo list was reconverted to a small
.. software manager. Tasks are no longer removed upon completion. Progress on
.. the tasks is also kept.
.. Tools like ZenHub, Jira, Taiga.io, Trello or MavenLink are all under subscription.
..
..
..

.. See:
.. https://sublime-and-sphinx-guide.readthedocs.io/en/latest/tables.html
..
.. For maintaining the tables, ALWAYS KEEP the toDo.xlsx. Then only export to
.. .csv for including them here.
..
.. IMPORTANT: The .csv CANNOT have character with tilde!!! Otherwise, sphynx
.. will throw a cryptic error:
.. Encoding error:
.. 'utf-8' codec can't decode byte 0xc1 in position 132: invalid start byte
.. The full traceback has been saved in C:\Users\felip\AppData\Local\Temp\sphinx-err-cljzk4dg.log, if you want to report the issue to the developers.
..
.. SO REMOVE THE TILDES OF THE NAMES IN THE CODEBOOK!!!!
..

See :ref:`secCodebook` below.

.. csv-table:: To Do List
   :file: ./toDo.csv
   :widths: 5,5,5,9,9,5,7,7,7,11,30
   :header-rows: 1

.. _secCodebook:

Codebook
--------

.. csv-table:: To Do Codebook
   :file: ./toDo_Codebook.csv
   :widths: 25, 25, 50
   :header-rows: 1


.. .. _secTaskForV0.4:
..
.. Tasks pending for v0.4
.. ----------------------
..
.. Data Model
..
.. * Provide a combined class OCTsegmentedScan that manages the raw scan
..   and their segmentation TOGETHER seamlessly.
..
.. New features:
..
.. * Document serialization. See either JSON or pickle ( https://docs.python.org/3.4/library/pickle.html )
.. * Allow selection of scan for stitching. Currently stitching is
..   made against default selected scan.
..
..
..
.. .. _secTaskForV0.3:
..
.. Tasks pending for v0.3
.. ----------------------
..
.. New features:
..
.. * Improve segmentation algorithm
.. * Assign arbitrary colors to tissue layers.
.. * Incorporation of segmentation edition suboperation of merge ROIs
..   and shifting ROIs should be incorporated. These are not aplicable
..   to COI.
.. * Improving manual edition of segmentation borders.
.. * Perfilometer axis should resize with main scan axis
.. * Add scan navigation panel
..
.. Documentation:
..
.. * Update documentation in Eclipse for architecture (following the separation of
..   foundational classes).
..
.. Miscellaneous:
..
.. * Check Duke images set to check whether they are useful to test the segmentation
..   algorithm.
.. * Panorama Stitching operation to work on only 2 images at a time. One may
.. * Attend dependency on OpenCV (remove dependency on panorama for stitching?)
..   still join as many as desired, but it will have to be done in pairs. For instance,
..   if 3 images have to be stitched; you will have to make first 2, and then to the
..   result add the 3rd. Although this works, but it is not a desirable situation.
..   Note however that this is not a bug but a limitation of panorama itself. See
..   summary section Adrian Rosebrock's (creator of python's panorama code) article:
..
..   https://www.pyimagesearch.com/2016/01/11/opencv-panorama-stitching/
..
..
..
..   .. _secBugsKnown:
..
..
.. Bugs known
.. ----------
..
.. * Although loading of scans is correct but rendering of the thumbnails is not.
..
