"""
Helper methods for working with images.
"""

import base64
import io

import numpy as np
from numpy import str_
import PIL
from PIL import Image


def _rescale_to_width(
        img: Image,
        target_width: int):
    """Helper function to rescale image to `target_width`.

    Parameters
    ----------
    img : PIL.Image
        Input image object to be rescaled.
    target_width : int
        Target width (in pixels) for rescaling.

    Returns
    -------
    PIL.Image
        Rescaled image object
    """
    w, h = img.size
    rescaled_img = img.resize(_scale_wh_by_target_width(w, h, target_width))
    return rescaled_img


def _scale_wh_by_target_width(w: int, h: int, target_width: int):
    """Helper functions for scaling width and height based on target width.

    Parameters
    ----------
    w : int
        Width in pixels.
    h : int
        Heights in pixels.
    target_width : int
        Target width (in pixels) for rescaling.

    Returns
    -------
    (int, int)
        Returns rescaled width and height as a tuple (w, h).
    """
    scale = target_width / w
    return int(w * scale), int(h * scale)


def _img_to_base64(
        image: str or str_ or np.ndarray or PIL.Image,
        target_width: int = None):
    """Converts image to base64 string.
    Use `target_width` param to rescale the image to specific width - keeps original size by default.

    Parameters
    ----------
    image : str or numpy.str_ or numpy.ndarray or PIL.Image
        Input image can be either PIL.Image, numpy.ndarray or simply a string URL to local or external image file.
    target_width : int, optional
        Target width (in pixels) to rescale to. If None image will not be rescaled.
        Defaults to None.

    Returns
    -------
    str
        Image as base64 string.
    """  # NOQA E501
    # if statements to convert image to PIL.Image object
    if isinstance(image, np.ndarray):
        if image.dtype in [np.float32, np.float64]:
            # if dtype is float and values range is from 0.0 to 1.0
            # we need to normalize it to 0-255 range
            image = image * 255 if image.max() <= 1.0 else image
            image = PIL.Image.fromarray(image.astype(np.uint8))
        else:
            image = PIL.Image.fromarray(image)
    elif type(image) is str or type(image) is str_:
        image = PIL.Image.open(image)

    # rescale image based on target_width
    if target_width:
        image = _rescale_to_width(image, target_width)
    # save image object to bytes stream
    output = io.BytesIO()
    image.save(output, format='PNG')
    # encode bytes as base64 string
    b64 = str(base64.b64encode(output.getvalue()).decode('utf-8'))
    return b64
