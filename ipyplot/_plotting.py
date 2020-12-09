"""
This is the main module of IPyPlot package.
It contains all the user-facing functions for displaying images in Python Notebooks.
"""  # NOQA E501

import numpy as _np
from typing import Sequence

from ._html_helpers import (
    _display_html, _create_tabs, _create_imgs_grid)
from ._utils import _get_class_representations, _seq2arr


def plot_class_tabs(
        images: Sequence[object],
        labels: Sequence[str or int],
        custom_texts: Sequence[str] = None,
        max_imgs_per_tab: int = 30,
        img_width: int = 150,
        zoom_scale: float = 2.5,
        show_url: bool = True,
        force_b64: bool = False,
        tabs_order: Sequence[str or int] = None):
    """
    Efficient and convenient way of displaying images in interactive tabs grouped by labels.
    For tabs ordering and filtering check out `tabs_order` param.
    This function (same as the whole IPyPlot package) is using IPython and HTML under the hood.

    Parameters
    ----------
    images : Sequence[object]
        List of images to be displayed in tabs layout.
        Currently supports images in the following formats:
        - str (local/remote URL)
        - PIL.Image
        - numpy.ndarray
    labels : Sequence[str or int]
        List of classes/labels for images to be grouped by.
        Must be same length as `images`.
    custom_texts : Sequence[str], optional
        List of custom strings to be drawn above each image.
        Must be same length as `images`, by default `None`.
    max_imgs_per_tab : int, optional
        How many samples from each label/class to display in a tab
        Defaults to 30.
    img_width : int, optional
        Image width in px, by default 150
    zoom_scale : float, optional
        Scale for zoom-in-on-click feature.
        Best to keep between 1.0~5.0.
        Defaults to 2.5.
    show_url : bool, optional
        Defines if the urls are displayed as text above the images. 
    force_b64 : bool, optional
        You can force conversion of images to base64 instead of reading them directly from filepaths with HTML.  
        Do mind that using b64 conversion vs reading directly from filepath will be slower.
        You might need to set this to `True` in environments like Google colab.
        Defaults to False.
    tabs_order : Sequence[str or int], optional
        Order of tabs based on provided list of classes/labels.
        By default, tabs will be sorted alphabetically based on provided labels.
        This param can be also used as a filtering mechanism - only labels provided in `tabs_order` param will be displayed as tabs.
        Defaults to None.
    """  # NOQA E501
    assert(len(images) == len(labels))

    # convert to numpy.ndarray for further processing
    images = _seq2arr(images)
    labels = _np.asarray(labels)
    tabs_order = _np.asarray(tabs_order) if tabs_order is not None else tabs_order  # NOQA E501
    custom_texts = _np.asarray(custom_texts) if custom_texts is not None else custom_texts  # NOQA E501

    # run html helper function to generate html content
    html = _create_tabs(
        images=images,
        labels=labels,
        custom_texts=custom_texts,
        max_imgs_per_tab=max_imgs_per_tab,
        img_width=img_width,
        zoom_scale=zoom_scale,
        show_url=show_url,
        force_b64=force_b64,
        tabs_order=tabs_order)

    _display_html(html)


def plot_images(
        images: Sequence[object],
        labels: Sequence[str or int] = None,
        custom_texts: Sequence[str] = None,
        max_images: int = 30,
        img_width: int = 150,
        zoom_scale: float = 2.5,
        show_url: bool = True,
        force_b64: bool = False):
    """
    Simply displays images provided in `images` param in grid-like layout.
    Check optional params for max number of images to plot, labels and custom texts to add to each image, image width and other options.
    This function (same as the whole IPyPlot package) is using IPython and HTML under the hood.

    Parameters
    ----------
    images : Sequence[object]
        List of images to be displayed in tabs layout.
        Currently supports images in the following formats:
        - str (local/remote URL)
        - PIL.Image
        - numpy.ndarray
    labels : Sequence[str or int], optional
        List of classes/labels for images to be grouped by.
        Must be same length as `images`.
        Defaults to None.
    custom_texts : Sequence[str], optional
        List of custom strings to be drawn above each image.
        Must be same length as `images`, by default `None`.
    max_images : int, optional
        How many images to display (takes first N images).
        Defaults to 30.
    img_width : int, optional
        Image width in px, by default 150
    zoom_scale : float, optional
        Scale for zoom-in-on-click feature.
        Best to keep between 1.0~5.0.
        Defaults to 2.5.
    show_url : bool, optional
        Defines if the urls are displayed as text above the images. 
    force_b64 : bool, optional
        You can force conversion of images to base64 instead of reading them directly from filepaths with HTML.  
        Do mind that using b64 conversion vs reading directly from filepath will be slower.
        You might need to set this to `True` in environments like Google colab.
        Defaults to False.
    """  # NOQA E501

    images = _seq2arr(images)

    if labels is None:
        labels = list(range(0, len(images)))
    else:
        labels = _np.asarray(labels)

    custom_texts = _np.asarray(custom_texts) if custom_texts is not None else custom_texts  # NOQA E501

    html = _create_imgs_grid(
        images=images,
        labels=labels,
        custom_texts=custom_texts,
        max_images=max_images,
        img_width=img_width,
        zoom_scale=zoom_scale,
        show_url=show_url,
        force_b64=force_b64)

    _display_html(html)


def plot_class_representations(
        images: Sequence[object],
        labels: Sequence[str or int],
        img_width: int = 150,
        zoom_scale: float = 2.5,
        show_url: bool = True,
        force_b64: bool = False,
        ignore_labels: Sequence[str or int] = None,
        labels_order: Sequence[str or int] = None):
    """
    Displays single image (first occurence for each class) for each label/class in grid-like layout.
    Check optional params for labels filtering, ignoring and ordering, image width and other options.
    This function (same as the whole IPyPlot package) is using IPython and HTML under the hood.

    Parameters
    ----------
    images : Sequence[object]
        List of images to be displayed in tabs layout.
        Currently supports images in the following formats:
        - str (local/remote URL)
        - PIL.Image
        - numpy.ndarray
    labels : Sequence[str or int]
        List of classes/labels for images to be grouped by.
        Must be same length as `images`.
    img_width : int, optional
        Image width in px, by default 150
    zoom_scale : float, optional
        Scale for zoom-in-on-click feature.
        Best to keep between 1.0~5.0.
        Defaults to 2.5.
    show_url : bool, optional
        Defines if the urls are displayed as text above the images. 
    force_b64 : bool, optional
        You can force conversion of images to base64 instead of reading them directly from filepaths with HTML.  
        Do mind that using b64 conversion vs reading directly from filepath will be slower.
        You might need to set this to `True` in environments like Google colab.
        Defaults to False.
    ignore_labels : Sequence[str or int], optional
        List of labels to ignore.
        Defaults to None.
    labels_order : Sequence[str or int], optional
        Defines order of labels based on provided list of classes/labels.
        By default, images will be sorted alphabetically based on provided label.
        This param can be also used as a filtering mechanism - only images for labels provided in `labels_order` param will be displayed.
        Defaults to None.
    """  # NOQA E501

    assert(len(images) == len(labels))

    images = _seq2arr(images)

    labels = _np.asarray(labels)
    ignore_labels = _np.asarray(ignore_labels) if ignore_labels is not None else ignore_labels  # NOQA E501
    labels_order = _np.asarray(labels_order) if labels_order is not None else labels_order  # NOQA E501

    images, labels = _get_class_representations(
        images, labels, ignore_labels, labels_order)

    plot_images(
        images=images,
        labels=labels,
        max_images=len(images),
        img_width=img_width,
        zoom_scale=zoom_scale,
        show_url=show_url,
        force_b64=force_b64)
