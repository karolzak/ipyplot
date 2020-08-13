import numpy as np

from .html_helpers import (
    display_html, create_img, create_tabs, create_imgs_grid)


def plot_class_tabs(
        images,
        labels,
        max_imgs_per_tab=10,
        img_width=220,
        force_b64=False):
    """
    Efficient and convenient way of displaying images in interactive tabs
    grouped by labels/clusters.
    It's using IPython.display function and HTML under the hood

    Args:
        images (numpy.ndarray):
            Numpy array of image file paths or PIL.Image objects
        labels (numpy.ndarray):
            Numpy array of corresponding classes
        max_imgs_per_tab (int, optional):
            How many samples from each cluster/class to display.
            Defaults to 10.
        img_width (int, optional):
            Image width.
            Adjust to change the number of images per row.
            Defaults to 220.
        force_b64 (boolean, optional):
            You can force conversion of images to base64 instead of reading them directly from filepaths with HTML.  # NOQA E501
            Do mind that using b64 conversion vs reading directly from filepath will be slower.  # NOQA E501
            You might need to set this to `True` in environments like Google colab.
            Defaults to False.
    """
    assert(len(images) == len(labels))
    assert(type(images) is np.ndarray)
    assert(type(labels) is np.ndarray)
    assert(type(max_imgs_per_tab) is int)
    assert(type(img_width) is int)

    html = create_tabs(
        images, labels, max_imgs_per_tab, img_width, force_b64=force_b64)

    display_html(html)


def plot_images(
        images,
        labels=None,
        max_images=30,
        img_width=300,
        force_b64=False):
    """
    Displays images based on the provided paths

    Args:
        images (array):
            Array of coresponding file paths.
        labels (array, optional):
            Array of labels/cluster names.
            If None it will just assign numbers going from 0
            Defaults to None.
        max_images (int, optional):
            Max number of images to display.
            Defaults to 100.
        img_width (int, optional):
            Width of the displayed image.
            Defaults to 300.
        force_b64 (boolean, optional):
            You can force conversion of images to base64 instead of reading them directly from filepaths with HTML.  # NOQA E501
            Do mind that using b64 conversion vs reading directly from filepath will be slower.  # NOQA E501
            You might need to set this to `True` in environments like Google colab.
            Defaults to False.
    """
    assert(type(max_images) is int)
    assert(type(img_width) is int)

    if labels is None:
        labels = list(range(0, len(images)))
    html = create_imgs_grid(
        images, labels, max_images, img_width, force_b64=force_b64)

    display_html(html)


def plot_class_representations(
        images, labels,
        ignore_list=['-1', 'unknown'],
        img_width=150,
        force_b64=False):
    """
    Function used to display first image from each cluster/class

    Args:
        images (array):
            Array of image file paths or PIL.Image objects.
        labels (array):
            Array of labels/classes names.
        ignore_list (list, optional):
            List of classes to ignore when plotting.
            Defaults to ['-1', 'unknown'].
        img_width (int, optional):
            Width of the displayed image.
            Defaults to 150.
        force_b64 (boolean, optional):
            You can force conversion of images to base64 instead of reading them directly from filepaths with HTML.  # NOQA E501
            Do mind that using b64 conversion vs reading directly from filepath will be slower.  # NOQA E501
            You might need to set this to `True` in environments like Google colab.
            Defaults to False.
    """
    assert(len(images) == len(labels))
    assert(type(ignore_list) is list or ignore_list is None)
    assert(type(img_width) is int)

    uniques = np.unique(labels, return_index=True)
    labels = uniques[0]
    not_labeled_mask = np.isin(labels, ignore_list)
    labels = labels[~not_labeled_mask]
    idices = uniques[1][~not_labeled_mask]

    group = []
    for img_path in images[idices]:
        group.append(img_path)

    plot_images(
        group,
        labels=labels,
        max_images=len(group),
        img_width=img_width,
        force_b64=force_b64)
