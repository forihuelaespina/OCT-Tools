.. _rst-intro:

About OCTant
============

OCTant (**O**ptical **C**oherence **T**omography **an**alysis **t**ools) is a suite of tools for OCT analysis in Python.

Prior to v0.3, OCTant was known as OCT-tools.

Documentation available at: [readthedocs](https://octant.readthedocs.io/en/latest/)


.. _sec:aboutthelogo:

About the logo
--------------

Typeface is Courier New bold common in many programming environments and the bold emphasis is usually kept for reserved words.
An octant is one of the 8 regions of a volumetric space partitioned by 3 orthogonal planes. A segmentation (the most relevant operation of OCTant) is also a partition of a space, and OCTant is capable of handle OCT volumes (collection of scans, the are planes usually orthogonal, A-scans, B-scans and C-scans).



.. _sec:functionality:

Functionality
-------------

Currently, the following operations are supported:
* **Flattening**: Corrects retinal curvature using a plynomial fit to reflective RPE layer.
* **Stitching / Mosaicing**: Permits stitching together several retinal images (usually taken at different angles) to create a larger retinal image
* **Profiling**:  This is automatically "tracked". The intensity profile of the scan is reproduced "side by side" to the scan
* **Segmentation**: A very naive retinal layers segmentation algorithm (with let's be honest, still very disappointing performance). We hope to improve this soon.
* **(Manual) Edit segmentation**: Still rudimentary, but some operations to manually edit a segmentation whether by class of interest (COI) or region of interest (ROI).


This should produces a inheritance diagram
.. inheritance-diagram:: src/octant


.. _subsection:


Subsection
----------

.. seealso::

   Something of the seealso here

This is a link to the :ref:`subsection`.
