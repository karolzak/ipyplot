import sys

if 'google.colab' in sys.modules:
    print("WARNING! You might encounter some issues while running in Google colab environment")  # NOQA E501

from .plotting import (
    plot_class_representations, plot_class_tabs,
    plot_images
)

import ipyplot.img_helpers
