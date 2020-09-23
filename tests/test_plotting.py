import sys
from typing import Sequence

import numpy as np
import pandas as pd
import pytest
from IPython.display import HTML
from PIL import Image

sys.path.append(".")
sys.path.append("../.")
import ipyplot


BASE_NP_IMGS = list(np.asarray(
    np.random.randint(0, 255, (3, 128, 128, 3)), dtype=np.uint8))

BASE_INTERNET_URLS = [
    "https://raw.githubusercontent.com/karolzak/boxdetect/master/images/checkbox-example.jpg",  # NOQA E501
    "https://raw.githubusercontent.com/karolzak/boxdetect/master/images/checkboxes-details.jpg",  # NOQA E501
    "https://raw.githubusercontent.com/karolzak/boxdetect/master/images/example1.png",  # NOQA E501
]

BASE_LOCAL_URLS = [
    "docs/example1-tabs.jpg",
    "docs/example2-images.jpg",
    "docs/example3-classes.jpg",
]

LOCAL_URLS_AS_PIL = list([Image.open(url) for url in BASE_LOCAL_URLS])

TEST_DATA = [
    # (imgs, b64)
    (LOCAL_URLS_AS_PIL, True),
    (BASE_NP_IMGS, True),
    (pd.Series(BASE_NP_IMGS), True),
    (np.asarray(BASE_NP_IMGS), True),
    (np.asarray(BASE_NP_IMGS), False),
    (np.asarray(BASE_INTERNET_URLS), False),
    (np.asarray(BASE_INTERNET_URLS), True),
    (np.asarray(BASE_LOCAL_URLS), True),
    (np.asarray(BASE_LOCAL_URLS), False),
    (np.asarray(BASE_NP_IMGS, dtype=np.float) / 255, False),
    (np.asarray(BASE_NP_IMGS, dtype=np.float) / 255, True),
]


@pytest.mark.parametrize(
    "imgs, b64",
    TEST_DATA)
def test_plot_images(capsys, imgs, b64):
    ipyplot.plot_images(
        imgs,
        labels=None,
        max_images=30,
        img_width=300,
        force_b64=b64)
    captured = capsys.readouterr()
    if b64 and type(imgs[0]) is np.str_ and "http" in imgs[0]:
        assert("Ignoring 'force_b64' flag" in captured.out)

    assert(str(HTML).split("'")[1] in captured.out)


@pytest.mark.parametrize(
    "imgs, b64",
    TEST_DATA)
def test_plot_class_tabs(capsys, imgs, b64):
    ipyplot.plot_class_tabs(
        imgs,
        labels=np.asarray(['a', 'b', 'b']),
        img_width=300,
        force_b64=b64)
    captured = capsys.readouterr()
    if b64 and type(imgs[0]) is np.str_ and "http" in imgs[0]:
        assert("Ignoring 'force_b64' flag" in captured.out)

    assert(str(HTML).split("'")[1] in captured.out)


@pytest.mark.parametrize(
    "imgs, b64",
    TEST_DATA)
def test_plot_class_representations(capsys, imgs, b64):
    ipyplot.plot_class_representations(
        imgs,
        labels=np.asarray(['a', 'b', 'b']),
        img_width=300,
        force_b64=b64)
    captured = capsys.readouterr()
    if b64 and type(imgs[0]) is np.str_ and "http" in imgs[0]:
        assert("Ignoring 'force_b64' flag" in captured.out)

    assert(str(HTML).split("'")[1] in captured.out)
