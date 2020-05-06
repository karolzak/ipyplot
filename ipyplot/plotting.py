import base64
import io
import uuid

import numpy as np
from numpy import str_
from PIL import Image

from .img_helpers import resize_with_aspect_ratio

try:
    from IPython.display import display, HTML
except Exception as e:
    raise Exception('IPython not detected. Plotting without IPython is not possible')  # NOQA E501

try:
    import google.colab
except:
    print("WARNING! Running in Google colab environment makes some of the functions impossible to run correctly")  # NOQA E501


def plot_class_tabs(images, labels, max_imgs_per_tab=10, img_width=220):
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
            Defaults to 50.
        img_width (int, optional):
            Image width.
            Adjust to change the number of images per row.
            Defaults to 220.
    """
    assert(len(images) == len(labels))
    assert(type(images) is np.ndarray)
    assert(type(labels) is np.ndarray)
    assert(type(max_imgs_per_tab) is int)
    assert(type(img_width) is int)
        
    html = _create_tabs_html(images, labels, max_imgs_per_tab, img_width)

    _display(html)


def plot_images(images, labels=None, max_images=30, img_width=300):
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
    """
    assert(type(max_images) is int)
    assert(type(img_width) is int)

    if labels is None:
        labels = list(range(0, len(images)))
    html = _create_imgs_list_html(images, labels, max_images, img_width)

    _display(html)


def plot_class_representations(
        images, labels,
        ignore_list=['-1', 'unknown'],
        img_width=150):
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
        img_width=img_width)


def _create_tabs_html(images, labels, max_imgs_per_tab, img_width):
    html = '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>'  # NOQA E501
    html = '<div><ul class="nav nav-pills">'

    unique_labels = np.unique(labels)
    tab_ids = [uuid.uuid4() for label in unique_labels]

    active_tab = True
    for i, label in zip(tab_ids, unique_labels):
        html += '<li class="active">' if active_tab else '<li>'
        active_tab = False
        html += '<a href="#%s" data-toggle="tab">%s</a></li>' % (i, label)
    html += '</ul><div class="tab-content clearfix">'

    active_tab = True
    for i, label in zip(tab_ids, unique_labels):
        html += '<div class="tab-pane active" id="%s">' % i if active_tab else '<div class="tab-pane" id="%s">' % i  # NOQA E501
        active_tab = False
        img_ids = list(range(0, len(images)))
        html += ''.join([
            _create_img_html(x, img_width, label=y)
            for x, y in zip(images[labels == label][:max_imgs_per_tab], img_ids)
        ])        
        html += '</div>'

    html += '</div></div>'

    return html


def _display(html):
    return display(HTML(html))


def _img_to_base64(image, max_size):
    if type(image) is np.ndarray:
        image = Image.fromarray(image)
    elif type(image) is str or type(image) is str_:
        image = Image.open(image)
    output = io.BytesIO()
    image = resize_with_aspect_ratio(image, max_size)
    image.save(output, format='PNG')
    b64 = str(base64.b64encode(output.getvalue()).decode('utf-8'))
    return b64


def _create_img_html(image, width, label):
    html = (
        '<div style="display: inline-block; width: %spx; text-align: center;">' % width +
        '<h4 style="font-size: 12px">%s</h4>' % label
    )
    if type(image) is str or type(image) is str_:
        html += '<h4 style="font-size: 9px; padding-left: 15px; padding-right: 15px; width: 100%%; word-wrap: break-word; white-space: normal;">%s</h4>' % (image)  # NOQA E501

    html += '<img src="data:image/png;base64,%s" style="margin: 1px; width: %spx; border: 2px solid #ddd;"/>' % (
        _img_to_base64(image, width*2), width)  # NOQA E501

    return html + '</div>'


def _create_imgs_list_html(images, labels, max_images, img_width):
    html = ''.join([
        _create_img_html(x, img_width, label=y)
        for x, y in zip(images[:max_images], labels[:max_images])
    ])
    return html
