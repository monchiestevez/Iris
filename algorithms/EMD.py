from scipy.stats import wasserstein_distance
from scipy.ndimage import imread
import numpy as np


def get_histogram(img):
  '''
  Get the histogram of an image. For an 8-bit, grayscale image, the
  histogram will be a 256 unit vector in which the nth value indicates
  the percent of the pixels in the image with the given darkness level.
  The histogram's values sum to 1.
  '''
  h, w = img.shape
  hist = [0.0] * 256
  for i in range(h):
    for j in range(w):
      hist[img[i, j]] += 1
  return np.array(hist) / (h * w)


a = imread('a.jpg')
b = imread('b.jpg')
a_hist = get_histogram(a)
b_hist = get_histogram(b)
dist = wasserstein_distance(a_hist, b_hist)
print(dist)