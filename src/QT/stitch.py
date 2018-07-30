# USAGE
# python stitch.py --first images/bryce_left_01.png --second images/bryce_right_01.png 

# import the necessary packages
from pyimagesearch.panorama import Stitcher
#import argparse
import imutils
import cv2
import flattening as fl
import numpy as np

# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-f", "--first", required=True,
#	help="path to the first image")
#ap.add_argument("-s", "--second", required=True,
#	help="path to the second image")
#args = vars(ap.parse_args())

# load the two images and resize them to have a width of 400 pixels
# (for faster processing)
def stitch(imageA, imageB):
    #imageA = cv2.imread("D:\Documentos\OCT\imagenes\image1.jpg")
    #imageB = cv2.imread("D:\Documentos\OCT\imagenes\image2.jpg")
    #imageA = imutils.resize(imageA, width=400)
    #imageB = imutils.resize(imageB, width=400)

    # stitch the images together to create a panorama
    stitcher = Stitcher()
    (result, vis) = stitcher.stitch([imageA, imageB], showMatches=True)
    a = fl.rgb2gray(result)
    matriz_v = np.array(a)
    good_cols = np.any(matriz_v.T != 0,  axis = 1)
    matriz_v = matriz_v[:, good_cols][:, :]
    

    # show the images
    #cv2.imshow("Image A", imageA)
    #cv2.imshow("Image B", imageB)
    #cv2.imshow("Keypoint Matches", vis)
    #cv2.imshow("Result", result)
#    cv2.waitKey(0)
    return matriz_v

#imageA = cv2.imread("D:\Documentos\OCT\git\src\left.png")
#imageB = cv2.imread("D:\Documentos\OCT\git\src\center.png") 
#imageC = cv2.imread("D:\Documentos\OCT\git\src\\right.png")  
#imageD = stitch(imageA, imageB)
#cv2.imshow("i", imageD)
    

#imageE = stitch(imageC, imageD)
#cv2.imshow("ii", imageC)
#cv2.imshow("i2", imageE)