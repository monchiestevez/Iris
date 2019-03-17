import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
img1 = cv.imread('canada.png', cv.IMREAD_GRAYSCALE)          # queryImage
img2 = cv.imread('canada.png', cv.IMREAD_GRAYSCALE)          # trainImage
# Initiate SIFT detector
sift = cv.xfeatures2d.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

# BFMatcher with default params
bf = cv.BFMatcher()
matches = bf.knnMatch(des1,des2,k=2)

# Apply ratio test
good = []
for m, n in matches:
    if m.distance < 0.75*n.distance:
        good.append([m])

# cv.drawMatchesKnn expects list of lists as matches.
print(good)
print(kp1)
print(kp2)
drawmatches = cv.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)
plt.imshow(drawmatches),plt.axis("off"),plt.show()