import cv2
import os

scanned = 'tests/temp_bw.png'
surf = cv2.xfeatures2d.SURF_create(400)
surf.setUpright(True)

img1 = cv2.imread(scanned, 0)
kp1, des1 = surf.detectAndCompute(img1, None)

FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

for filename in os.listdir('images'):
    img2 = cv2.imread('images/' + filename, 0)
    kp2, des2 = surf.detectAndCompute(img2, None)
    flann.add([des2])

print str(len(flann.getTrainDescriptors()))

flann = cv2.flann.Index()
print "Training..."
flann.build(des_all, index_params)
print "Matching..."
indexes, matches = flann.knnSearch(des1, 2)
