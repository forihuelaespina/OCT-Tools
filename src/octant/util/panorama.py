# Original from:
#   https://github.com/haurbano/PythonPanorama
#	https://www.pyimagesearch.com/2016/01/11/opencv-panorama-stitching/
#
# Copyright belongs to the original developer; Hamilton Urbano (GitHub username: haurbano)


## Log
#
# 28-Apr-2019: FOE
#	+ Better support for conversion from grayscale image. Now, it can convert
#	from CV_64F.
# 	+ Added support for OpenCV version 4.x
#
# 5-May-2019: FOE
#	+ Final solution to the problem of CV_64F.
#	+ Added method prepareImageForPanorama.
#	+ Some additional cleaning.
#	+ Relaxed the need to provide the images to stitch in a specific order.
#
# 19-May-2019: FOE
#	+ The homography matrix estimated for the stitching is now saved
#	as a public attribute. This permits that I can use this later
#	for mimicking the stitching in segmentation scans.
#
# 1-Jun-2019: FOE
#	+ Class stitcher now remembers whether the order of the operands
#	were inverted during stitching (see property).
#	+ Parameters of the last stitching (ratio, reprojThresh and showMatches)
#	are also remembered.
#




# import the necessary packages
import numpy as np
import imutils
import cv2

class Stitcher:
	def __init__(self):
		# determine the version of OpenCV that we are using
		self.isv2 = imutils.is_cv2() #28-Apr-2019: FOE added
		self.isv3 = imutils.is_cv3()
		self.isv4 = imutils.is_cv4() #28-Apr-2019: FOE added
		self.homographyMatrix = None #19-May-2019: FOE added
		self.ratio=0.75 #1-Jun-2019: FOE added
		self.reprojThresh=4.0 #1-Jun-2019: FOE added
		self.showMatches=False #1-Jun-2019: FOE added
		self.switchedOperands=False #1-Jun-2019: FOE added. True if operands have to be switched in order.

	def stitch(self, images, ratio=0.75, reprojThresh=4.0,
		showMatches=False):
		
		self.ratio=ratio #1-Jun-2019: FOE added
		self.reprojThresh=reprojThresh #1-Jun-2019: FOE added
		self.showMatches=showMatches #1-Jun-2019: FOE added
		
		
		# unpack the images, then detect keypoints and extract
		# local invariant descriptors from them
		(imageB, imageA) = images
		
		
		#FOE added: Support for conversion from grayscale images.
		imageA = self.prepareImageForPanorama(imageA);
		imageB = self.prepareImageForPanorama(imageB);
		
		(kpsA, featuresA) = self.detectAndDescribe(imageA)
		(kpsB, featuresB) = self.detectAndDescribe(imageB)
		
		print('NFeatures A: ' + str(len(kpsA)) + ' ' + str(len(featuresA)))
		print('NFeatures B: ' + str(len(kpsB)) + ' ' + str(len(featuresB)))

		# match features between the two images
		M = self.matchKeypoints(kpsA, kpsB,
			featuresA, featuresB, ratio, reprojThresh)

		# if the match is None, then there aren't enough matched
		# keypoints to create a panorama
		if M is None:
			return None
		
		print('Matched keypoints: ' + str(len(M)))
		
		(matches, H, status) = M
		#print('MATCHES')
		#print(matches)
		self.homographyMatrix = H #19-May-2019: FOE added
		self.switchedOperands=False #1-Jun-2019: FOE added.
		
		#print('status')
		#print(status)
		
		#5-May-2019: FOE added
		#By default, panorama only stitches correctly if the "first"
		#image (imageA is the right-most). Obviously, we cannot expect
		#the user to pass the image in a certain sequence, and hence
		#we have to decide the order in which the images ought to be
		#stitched. We can do so by looking at the 
		#inverse transformation matrix (stored in H)
		#Fortunately, it is relatively stright forward to do so; this
		#lemma comes handy:
		#Let T be the matrix of the homogeneous transformation L. If
		#the inverse transformation L^{−1} exists, then T^ {−1} exists
		#and is the transformation matrix of L^{−1}.
		# See for details and proof:
		#	"Transformations in Homogeneous Coordinates"
		#	Yan-Bin Jia, Handouts for course Com S 477/577
		#	http://web.cs.iastate.edu/~cs577/handouts/homogeneous-transform.pdf
		#
		#So checking which whether the shifting of the image B is towards
		#right or left is just a matter of looking at the sign of
		#the shift along abscissa axes (that is H(0,2))
		
		#Decide which image goes to the left and which one goes to the right
		# otherwise, apply a perspective warp to stitch the images
		# together
		
		#Assume that images have been given in the "right" default order.
		#and stitch image B to the left.
		result = cv2.warpPerspective(imageA, H,
			(imageA.shape[1] + imageB.shape[1], imageA.shape[0]))
		result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB
		if H[0,2]<0: #Switch order and stitch image B to the right.
			#print('Switching')
			if showMatches:
				(result,vis) = self.stitch((imageA, imageB), ratio, reprojThresh,showMatches)
			else:
				result = self.stitch((imageA, imageB), ratio, reprojThresh,showMatches)
			self.switchedOperands=True #1-Jun-2019: FOE added.
		
		# check to see if the keypoint matches should be visualized
		if showMatches:
			#print('Showing matches')
			vis = self.drawMatches(imageA, imageB, kpsA, kpsB, matches,
				status)
			# return a tuple of the stitched image and the
			# visualization
			return (result, vis)
		
		# return the stitched image
		return result

	def prepareImageForPanorama(self, image):
		#Function added by FOE
		#Support for conversion from grayscale images and type CV_64F
		if len(image.shape)==2: #Grayscale image received.
			#print('Converting to grayscale.')
			try:
				image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			except:
				#28-Abr-2019: FOE: Added support for CV_64F (use of astype)
				#print('Direct conversion failed. Attempting to normalize ' + \
				#	   'and resetting image depth')
				image = cv2.cvtColor((255*image).astype('uint8'),cv2.COLOR_GRAY2RGB)
		return image

	def detectAndDescribe(self, image):
		#28-Apr-2019: FOE added
		#As from v3 SIFT algorithm is NOT accepted because it is non/free
		#
		#See: https://www.pyimagesearch.com/2015/07/16/where-did-sift-and-surf-go-in-opencv-3/
		#
		# For free alternatives see:
		#
		# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_table_of_contents_feature2d/py_table_of_contents_feature2d.html
		#
		if self.isv4: #Using OpenCV 4.X #28-Apr-2019: FOE added.
			# detect and extract features from the image
			#detector = cv2.ORB_create()
			detector = cv2.ORB_create(nfeatures=100000, \
							 nlevels = 16, \
							 fastThreshold=10, \
							 scoreType=cv2.ORB_FAST_SCORE)
			kps = detector.detect(image,None)
			(kps, features) = detector.compute(image, kps)
			#(kps, features) = detector.detectAndCompute(image, None)
			
		elif self.isv3: #Using OpenCV 3.X
			# detect and extract features from the image
			descriptor = cv2.xfeatures2d.SIFT_create()
			(kps, features) = descriptor.detectAndCompute(image, None)

		else: #using OpenCV 2.4.X
			# detect keypoints in the image
			detector = cv2.FeatureDetector_create("SIFT")
			kps = detector.detect(image)

			# extract features from the image
			extractor = cv2.DescriptorExtractor_create("SIFT")
			(kps, features) = extractor.compute(image, kps)

		# convert the keypoints from KeyPoint objects to NumPy
		# arrays
		kps = np.float32([kp.pt for kp in kps])

		# return a tuple of keypoints and features
		return (kps, features)

	def matchKeypoints(self, kpsA, kpsB, featuresA, featuresB,
		ratio, reprojThresh):
		# compute the raw matches and initialize the list of actual
		# matches
		matcher = cv2.DescriptorMatcher_create("BruteForce")
		rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
		matches = []

		# loop over the raw matches
		for m in rawMatches:
			# ensure the distance is within a certain ratio of each
			# other (i.e. Lowe's ratio test)
			if len(m) == 2 and m[0].distance < m[1].distance * ratio:
				matches.append((m[0].trainIdx, m[0].queryIdx))

		# computing a homography requires at least 4 matches
		if len(matches) > 4:
			# construct the two sets of points
			ptsA = np.float32([kpsA[i] for (_, i) in matches])
			ptsB = np.float32([kpsB[i] for (i, _) in matches])

			# compute the homography between the two sets of points
			(H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC,
				reprojThresh)

			# return the matches along with the homograpy matrix
			# and status of each matched point
			return (matches, H, status)

		# otherwise, no homograpy could be computed
		return None

	def drawMatches(self, imageA, imageB, kpsA, kpsB, matches, status):
		# initialize the output visualization image
		(hA, wA) = imageA.shape[:2]
		(hB, wB) = imageB.shape[:2]
		vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
		vis[0:hA, 0:wA] = imageA
		vis[0:hB, wA:] = imageB

		# loop over the matches
		for ((trainIdx, queryIdx), s) in zip(matches, status):
			# only process the match if the keypoint was successfully
			# matched
			if s == 1:
				# draw the match
				ptA = (int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
				ptB = (int(kpsB[trainIdx][0]) + wA, int(kpsB[trainIdx][1]))
				cv2.line(vis, ptA, ptB, (0, 255, 0), 1)

		# return the visualization
		return vis
	
	
	
	def applyStitch(self, images, H=None,switchedOperands=None):
		"""Apply the a knwon stitching to the images.
		
		Instead of calculating the homography matrix needed for the
		stitching, this method applies a known homography matrix to
		the current set of operands.
		
		:param H: The homography matrix. By default it uses the last calculated H.
			If the last calculated H is None, then a normal stitch operation
			is attempted.
		:type H: numpy.array
		:param switchedOperands: Indicates whether the operands should be switched in order.
		:type switchedOperands: Boolean.
		"""
		if H is None:
			H = self.homographyMatrix
		if switchedOperands is None:
			switchedOperands=self.switchedOperands
		
		# unpack the images
		(imageB, imageA) = images
		
		if H is None: #Note that self.homographyMatrix may still be None.
			result = self.stitch((imageB, imageA), self.ratio, self.reprojThresh,self.showMatches)
		else:
			result = cv2.warpPerspective(imageA, H,
								(imageA.shape[1] + imageB.shape[1], imageA.shape[0]))
			result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB
		# return the stitched image
		return result

