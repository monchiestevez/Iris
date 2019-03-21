from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec


def plot_images_grid(images, height, width):
    """
    Plotting height * width number of images from collection images
    in a grid form
    :param images: list of images
    :param height: number of images per column
    :param width: number of images per row
    """
    plt.subplots(figsize=(width * 2, height * 2))
    gs = gridspec.GridSpec(height, width)
    gs.update(wspace=0.05, hspace=0.05)
    for i, img in enumerate(images):
        ax = plt.subplot(gs[i])
        plt.axis('off')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_aspect('equal')
        plt.imshow(img)
