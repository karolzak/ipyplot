import numpy as np
import shortuuid
from numpy import str_

from .img_helpers import img_to_base64

try:
    from IPython.display import display, HTML
except Exception:  # pragma: no cover
    raise Exception('IPython not detected. Plotting without IPython is not possible')  # NOQA E501


def create_tabs(
        images,
        labels,
        custom_texts=None,
        max_imgs_per_tab=30,
        img_width=150,
        zoom_scale=2.5,
        force_b64=False,
        tabs_order=None):
    tab_id = shortuuid.uuid()

    if tabs_order is None:
        tabs_order = np.unique(labels)

    if custom_texts is None:
        custom_texts = np.asarray([None for _ in range(len(images))])

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
    """ % {'0': tab_id}

    for i in tab_ids:
        style_html += '#tab%s:checked ~ .tab.content%s,' % (i, i)
    style_html = style_html[:-1] + '{ display: block; }</style>'

    html += style_html

    active_tab = True
    for i, label in zip(tab_ids, tabs_order):
        html += '<input class="ipyplot-tab-%s" type="radio" name="tabs" id="tab%s"%s/>' % (tab_id, i, ' checked ' if active_tab else '')  # NOQA E501
        html += '<label class="ipyplot-tab-label-%s" for="tab%s">%s</label>' % (tab_id, i, label)  # NOQA E501
        active_tab = False

    active_tab = True
    for i, label in zip(tab_ids, tabs_order):
        html += '<div class="tab content%s">' % i  # NOQA E501
        active_tab = False

        tab_imgs_mask = labels == label
        html += create_imgs_grid(
            images=images[tab_imgs_mask],
            labels=list(range(0, max_imgs_per_tab)),
            max_images=max_imgs_per_tab,
            img_width=img_width,
            zoom_scale=zoom_scale,
            custom_texts=custom_texts[tab_imgs_mask],
            force_b64=force_b64)

        html += '</div>'

    html += '</div>'

    return html


def display_html(html):
    return display(HTML(html))


def create_img(
        image,
        label,
        width,
        grid_style_uuid,
        custom_text=None,
        force_b64=False):
    img_uuid = shortuuid.uuid()

    img_html = ""
    if custom_text is not None:
        img_html += '<h4 style="font-size: 12px">%s</h4>' % custom_text

    use_b64 = True
    # if image is a string (URL) display its URL
    if type(image) is str or type(image) is str_:
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
        img_html += '<img src="data:image/png;base64,%s"/>' % img_to_base64(image, width)  # NOQA E501

    html = """
    <div class="ipyplot-holder-%(0)s">
        <div id="ipyplot-image-%(0)s-%(1)s" class="ipyplot-imgbox-%(0)s">
            <a class="ipyplot-close" href="#"/>
            <a class="ipyplot-expand" href="#ipyplot-image-%(0)s-%(1)s"/>
            <h4 style="font-size: 12px">%(2)s</h4>
            %(3)s
        </div>
    </div>
    """ % {'0': grid_style_uuid, '1': img_uuid, '2': label, '3': img_html}
    return html


def create_imgs_grid(
        images,
        labels,
        custom_texts=None,
        max_images=30,
        img_width=150,
        zoom_scale=2.5,
        force_b64=False):
    if custom_texts is None:
        custom_texts = [None for _ in range(len(images))]
    html, grid_style_uuid = get_default_style(img_width, zoom_scale)
    html += '<div id="ipyplot-img-container-%s">' % grid_style_uuid
    html += ''.join([
        create_img(
            x, width=img_width, label=y,
            grid_style_uuid=grid_style_uuid,
            custom_text=text, force_b64=force_b64)
        for x, y, text in zip(
            images[:max_images], labels[:max_images],
            custom_texts[:max_images])
    ])
    html += '</div>'
    return html


def get_default_style(img_width, zoom_scale):
    style_uuid = shortuuid.uuid()
    html = """
        <style>
        #ipyplot-img-container-%(0)s {
            width: 100%%;
            height: 100%%;
            margin: 0%%;
            overflow: auto;
            position: relative;
            overflow-y:scroll;
        }

        .ipyplot-holder-%(0)s {
            /* The width and height, you can change these */
            width: %(1)spx;
            display: inline-block;
            margin: 5px;
            position: relative;
        }

        .ipyplot-imgbox-%(0)s {
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

        .ipyplot-imgbox-%(0)s img {
            /* Inherit the width and height from the parent element */
            width: 100%%;
        }

        .ipyplot-imgbox-%(0)s a {
            width: 100%%;
            height: 100%%;
            position: absolute;
            top: 0;
            left: 0;
        }

        .ipyplot-imgbox-%(0)s .ipyplot-close {
            display: none;
        }

        .ipyplot-imgbox-%(0)s .ipyplot-close:hover {
            cursor: zoom-out;
        }
        .ipyplot-imgbox-%(0)s .ipyplot-expand:hover {
            cursor: zoom-in;
        }

        div[id^=ipyplot-image-%(0)s]:target {
            width: 100%%;
            transform: scale(%(2)s);
            transform-origin: left top;
            z-index: 5000;
            top: 0;
            left: 0;
            position: absolute;
        }

        div[id^=ipyplot-image-%(0)s]:target .ipyplot-close {
            display: block;
        }

        div[id^=ipyplot-image-%(0)s]:target .ipyplot-expand {
            display: none;
        }
        </style>
    """ % {'0': style_uuid, '1': img_width, '2': zoom_scale}
    return html, style_uuid
