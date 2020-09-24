import base64
import io

import numpy as np
from numpy import str_
from PIL import Image


def resize_with_aspect_ratio(img, max_size=1000):
    """Helper function to resize image against the longer edge

    Args:
        img (PIL.Image):
            Image object to be resized
        max_size (int, optional):
            Max size of the longer edge in pixels.
            Defaults to 1000.

    Returns:
        PIL.Image:
            Resized image object
    """
    w, h = img.size
    aspect_ratio = min(max_size/w, max_size/h)
    resized_img = img.resize(
        (int(w * aspect_ratio), int(h * aspect_ratio))
    )
    return resized_img


def img_to_base64(image, max_size):
    if type(image) is np.ndarray:
        if image.dtype in [np.float, np.float32, np.float64]:
            image = image * 255 if image.max() <= 1.0 else image
            image = Image.fromarray(image.astype(np.uint8))
        else:
            image = Image.fromarray(image)
    elif type(image) is str or type(image) is str_:
        image = Image.open(image)
    output = io.BytesIO()
    image = resize_with_aspect_ratio(image, max_size)
    image.save(output, format='PNG')
    b64 = str(base64.b64encode(output.getvalue()).decode('utf-8'))
    return b64
