[![Build](https://github.com/karolzak/ipyplot/workflows/CI%20Build/badge.svg)](https://github.com/karolzak/ipyplot/actions?query=workflow%3A%22CI+Build%22)
[![PyPI - version](https://img.shields.io/pypi/v/ipyplot.svg "PyPI version")](https://pypi.org/project/ipyplot/) 
[![Downloads](https://pepy.tech/badge/ipyplot)](https://pepy.tech/project/ipyplot)
[![Downloads/Month](https://pepy.tech/badge/ipyplot/month)](https://pepy.tech/project/ipyplot/month)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/karolzak/ipyplot/blob/master/LICENSE)

**Share**:  
[![Twitter URL](https://img.shields.io/twitter/url?url=https%3A%2F%2Fgithub.com%2karolzak%2Fipyplot)](http://twitter.com/share?text=IPyPlot%20-%20fast%20and%20effortless%20way%20to%20display%20huge%20numbers%20of%20images%20in%20Python%20notebooks&url=https://github.com/karolzak/ipyplot/&hashtags=python,computervision,imageclassification,deeplearning,ML,AI)
[![LinkedIn URL](https://raw.githubusercontent.com/karolzak/boxdetect/master/images/linkedin_share4.png)](http://www.linkedin.com/shareArticle?mini=true&url=https://github.com/karolzak/ipyplot&title=IPyPlot%20python%20package)

**IPyPlot** is a small python package offering fast and efficient plotting of images inside Python Notebooks cells. It's using IPython with HTML for faster, richer and more interactive way of displaying big numbers of images.

![](https://raw.githubusercontent.com/karolzak/ipyplot/master/docs/example1-tabs.gif)

Displaying big numbers of images with Python in Notebooks always was a big pain for me as I always used `matplotlib` for that task and never have I even considered if it can be done faster, easier or more efficiently.  
Especially in one of my recent projects I had to work with a vast number of document images in a very interactive way which led me to forever rerunning notebook cells and waiting for countless seconds for `matplotlib` to do it's thing..   
My frustration grew up to the point were I couldn't stand it anymore and started to look for other options..  
Best solution I found involved using `IPython` package in connection with simple HTML. Using that approach I built this simple python package called **IPyPlot** which finally helped me cure my frustration and saved a lot of my time.

### Features:
- [x] Easy, fast and efficient plotting of images in python within notebooks
- [x] Plotting functions (see [examples section](#Usage-examples) to learn more):
  - [x] `plot_images` - simply plots all the images in a grid-like layout 
  - [x] `plot_class_representations` - similar to `plot_images` but displays only the first image for each label/class (based on provided labels collection)
  - [x] `plot_class_tabs` - plots images in a grid-like manner in a separate tab for each label/class based on provided labels
- [x] Supported image formats:
  - [x] Sequence of local storage URLs, e.g. `[your/dir/img1.jpg]`
  - [x] Sequence of remote URLs, e.g. `[http://yourimages.com/img1.jpg]`
  - [x] Sequence of `PIL.Image` objects
  - [x] Sequence of images as `numpy.ndarray` objects
  - [x] Supported sequence types: `list`, `numpy.ndarray`, `pandas.Series`
- [x] Misc features:
  - [x] `custom_texts` param to display additional texts like confidence score or some other information for each image
  - [x] `force_b64` flag to force conversion of images from URLs to base64 format
  - [x] click on image to enlarge 
  - [x] control number of displayed images and their width through `max_images` and `img_width` params
  - [x] "show html" button which reveals the HTML code used to generate plots
  - [x] option to set specific order of labels/tabs, filter them or ignore some of the labels
- [x] Supported notebook platforms:
  - [x] Jupyter
  - [x] Google Colab
  - [x] Azure Notebooks
  - [x] Kaggle Notebooks

## Getting Started

To start using IPyPlot, see [examples below](#Usage-examples) or go to 
[gear-images-examples.ipynb](https://github.com/karolzak/ipyplot/blob/master/notebooks/gear-images-examples.ipynb) notebook which takes you through most of the scenarios and options possible with **IPyPlot**.

## Installation

**IPyPlot** can be installed through [PyPI](https://pypi.org/project/ipyplot/):

```
pip install ipyplot
```

or directly from this repo using `pip`:

```
pip install git+https://github.com/karolzak/ipyplot
```

## Usage examples

IPyPlot offers 3 main functions which can be used for displaying images in notebooks:

To start working with `IPyPlot` you need to simply import it like this:
```python
import ipyplot
```  
and use any of the available plotting functions shown below (notice execution times).  
- **images** - should be a sequence of either `string` (local or remote image file URLs), `PIL.Image` objects or `numpy.ndarray` objects representing images  
- **labels** - should be a sequence of `string` or `int`

#### Display a collection of images

```python
images = [
    "docs/example1-tabs.jpg",
    "docs/example2-images.jpg",
    "docs/example3-classes.jpg",
]
ipyplot.plot_images(images, max_images=30, img_width=150)
```

![](https://raw.githubusercontent.com/karolzak/ipyplot/master/docs/example2-images.jpg)

#### Display class representations (first image for each unique label)

```python
images = [
    "docs/example1-tabs.jpg",
    "docs/example2-images.jpg",
    "docs/example3-classes.jpg",
]
labels = ['label1', 'label2', 'label3']
ipyplot.plot_class_representations(images, labels, img_width=150)

```

![](https://raw.githubusercontent.com/karolzak/ipyplot/master/docs/example3-classes.jpg)

#### Display images in separate, interactive tabs for each unique class

```python
images = [
    "docs/example1-tabs.jpg",
    "docs/example2-images.jpg",
    "docs/example3-classes.jpg",
]
labels = ['class1', 'class2', 'class3']
ipyplot.plot_class_tabs(images, labels, max_imgs_per_tab=10, img_width=150)

```

![](https://raw.githubusercontent.com/karolzak/ipyplot/master/docs/example1-tabs.gif)

To learn more about what you can do with IPyPlot go to [gear-images-examples.ipynb](https://github.com/karolzak/ipyplot/blob/master/notebooks/gear-images-examples.ipynb) notebook for more complex examples.
