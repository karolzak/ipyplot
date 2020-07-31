import sys

import numpy as np
import pytest
from IPython.display import HTML

sys.path.append(".")
sys.path.append("../.")
import ipyplot

BASE_NP_IMGS = np.random.rand(3, 128, 128, 3)

BASE_INTERNET_URIS = np.asarray([
    "https://raw.githubusercontent.com/karolzak/boxdetect/master/images/checkbox-example.jpg",
    "https://raw.githubusercontent.com/karolzak/boxdetect/master/images/checkboxes-details.jpg",
    "https://raw.githubusercontent.com/karolzak/boxdetect/master/images/example1.png",
])

BASE_LOCAL_URIS = np.asarray([
    "docs/example1-tabs.jpg",
    "docs/example2-images.jpg",
    "docs/example3-classes.jpg",
])

TEST_DATA = [
    # (np.random.rand(3, 128, 128, 3).astype(np.float32), False),
    # (np.random.rand(3, 128, 128, 3).astype(np.float32) * 255, False),
    (BASE_NP_IMGS.astype(np.uint8), True),
    (BASE_NP_IMGS.astype(np.uint8) * 255, True),
    (BASE_NP_IMGS.astype(np.uint8), False),
    (BASE_NP_IMGS.astype(np.uint8) * 255, False),
    (BASE_INTERNET_URIS, False),
    (BASE_INTERNET_URIS, True),
    (BASE_LOCAL_URIS, True),
    (BASE_LOCAL_URIS, False),
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
