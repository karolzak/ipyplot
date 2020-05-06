import sys

try:
    from IPython.display import display, HTML
except Exception as e:
    raise Exception('IPython not detected. Plotting without IPython is not possible')  # NOQA E501

if 'google.colab' in sys.modules:
    print("WARNING! You might encounter some issues while running in Google colab environment")  # NOQA E501

from .plotting import (
    plot_class_representations, plot_class_tabs,
    plot_images
)

import ipyplot.img_helpers
