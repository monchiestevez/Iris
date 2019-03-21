import os
import cv2


def read_dataset(root: str, img_format: str):
    """
    Reading dataset of images with concrete format from root folder
    :param root: root folder
    :param img_format: format of image
    :return: list of images
    """
    images = []
    file_names = []
    for file in os.listdir(root):
        title = file.title().lower()
        if title.split('.')[-1] == img_format:
            file_names.append(title)
            images.append(cv2.imread(os.path.join(root, title)))
    return images
