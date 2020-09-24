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
    # (imgs)
    (LOCAL_URLS_AS_PIL),
    (BASE_NP_IMGS),
    (pd.Series(BASE_NP_IMGS)),
    (np.asarray(BASE_NP_IMGS)),
    (np.asarray(BASE_INTERNET_URLS)),
    (np.asarray(BASE_LOCAL_URLS)),
    (np.asarray(BASE_NP_IMGS, dtype=np.float) / 255),
]

TEST_CUSTOM_TEXTS = [
    None,
    ['a', 'b', 'a'],
    np.asarray(['a', 'b', 'a']),
    pd.Series(['a', 'b', 'a'])]


@pytest.fixture(params=[True, False])
def test_true_false(request):
    return request.param


@pytest.fixture(params=TEST_CUSTOM_TEXTS)
def test_custom_texts(request):
    return request.param


@pytest.fixture(params=TEST_CUSTOM_TEXTS[1:])
def test_labels(request):
    return request.param


@pytest.mark.parametrize(
    "imgs",
    TEST_DATA)
def test_plot_images(
        capsys, test_custom_texts, test_true_false, imgs):
    ipyplot.plot_images(
        imgs,
        labels=test_custom_texts,
        custom_texts=test_custom_texts,
        max_images=30,
        img_width=300,
        force_b64=test_true_false)
    captured = capsys.readouterr()
    if test_true_false and type(imgs[0]) is np.str_ and "http" in imgs[0]:
        assert("Ignoring 'force_b64' flag" in captured.out)

    assert(str(HTML).split("'")[1] in captured.out)


@pytest.mark.parametrize(
    "imgs",
    TEST_DATA)
def test_plot_class_tabs(
        capsys, test_labels, test_custom_texts, test_true_false, imgs):
    ipyplot.plot_class_tabs(
        imgs,
        labels=test_labels,
        custom_texts=test_custom_texts,
        img_width=300,
        force_b64=test_true_false)
    captured = capsys.readouterr()
    if test_true_false and type(imgs[0]) is np.str_ and "http" in imgs[0]:
        assert("Ignoring 'force_b64' flag" in captured.out)

    assert(str(HTML).split("'")[1] in captured.out)


@pytest.mark.parametrize(
    "imgs",
    TEST_DATA)
def test_plot_class_representations(
        capsys, test_labels, test_true_false, imgs):
    ipyplot.plot_class_representations(
        imgs,
        labels=test_labels,
        img_width=300,
        force_b64=test_true_false)
    captured = capsys.readouterr()
    if test_true_false and type(imgs[0]) is np.str_ and "http" in imgs[0]:
        assert("Ignoring 'force_b64' flag" in captured.out)

    assert(str(HTML).split("'")[1] in captured.out)
