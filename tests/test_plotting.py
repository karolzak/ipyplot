import os
import sys
import tempfile

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
    "tests/data/21HnHt+LMDL._AC_US436_QL65_.jpg",
    "tests/data/41edw+BCUjL._AC_US436_QL65_.jpg",
    "tests/data/100205.jpeg",
]

TEST_OUTPUT_IMG = "tests/data/out_img.jpg"
TEST_OUTPUT_IMG_B64 = "tests/data/out_img_b64.jpg"

LOCAL_URLS_AS_PIL = list([Image.open(url) for url in BASE_LOCAL_URLS])
LOCAL_URLS_AS_NP = list([np.asarray(img) for img in LOCAL_URLS_AS_PIL])

LABELS = [
    None,
    ['a', 'b', 'a'],
    np.asarray(['a', 'b', 'a']),
    pd.Series(['a', 'b', 'a'])
]

TEST_DATA = [
    # (imgs, labels, custom_texts)
    (BASE_LOCAL_URLS, LABELS[1], LABELS[0]),
    (LOCAL_URLS_AS_PIL, LABELS[1], LABELS[0]),
    (BASE_NP_IMGS, LABELS[1], LABELS[0]),
    (pd.Series(BASE_NP_IMGS), LABELS[1], LABELS[0]),
    (np.asarray(BASE_NP_IMGS), LABELS[1], LABELS[0]),
    (np.asarray(BASE_INTERNET_URLS), LABELS[1], LABELS[0]),
    (np.asarray(BASE_LOCAL_URLS), LABELS[1], LABELS[0]),
    (np.asarray(BASE_NP_IMGS, dtype=np.float) / 255, LABELS[1], LABELS[0]),
    (LOCAL_URLS_AS_PIL, LABELS[0], LABELS[0]),
    (LOCAL_URLS_AS_PIL, LABELS[1], LABELS[1]),
    (LOCAL_URLS_AS_PIL, LABELS[2], LABELS[2]),
    (LOCAL_URLS_AS_PIL, LABELS[3], LABELS[3]),
    ([os.path.abspath(x) for x in BASE_LOCAL_URLS], LABELS[1], LABELS[0]),
]

TEST_SAVE_OUTPUT_DATA = [
    # (imgs, output_img_path, b64, out)
    (BASE_LOCAL_URLS, "out.jpg", False, TEST_OUTPUT_IMG),
    (BASE_LOCAL_URLS, "out.jpeg", False, TEST_OUTPUT_IMG),
    (BASE_LOCAL_URLS, "out/out.jpg", False, TEST_OUTPUT_IMG),
    (BASE_LOCAL_URLS, "out.jpg", True, TEST_OUTPUT_IMG_B64),
    (LOCAL_URLS_AS_PIL, "out.jpg", True, TEST_OUTPUT_IMG_B64),
    (LOCAL_URLS_AS_NP, "out.jpg", True, TEST_OUTPUT_IMG_B64),
    (BASE_INTERNET_URLS, "out.jpg", True, TEST_OUTPUT_IMG_B64),
    ([os.path.abspath(x) for x in BASE_LOCAL_URLS], "out.jpg", False, TEST_OUTPUT_IMG),  # NOQA E501
]


@pytest.fixture(params=[True, False])
def test_true_false(request):
    return request.param


@pytest.mark.parametrize(
    "imgs, labels, custom_texts",
    TEST_DATA)
def test_plot_images(
        capsys, test_true_false, imgs, labels, custom_texts):
    ipyplot.plot_images(
        imgs,
        labels=labels,
        custom_texts=custom_texts,
        max_images=30,
        img_width=300,
        force_b64=test_true_false)
    captured = capsys.readouterr()
    if test_true_false and type(imgs[0]) is np.str_ and "http" in imgs[0]:
        assert("Ignoring 'force_b64' flag" in captured.out)

    assert(str(HTML).split("'")[1] in captured.out)


@pytest.mark.parametrize(
    "imgs, labels, custom_texts",
    TEST_DATA)
def test_plot_class_tabs(
        capsys, test_true_false, imgs, labels, custom_texts):
    ipyplot.plot_class_tabs(
        imgs,
        labels=labels if labels is not None else LABELS[1],
        custom_texts=custom_texts,
        img_width=300,
        force_b64=test_true_false)
    captured = capsys.readouterr()
    if test_true_false and type(imgs[0]) is np.str_ and "http" in imgs[0]:
        assert("Ignoring 'force_b64' flag" in captured.out)

    assert(str(HTML).split("'")[1] in captured.out)


@pytest.mark.parametrize(
    "imgs, labels, custom_texts",
    TEST_DATA)
def test_plot_class_representations(
        capsys, test_true_false, imgs, labels, custom_texts):
    ipyplot.plot_class_representations(
        imgs,
        labels=labels if labels is not None else LABELS[1],
        img_width=300,
        force_b64=test_true_false)
    captured = capsys.readouterr()
    if test_true_false and type(imgs[0]) is np.str_ and "http" in imgs[0]:
        assert("Ignoring 'force_b64' flag" in captured.out)

    assert(str(HTML).split("'")[1] in captured.out)


@pytest.mark.parametrize(
    "imgs, output_img_path, b64, exp_output",
    TEST_SAVE_OUTPUT_DATA)
def test_saving_output(
        imgs, output_img_path, b64, exp_output):
    with tempfile.TemporaryDirectory() as temp_dir:
        test_out_path = os.path.join(temp_dir, output_img_path)
        ipyplot.plot_images(
            imgs,
            force_b64=b64,
            output_img_path=test_out_path)

        assert os.path.exists(test_out_path)
        assert os.stat(test_out_path).st_size > 10000
        # assert filecmp.cmp(exp_output, test_out_path, shallow=False)

    with tempfile.TemporaryDirectory() as temp_dir:
        test_out_path = os.path.join(temp_dir, output_img_path)
        ipyplot.plot_class_representations(
            imgs,
            labels=[0, 1, 2],
            force_b64=b64,
            output_img_path=test_out_path)
        assert os.path.exists(test_out_path)
        assert os.stat(test_out_path).st_size > 10000
        # assert filecmp.cmp(exp_output, test_out_path, shallow=False)
