import sys

name = "keras_unet"

__version__ = "1.0.0"

if 'google.colab' in sys.modules:
    print("""
    WARNING! Google Colab Environment detected!
    You might encounter issues while running in Google Colab environment.
    If images are not displaying properly please try setting `base_64` param to `True`.
    """)

from .plotting import (
    plot_class_representations, plot_class_tabs,
    plot_images
)

import ipyplot.img_helpers
