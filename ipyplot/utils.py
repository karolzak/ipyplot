from typing import Sequence

import numpy as np
from PIL import Image


def get_class_representations(
        images: Sequence[object],
        labels: Sequence[str or int],
        ignore_list: Sequence[str or int],
        labels_order: Sequence[str or int]):

    images = np.asarray(images)
    labels = np.asarray(labels)
    ignore_list = np.asarray(ignore_list) if ignore_list is not None else ignore_list  # NOQA E501
    labels_order = np.asarray(labels_order) if labels_order is not None else labels_order  # NOQA E501

    if ignore_list is not None:
        not_labeled_mask = np.isin(labels, ignore_list)
        labels = labels[~not_labeled_mask]
        images = images[~not_labeled_mask]

    if labels_order is not None:
        labels_order_mask = [
            np.where(labels == label)[0][0]
            for label in labels_order
            if len(np.where(labels == label)[0]) > 0
        ]
        out_images = images[labels_order_mask]
        out_labels = labels[labels_order_mask]
    else:
        uniques = np.unique(labels, return_index=True)
        out_labels = uniques[0]
        out_images = images[uniques[1]]

    return out_images, out_labels


def seq2arr(seq: Sequence[str or int or object]):
    # this is a hack to make the code work with PIL images
    if issubclass(type(seq[0]), Image.Image):
        return np.asarray(seq, dtype=type(seq[0]))
    else:
        return np.asarray(seq)
