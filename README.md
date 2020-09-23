[![Build](https://github.com/karolzak/ipyplot/workflows/CI%20Build/badge.svg)](https://github.com/karolzak/ipyplot/actions?query=workflow%3A%22CI+Build%22)
[![PyPI - version](https://img.shields.io/pypi/v/ipyplot.svg "PyPI version")](https://pypi.org/project/ipyplot/) 
[![Downloads](https://pepy.tech/badge/ipyplot)](https://pepy.tech/project/ipyplot)
[![Downloads/Month](https://pepy.tech/badge/ipyplot/month)](https://pepy.tech/project/ipyplot/month)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/karolzak/ipyplot/blob/master/LICENSE)

**Share**:  
[![Twitter URL](https://img.shields.io/twitter/url?url=https%3A%2F%2Fgithub.com%2karolzak%2Fipyplot)](http://twitter.com/share?text=IPyPlot%20-%20fast%20and%20effortless%20way%20to%20display%20huge%20numbers%20of%20images%20in%20Python%20notebooks&url=https://github.com/karolzak/ipyplot/&hashtags=python,computervision,imageclassification,deeplearning,ML,AI)
[![LinkedIn URL](https://raw.githubusercontent.com/karolzak/boxdetect/master/images/linkedin_share4.png)](http://www.linkedin.com/shareArticle?mini=true&url=https://github.com/karolzak/ipyplot&title=IPyPlot%20python%20package)

**IPyPlot** is a small python package offering fast and efficient plotting of images inside Jupyter Notebooks cells. It's using IPython with HTML for faster, richer and more interactive way of displaying big number of images.

Displaying huge numbers of images with Python in Notebooks always was a big pain for me as I always used `matplotlib` for that task and never have I even considered if it can be done faster, easier or more efficiently.  
Especially in one of my recent projects I had to work with a vast number of document images in a very interactive way which led me to forever rerunning notebook cells and waiting for countless seconds for `matplotlib` to do it's thing..   
My frustration grew up to a point were I couldn't stand it anymore and started to look for other options..  
Best solution I found involved using `IPython.display` function in connection with simple HTML. Using that approach I built a simple python package called **IPyPlot** which finally helped me cure my frustration and saved a lot of my time

### Features:
- [x] Easy, fast and efficient plotting of images in python within notebooks
- [x] Plotting functions (see [examples section](#Usage-examples) to learn more:
  - [x] `plot_images` - simply plots all the images in a grid-like manner 
  - [x] `plot_class_representations` - similar to `plot_images` but displays only a single image per class (based on provided labels collection)
  - [x] `plot_class_tabs` - plots images in a grid-like manner in a separate tab for each class based on provided label
- [x] Supported notebook platforms:
  - [x] Jupyter
  - [x] Google Colab
  - [x] Azure Notebooks
  - [x] Kaggle Notebooks
- [x] Supported image formats:
  - [x] Array of local storage URLs, e.g. `[your/dir/img1.jpg]`
  - [x] Array of remote URLs, e.g. `[http://yourimages.com/img1.jpg]`
  - [x] Array of `PIL.Image` objects
  - [x] Array of images as `numpy.ndarray` objects
- [x] Misc:
  - [x] `force_b64` flag to force conversion of images from URLs to base64 format

## Getting Started

Checkout the [examples below](#Usage-examples) and 
[gear-images-examples.ipynb](https://github.com/karolzak/ipyplot/blob/master/notebooks/gear-images-examples.ipynb) notebook which holds end to end examples for using **IPyPlot**.

## Installation

**IPyPlot** can be installed directly from this repo using `pip`:

```
pip install git+https://github.com/karolzak/ipyplot
```

or through [PyPI](https://pypi.org/project/ipyplot/)

```
pip install ipyplot
```

## Usage examples

IPyPlot offers 3 main functions which can be used for displaying images in notebooks:

To start working with `IPyPlot` you need to simply import it like this:
```python
import ipyplot
```  
and use any of the available plotting functions shown below (notice execution times).  
`images` - should be a numpy array of either `string` (image file paths), `PIL.Image` objects or `numpy.array` objects representing images  
`labels` - should be a numpy array of `string`

#### Display images in separate, interactive tabs for each class

![](https://raw.githubusercontent.com/karolzak/ipyplot/master/docs/example1-tabs.gif)

#### Display a collection of images

![](https://raw.githubusercontent.com/karolzak/ipyplot/master/docs/example2-images.jpg)

#### Display class representations (first image for each class)

![](https://raw.githubusercontent.com/karolzak/ipyplot/master/docs/example3-classes.jpg)
