#  https://docs.opencv.org/trunk/dc/dc3/tutorial_py_matcher.html
import numpy as np
import cv2
import matplotlib.pyplot as plt
import sqlite3


img1 = cv2.imread('box.png', cv2.IMREAD_GRAYSCALE)      # queryImage
img2 = cv2.imread('box_in_scene.png', cv2.IMREAD_GRAYSCALE)   # trainImage
# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)
# BFMatcher with default params
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1, des2, k=2)
# Apply ratio test

good = []
for m, n in matches:
    if m.distance < 0.75*n.distance:
        good.append([m])

amount = len(good)
image = "test"
print(good)

connectdb = sqlite3.connect("results.db")
cursor = connectdb.cursor()
cursor.execute("INSERT INTO BFSIFT (percentage, filename, list) VALUES (?, ?, ?);", (amount, image, str(good)))
connectdb.commit()

percentages = list(connectdb.cursor().execute("SELECT * FROM BFSIFT order by percentage desc limit 10"))
print(percentages[0])

highest = percentages[0]
connections = highest[2]
print(connections)

# cv.drawMatchesKnn expects list of lists as matches.
img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, connections, None)
plt.imshow(img3), plt.show()
