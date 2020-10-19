"""
Misc utils for IPyPlot package.
"""

from typing import Sequence

import numpy as np
from PIL import Image


def _get_class_representations(
        images: Sequence[object],
        labels: Sequence[str or int],
        ignore_labels: Sequence[str or int] = None,
        labels_order: Sequence[str or int] = None):
    """Returns a list of images (and labels) representing first occurance of each label/class type.
    Check optional params for labels ignoring and ordering.
    For labels filtering refer to `labels_order` param.

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
    ignore_labels : Sequence[str or int], optional
        List of labels to ignore.
        Defaults to None.
    labels_order : Sequence[str or int], optional
        Defines order of labels based on provided list of classes/labels.
        By default, images will be sorted alphabetically based on provided label.
        This param can be also used as a filtering mechanism - only images for labels provided in `labels_order` param will be displayed.
        Defaults to None.

    Returns
    -------
    (numpy.ndarray, numpy.ndarray)
        Returns a tuple containing an array of images along with associated labels (out_images, out_labels).
    """  # NOQA E501

    # convert everything to numpy.ndarray
    # required for further filtering and ordering operations
    images = np.asarray(images)
    labels = np.asarray(labels)
    ignore_labels = np.asarray(ignore_labels) if ignore_labels is not None else ignore_labels  # NOQA E501
    labels_order = np.asarray(labels_order) if labels_order is not None else labels_order  # NOQA E501

    # ignore labels based on provided list
    if ignore_labels is not None:
        not_labeled_mask = np.isin(labels, ignore_labels)
        labels = labels[~not_labeled_mask]
        images = images[~not_labeled_mask]

    if labels_order is not None:
        # create idices mask based on ordered labels provided
        labels_order_mask = [
            np.where(labels == label)[0][0]
            for label in labels_order
            if len(np.where(labels == label)[0]) > 0
        ]
        # note that this will not only order labels and images
        # but it will filter them as well
        out_images = images[labels_order_mask]
        out_labels = labels[labels_order_mask]
    else:
        # if no filtering/ordering was provided
        # use uniques from labels list as indices mask
        uniques = np.unique(labels, return_index=True)
        out_labels = uniques[0]
        out_images = images[uniques[1]]

    return out_images, out_labels


def _seq2arr(seq: Sequence[str or int or object]):
    """Convert sequence to numpy.ndarray.

    Parameters
    ----------
    seq : Sequence[str or int or object]
        Input sequence of elements

    Returns
    -------
    numpy.ndarray
        Array of elements
    """
    # this is a hack to make the code work with PIL images
    if issubclass(type(seq[0]), Image.Image):
        return np.asarray(seq, dtype=type(seq[0]))
    else:
        return np.asarray(seq)
