import os
import cv2


class Dataset:
    """
    Representing dataset of images
    """

    def __init__(self, root_folder: str, img_format: format, images=None):
        self.root = root_folder
        self.img_format = img_format
        self.images_names = None
        self.images = images

    def load_dataset(self, root: str, img_format: str):
        """
        Loading dataset of images with concrete format from root folder
        :param root: root folder
        :param img_format: format of image
        :return: list of images
        """
        self.images = []
        self.images_names = []
        for file in os.listdir(root):
            title = file.title().lower()
            if title.split('.')[-1] == img_format:
                self.images_names.append(title)
                self.images.append(cv2.imread(os.path.join(root, title)))
