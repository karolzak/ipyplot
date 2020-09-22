import numpy as np
from typing import Sequence


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
