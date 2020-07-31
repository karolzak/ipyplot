import uuid

import numpy as np
from numpy import str_

from .img_helpers import img_to_base64

try:
    from IPython.display import display, HTML
except Exception:
    raise Exception('IPython not detected. Plotting without IPython is not possible')  # NOQA E501


def create_tabs(
        images, labels, max_imgs_per_tab, img_width, force_b64=False):
    # html = '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>'  # NOQA E501
    html = '<div>'

    unique_labels = np.unique(labels)
    tab_ids = [uuid.uuid4() for label in unique_labels]
    style_html = """
        <style>
            input { display: none; }
            input + label { display: inline-block }

            input + label {
            border: 1px solid #999;
            background: #EEE;
            padding: 4px 12px;
            border-radius: 4px 4px 0 0;
            position: relative;
            top: 1px;
            }
            input:checked + label {
            background: #FFF;
            border-bottom: 1px solid transparent;
            }
            input ~ .tab {
            border-top: 1px solid #999;
            padding: 12px;
            }

            input ~ .tab { display: none }
        """

    for i in tab_ids:
        style_html += '#tab%s:checked ~ .tab.content%s,' % (i, i)
    style_html = style_html[:-1] + '{ display: block; }</style>'

    html += style_html

    active_tab = True
    for i, label in zip(tab_ids, unique_labels):
        html += '<input type="radio" name="tabs" id="tab%s"%s/>' % (i, ' checked ' if active_tab else '')  # NOQA E501
        html += '<label for="tab%s">%s</label>' % (i, label)
        active_tab = False

    active_tab = True
    for i, label in zip(tab_ids, unique_labels):
        html += '<div class="tab content%s">' % i  # NOQA E501
        active_tab = False

        html += ''.join([
            create_img(x, img_width, label=y, force_b64=force_b64)
            for y, x in enumerate(images[labels == label][:max_imgs_per_tab])
        ])        
        html += '</div>'

    html += '</div>'

    return html


def display_html(html):
    return display(HTML(html))


def create_img(image, width, label, force_b64=False):
    html = (
        '<div style="display: inline-block; width: %spx; vertical-align: top; text-align: center;">' % (width + 20) +  # NOQA E501
        '<h4 style="font-size: 12px">%s</h4>' % label  # NOQA E501
    )
    use_b64 = True
    if type(image) is str or type(image) is str_:
        html += '<h4 style="font-size: 9px; padding-left: 10px; padding-right: 10px; width: 90%%; word-wrap: break-word; white-space: normal;">%s</h4>' % (image)  # NOQA E501
        if not force_b64:
            use_b64 = False
            html += '<img src="%s" style="margin: 1px; width: %spx; border: 2px solid #ddd;"/>' % (image, width)  # NOQA E501
        elif "http" in image:
            print("WARNING: Current implementation doesn't allow to use 'force_b64=True' with images as internet URIs. Ignoring 'force_b64' flag")  # NOQA E501
            use_b64 = False

    if use_b64:
        html += '<img src="data:image/png;base64,%s" style="margin: 1px; width: %spx; border: 2px solid #ddd;"/>' % (
            img_to_base64(image, width*2), width)  # NOQA E501

    return html + '</div>'


def create_imgs_list(
        images, labels, max_images, img_width, force_b64=False):
    html = ''.join([
        create_img(x, img_width, label=y, force_b64=force_b64)
        for x, y in zip(images[:max_images], labels[:max_images])
    ])
    return html
