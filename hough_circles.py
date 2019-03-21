import cv2
import numpy as np
import filtering as filt


def detect_inner_circle(img, canny_param=20, hough_param=20):
    """
    Detecting inner iris circle after filtering
    :param img: image
    :param canny_param: higher threshold for canny edge detector
    :param hough_param: threshold parameter for Hough circle transform
    :return:
    """
    filtered = filt.bottom_hat_median_blurr(img)
    adjusted = filt.adjust_gamma(filtered, 10)
    circles = cv2.HoughCircles(adjusted, cv2.HOUGH_GRADIENT, 1, 20,
                               param1=canny_param,
                               param2=hough_param,
                               minRadius=0)
    inner_circle = [0, 0, 0]
    if circles is not None:
        inner_circle = np.uint16(np.around(circles[0][0])).tolist()
    return inner_circle