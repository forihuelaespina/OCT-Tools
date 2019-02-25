# OCT-Tools
Suite of tools for OCT analysis in Python.

Documentation available at: [readthedocs](https://oct-tools.readthedocs.io/en/latest/)

Currently, the following operations are supported:
* **Flattening**: Corrects retinal curvature using a plynomial fit to reflective RPE layer.
* **Stitching / Mosaicing**: Permits stitching together several retinal images (usually taken at different angles) to create a larger retinal image
* **Profiling**:  This is automatically "tracked". The intensity profile of the scan is reproduced "side by side" to the scan
* **Segmentation**: A very naive retinal layers segmentation algorithm (with let's be honest, still very disappointing performance). We hope to improve this soon.
* **(Manual) Edit segmentation**: Still rudimentary, but some operations to manually edit a segmentation whether by class of interest (COI) or region of interest (ROI).

## Dependencies

* The basic scientific libraries; `numpy`, `scipy`, `matplotlib`
* `scikit-image`
* OpenCV (for pyhton); that's `cv2`
* `PyQt5` (Qt for python for the GUI). Note that `sip` is "installed" separatedly
* `imutils`
* `panorama`

Installer is generated using `pynsist`.



