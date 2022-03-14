"""
This module contains helper functions for generating HTML code
required for displaying images, grid/tab layout and general styling.
"""

from typing import Sequence

import os
import numpy as np
import shortuuid
from numpy import str_

from ._img_helpers import _img_to_base64

try:
    from IPython.display import display, HTML
except Exception:  # pragma: no cover
    raise Exception('IPython not detected. Plotting without IPython is not possible')  # NOQA E501


def _create_tabs(
        images: Sequence[object],
        labels: Sequence[str or int],
        custom_texts: Sequence[str] = None,
        max_imgs_per_tab: int = 30,
        img_width: int = 150,
        zoom_scale: float = 2.5,
        show_url: bool = True,
        force_b64: bool = False,
        tabs_order: Sequence[str or int] = None,
        resize_image: bool = False):
    """
    Generates HTML code required to display images in interactive tabs grouped by labels.
    For tabs ordering and filtering check out `tabs_order` param.

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
    resize_image : bool, optional
        If `True` it will resize image based on `width` parameter.
        Useful when working with big images and notebooks getting too big in terms of file size.
        Defaults to `False`.
    """  # NOQA E501

    tab_layout_id = shortuuid.uuid()

    # if `tabs_order` is None use sorted unique values from `labels`
    if tabs_order is None:
        tabs_order = np.unique(labels)

    # assure same length for images, labels and custom_texts sequences
    assert(len(labels) == len(images))
    if custom_texts is not None:
        assert(len(custom_texts) == len(images))

    html = '<div>'
    tab_ids = [shortuuid.uuid() for label in tabs_order]
    style_html = """
        <style>
            input.ipyplot-tab-%(0)s {
                display: none;
            }
            input.ipyplot-tab-%(0)s + label.ipyplot-tab-label-%(0)s {
                border: 1px solid #999;
                background: #EEE;
                padding: 4px 12px;
                border-radius: 4px 4px 0 0;
                position: relative;
                top: 1px;
            }
            input.ipyplot-tab-%(0)s:checked + label.ipyplot-tab-label-%(0)s {
                background: #FFF;
                border-bottom: 1px solid transparent;
            }
            input.ipyplot-tab-%(0)s ~ .tab {
                border-top: 1px solid #999;
                padding: 12px;
            }

            input.ipyplot-tab-%(0)s ~ .tab {
                display: none
            }
    """ % {'0': tab_layout_id}

    for i in tab_ids:
        style_html += '#tab%s:checked ~ .tab.content%s,' % (i, i)
    style_html = style_html[:-1] + '{ display: block; }</style>'

    html += style_html

    # sets the first tab to active/selected state
    active_tab = True
    for i, label in zip(tab_ids, tabs_order):
        # define radio type tab buttons for each label
        html += '<input class="ipyplot-tab-%s" type="radio" name="tabs-%s" id="tab%s"%s/>' % (tab_layout_id, tab_layout_id, i, ' checked ' if active_tab else '')  # NOQA E501
        html += '<label class="ipyplot-tab-label-%s" for="tab%s">%s</label>' % (tab_layout_id, i, label)  # NOQA E501
        active_tab = False

    # sets the first tab to active/selected state
    active_tab = True
    for i, label in zip(tab_ids, tabs_order):
        # define content for each tab
        html += '<div class="tab content%s">' % i  # NOQA E501
        active_tab = False

        tab_imgs_mask = labels == label
        html += _create_imgs_grid(
            images=images[tab_imgs_mask],
            labels=list(range(0, max_imgs_per_tab)),
            max_images=max_imgs_per_tab,
            img_width=img_width,
            zoom_scale=zoom_scale,
            custom_texts=custom_texts[tab_imgs_mask] if custom_texts is not None else None,  # NOQA E501
            show_url=show_url,
            force_b64=force_b64)

        html += '</div>'

    html += '</div>'

    return html


def _create_html_viewer(
        html: str):
    """Creates HTML code for HTML previewer.

    Parameters
    ----------
    html : str
        HTML content to be displayed in HTML viewer.

    Returns
    -------
    str
        HTML code for HTML previewer control.
    """

    html_viewer_id = shortuuid.uuid()
    html_viewer = """
    <style>
        #ipyplot-html-viewer-toggle-%(1)s {
            position: absolute;
            top: -9999px;
            left: -9999px;
            visibility: hidden;
        }

        #ipyplot-html-viewer-label-%(1)s { 
            position: relative;
            display: inline-block;
            cursor: pointer;
            color: blue;
            text-decoration: underline;
        }

        #ipyplot-html-viewer-textarea-%(1)s {
            background: lightgrey;
            width: 100%%;
            height: 0px;
            display: none;
        }

        #ipyplot-html-viewer-toggle-%(1)s:checked ~ #ipyplot-html-viewer-textarea-%(1)s {
            height: 200px;
            display: block;
        }

        #ipyplot-html-viewer-toggle-%(1)s:checked + #ipyplot-html-viewer-label-%(1)s:after {
            content: "hide html";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: white;
            cursor: pointer;
            color: blue;
            text-decoration: underline;
        }
    </style>
    <div>
        <input type="checkbox" id="ipyplot-html-viewer-toggle-%(1)s">
        <label id="ipyplot-html-viewer-label-%(1)s" for="ipyplot-html-viewer-toggle-%(1)s">show html</label>
        <textarea id="ipyplot-html-viewer-textarea-%(1)s" readonly>
            %(0)s
        </textarea>
    </div>
    """ % {'0': html, '1': html_viewer_id}  # NOQA E501
    return html_viewer


def _display_html(html: str):
    """Simply displays provided HTML string using IPython.display function.

    Parameters
    ----------
    html : str
        HTML code to be displayed.

    Returns
    -------
    handle: DisplayHandle
        Returns a handle on updatable displays
    """
    display(HTML(_create_html_viewer(html)))
    return display(HTML(html))


def _create_img(
        image: str or object,
        label: str or int,
        width: int,
        grid_style_uuid: str,
        custom_text: str = None,
        show_url: bool = True,
        force_b64: bool = False,
        resize_image: bool = False):
    """Helper function to generate HTML code for displaying images along with corresponding texts.

    Parameters
    ----------
    image : str or object
        Image object or string URL to local/external image file.
    label : str or int
        Label/class string to be displayed above the image.
    width : int
        Image width value in pixels.
    grid_style_uuid : str
        Unique identifier used to connect image style with specific style definition.
    custom_text : str, optional
        Additional text to be displayed above the image but below the label name.
        Defaults to None.
    show_url : bool, optional
        Defines if the urls are displayed as text above the images. 
    force_b64 : bool, optional
        You can force conversion of images to base64 instead of reading them directly from filepaths with HTML.  
        Do mind that using b64 conversion vs reading directly from filepath will be slower.
        You might need to set this to `True` in environments like Google colab.
        Defaults to False.
    resize_image : bool, optional
        If `True` it will resize image based on `width` parameter.
        Useful when working with big images and notebooks getting too big in terms of file size.
        Defaults to `False`.

    Returns
    -------
    str
        Output HTML code.
    """  # NOQA E501
    if width is None:
        raise ValueError("`img_width` can't be `None`!")

    img_uuid = shortuuid.uuid()

    img_html = ""
    if custom_text is not None:
        img_html += '<h4 style="font-size: 12px; word-wrap: break-word;">%s</h4>' % str(custom_text)  # NOQA E501

    use_b64 = True

    if type(image) is str or type(image) is str_:
        # if image url is local path convert to relative path
        matches = ['http:', 'https:', 'ftp:', 'www.', 'data:', 'file:']
        if not any(image.lower().startswith(x) for x in matches):
            image = os.path.relpath(image)
        if show_url:
            img_html += '<h4 style="font-size: 9px; padding-left: 10px; padding-right: 10px; width: 95%%; word-wrap: break-word; white-space: normal;">%s</h4>' % (image)  # NOQA E501
        if not force_b64:
            use_b64 = False
            img_html += '<img src="%s"/>' % image
        elif "http" in image:
            print("WARNING: Current implementation doesn't allow to use 'force_b64=True' with images as remote URLs. Ignoring 'force_b64' flag")  # NOQA E501
            use_b64 = False

    # if image is not a string it means its either PIL.Image or np.ndarray
    # that's why it's necessary to use conversion to b64
    if use_b64:
        img_html += '<img src="data:image/png;base64,%s"/>' % _img_to_base64(
            image,
            width if resize_image else None)

    html = """
    <div class="ipyplot-placeholder-div-%(0)s">
        <div id="ipyplot-content-div-%(0)s-%(1)s" class="ipyplot-content-div-%(0)s">
            <h4 style="font-size: 12px; word-wrap: break-word;">%(2)s</h4>
            %(3)s
            <a href="#!">
                <span class="ipyplot-img-close"/>
            </a>
            <a href="#ipyplot-content-div-%(0)s-%(1)s">
                <span class="ipyplot-img-expand"/>
            </a>
        </div>
    </div>
    """ % {'0': grid_style_uuid, '1': img_uuid, '2': label, '3': img_html}  # NOQA E501
    return html


def _create_imgs_grid(
        images: Sequence[object],
        labels: Sequence[str or int],
        custom_texts: Sequence[str] = None,
        max_images: int = 30,
        img_width: int = 150,
        zoom_scale: float = 2.5,
        show_url: bool = True,
        force_b64: bool = False,
        resize_image: bool = False):
    """
    Creates HTML code for displaying images provided in `images` param in grid-like layout.
    Check optional params for max number of images to plot, labels and custom texts to add to each image, image width and other options.

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
    resize_image : bool, optional
        If `True` it will resize image based on `width` parameter.
        Useful when working with big images and notebooks getting too big in terms of file size.
        Defaults to `False`.

    Returns
    -------
    str
        Output HTML code.
    """  # NOQA E501

    if custom_texts is None:
        custom_texts = [None for _ in range(len(images))]

    # create code with style definitions
    html, grid_style_uuid = _get_default_style(img_width, zoom_scale)

    html += '<div id="ipyplot-imgs-container-div-%s">' % grid_style_uuid
    html += ''.join([
        _create_img(
            x, width=img_width, label=y,
            grid_style_uuid=grid_style_uuid,
            custom_text=text, show_url=show_url,
            force_b64=force_b64,
            resize_image=resize_image
        )
        for x, y, text in zip(
            images[:max_images], labels[:max_images],
            custom_texts[:max_images])
    ])
    html += '</div>'
    return html


def _get_default_style(img_width: int, zoom_scale: float):
    """Creates HTML code with default style definitions required for elements to be properly displayed

    Parameters
    ----------
    img_width : int
        Image width in pixels.
    zoom_scale : float
        Scale for zoom-in-on-click feature.
        Best to keep between 1.0~5.0.

    Returns
    -------
    str
        Output HTML code.
    """  # NOQA E501
    style_uuid = shortuuid.uuid()
    html = """
        <style>
        #ipyplot-imgs-container-div-%(0)s {
            width: 100%%;
            height: 100%%;
            margin: 0%%;
            overflow: auto;
            position: relative;
            overflow-y: scroll;
        }

        div.ipyplot-placeholder-div-%(0)s {
            width: %(1)spx;
            display: inline-block;
            margin: 3px;
            position: relative;
        }

        div.ipyplot-content-div-%(0)s {
            width: %(1)spx;
            background: white;
            display: inline-block;
            vertical-align: top;
            text-align: center;
            position: relative;
            border: 2px solid #ddd;
            top: 0;
            left: 0;
        }

        div.ipyplot-content-div-%(0)s span.ipyplot-img-close {
            display: none;
        }

        div.ipyplot-content-div-%(0)s span {
            width: 100%%;
            height: 100%%;
            position: absolute;
            top: 0;
            left: 0;
        }

        div.ipyplot-content-div-%(0)s img {
            width: %(1)spx;
        }

        div.ipyplot-content-div-%(0)s span.ipyplot-img-close:hover {
            cursor: zoom-out;
        }
        div.ipyplot-content-div-%(0)s span.ipyplot-img-expand:hover {
            cursor: zoom-in;
        }

        div[id^=ipyplot-content-div-%(0)s]:target {
            transform: scale(%(2)s);
            transform-origin: left top;
            z-index: 5000;
            top: 0;
            left: 0;
            position: absolute;
        }

        div[id^=ipyplot-content-div-%(0)s]:target span.ipyplot-img-close {
            display: block;
        }

        div[id^=ipyplot-content-div-%(0)s]:target span.ipyplot-img-expand {
            display: none;
        }
        </style>
    """ % {'0': style_uuid, '1': img_width, '2': zoom_scale}
    return html, style_uuid
