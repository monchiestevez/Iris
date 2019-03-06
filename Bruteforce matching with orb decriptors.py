#  https://docs.opencv.org/trunk/dc/dc3/tutorial_py_matcher.html
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt


img1 = cv.imread('argentina.png',cv.IMREAD_GRAYSCALE)              # queryImage
img2 = cv.imread('canada.png',cv.IMREAD_GRAYSCALE)     # trainImage


# Initiate ORB detector
orb = cv.ORB_create()
# find the keypoints and descriptors with ORB
kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)

# create BFMatcher object
bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
# Match descriptors.
matches = bf.match(des1,des2)
# Sort them in the order of their distance.
matches = sorted(matches, key = lambda x:x.distance)
# Draw first 10 matches.
img3 = cv.drawMatches(img1,kp1,img2,kp2,matches[:100],None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
plt.imshow(img3),plt.show()
