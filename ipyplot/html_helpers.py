

import numpy as np
from numpy import str_
import shortuuid

from .img_helpers import img_to_base64

try:
    from IPython.display import display, HTML
except Exception:
    raise Exception('IPython not detected. Plotting without IPython is not possible')  # NOQA E501


def create_tabs(
        images, labels, max_imgs_per_tab, img_width, force_b64=False):
    # html = '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>'  # NOQA E501
    html = '<div>'
    tab_id = shortuuid.uuid()
    unique_labels = np.unique(labels)
    tab_ids = [shortuuid.uuid() for label in unique_labels]
    style_html = """
        <style>
            input.ipyplot-tab {
                display: none;
            }
            input.ipyplot-tab + label.ipyplot-tab-label {
                border: 1px solid #999;
                background: #EEE;
                padding: 4px 12px;
                border-radius: 4px 4px 0 0;
                position: relative;
                top: 1px;
            }
            input.ipyplot-tab:checked + label.ipyplot-tab-label {
                background: #FFF;
                border-bottom: 1px solid transparent;
            }
            input.ipyplot-tab ~ .tab {
                border-top: 1px solid #999;
                padding: 12px;
            }

            input.ipyplot-tab ~ .tab {
                display: none
            }
    """

    for i in tab_ids:
        style_html += '#tab%s:checked ~ .tab.content%s,' % (i, i)
    style_html = style_html[:-1] + '{ display: block; }</style>'

    html += style_html

    active_tab = True
    for i, label in zip(tab_ids, unique_labels):
        html += '<input class="ipyplot-tab" type="radio" name="tabs" id="tab%s"%s/>' % (i, ' checked ' if active_tab else '')  # NOQA E501
        html += '<label class="ipyplot-tab-label" for="tab%s">%s</label>' % (i, label)  # NOQA E501
        active_tab = False

    active_tab = True
    for i, label in zip(tab_ids, unique_labels):
        html += '<div class="tab content%s">' % i  # NOQA E501
        active_tab = False

        html += create_imgs_grid(
            images[labels == label], list(range(0, max_imgs_per_tab)),
            max_imgs_per_tab, img_width, force_b64=force_b64)

        # html += ''.join([
        #     create_img(x, img_width, label=y, force_b64=force_b64)
        #     for y, x in enumerate(images[labels == label][:max_imgs_per_tab])
        # ])        
        html += '</div>'

    html += '</div>'

    return html


def display_html(html):
    return display(HTML(html))


def create_img(image, width, label, force_b64=False):
    img_uuid = shortuuid.uuid()

    img_html = ""
    use_b64 = True
    if type(image) is str or type(image) is str_:
        img_html += '<h4 style="font-size: 9px; padding-left: 10px; padding-right: 10px; width: 95%%; word-wrap: break-word; white-space: normal;">%s</h4>' % (image)  # NOQA E501
        if not force_b64:
            use_b64 = False
            img_html += '<img src="%s"/>' % image
        elif "http" in image:
            print("WARNING: Current implementation doesn't allow to use 'force_b64=True' with images as internet URIs. Ignoring 'force_b64' flag")  # NOQA E501
            use_b64 = False

    if use_b64:
        img_html += '<img src="data:image/png;base64,%s"/>' % img_to_base64(image, width)  # NOQA E501

    html = """
    <div class="holder">
        <div id="ipyplot-image-%s" class="ipyplot-imgbox">
            <a class="ipyplot-close" href="#"/>
            <a class="ipyplot-expand" href="#ipyplot-image-%s"/>
            <h4 style="font-size: 12px">%s</h4>
            %s
        </div>
    </div>
    """ % (img_uuid, img_uuid, label, img_html)

    return html


def create_imgs_grid(
        images, labels, max_images, img_width, force_b64=False):
    html = get_default_style(img_width)
    html += '<div id="ipyplot-img-container">'
    html += ''.join([
        create_img(x, width=img_width, label=y, force_b64=force_b64)
        for x, y in zip(images[:max_images], labels[:max_images])
    ])
    html += '</div>'
    return html


def get_default_style(img_width):
    style_uuid = shortuuid.uuid()
    html = """
        <style>
        #ipyplot-img-container {
            width: 100%%;
            height: 100%%;
            margin: 0%%;
            overflow: auto;
            position: relative;
        }

        .holder {
            /* The width and height, you can change these */
            width: %spx;
            display: inline-block;
            margin: 5px;
            position: relative;
        }

        .ipyplot-imgbox {
            /* Inherit width and height from the .holder */
            background: white;
            display: inline-block;
            vertical-align: top;
            text-align: center;
            width: inherit;
            position: relative;
            border: 2px solid #ddd;
            top: 0;
            left: 0;
        }

        .ipyplot-imgbox img {
            /* Inherit the width and height from the parent element */
            width: inherited;
        }

        .ipyplot-imgbox a {
            width: 100%%;
            height: 100%%;
            position: absolute;
            top: 0;
            left: 0;
        }

        .ipyplot-imgbox .ipyplot-close {
            display: none;
        }

        .ipyplot-imgbox .ipyplot-close:hover {
            cursor: zoom-out;
        }
        .ipyplot-imgbox .ipyplot-expand:hover {
            cursor: zoom-in;
        }

        div[id^=ipyplot-image]:target {
            width: 100%%;
            transform: scale(2.5);
            transform-origin: left top;
            z-index: 5000;
            top: 0;
            left: 0;
            position: absolute;
        }

        div[id^=ipyplot-image]:target .ipyplot-close {
            display: block;
        }

        div[id^=ipyplot-image]:target .ipyplot-expand {
            display: none;
        }
        </style>
    """ % (img_width)
    return html
