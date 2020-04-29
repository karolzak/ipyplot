def resize_with_aspect_ratio(img, max_size=1000):
    """Helper function to resize image against the longer edge

    Args:
        img (PIL.Image):
            Image object to be resized
        max_size (int, optional):
            Max size of the longer edge in pixels.
            Defaults to 2800.

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
