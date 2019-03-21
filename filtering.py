import cv2
import numpy as np


def bottom_hat_median_blurr(image):
    """
    Bottom hat filtering and smoothing with median filter
    :param image: image
    :return: filtered image
    """
    cimg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    blackhat = cv2.morphologyEx(cimg, cv2.MORPH_BLACKHAT, kernel)
    bottom_hat_filtered = cv2.add(blackhat, cimg)
    return cv2.medianBlur(bottom_hat_filtered, 17)


def adjust_gamma(image, gamma=1.0):
    """
    Building a lookup table mapping the pixel values [0, 255] to
    their adjusted gamma values. Increasing contrast
    :param image: image
    :param gamma: adjusting coefficient
    :return: adjusted image
    """
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)
