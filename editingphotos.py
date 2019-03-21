import os
from matplotlib import gridspec
import cv2
import read_dataset as data
import hough_circles as hough
import visualization as vis

root = "test"
os.path.exists(root)
images = data.read_dataset(root, "png")
print(len(images))

for img in images:
    circle = hough.detect_inner_circle(img)
    circling1 = cv2.circle(img,(circle[0],circle[1]),circle[2],(0,255,0),2)
    circling2 = cv2.circle(img,(circle[0],circle[1]),2,(0,255,0),3)
    print(circling1)
    print(circling2)

vis.plot_images_grid(images[:30], 5, 6)
