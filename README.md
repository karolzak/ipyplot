**IPyPlot** is a small python package offering fast and efficient plotting of images inside Jupyter Notebooks cells. It's using IPython with HTML for faster, richer and more interactive way of displaying big number of images.  

## Getting Started

Checkout the [examples below](#Examples) and 
[gear-images-examples.ipynb](notebooks/gear-images-examples.ipynb) notebook which holds end to end examples for using **IPyPlot**.

## Installation

So far **IPyPlot** can only be installed directly from this repo using `pip`:

```
pip install git+https://github.com/karolzak/ipyplot
```

## Examples

IPyPlot offers 3 main functions which can be used for displaying images in notebooks:

To start working with `IPyPlot` you need to simply import it like this:
```python
import ipyplot
```

and use any of the available plotting functions:

#### Display images in separate, interactive tabs for each class

![](docs/example1-tabs.jpg)

#### Display a collection of images

![](docs/example2-images.jpg)

#### Display class representations (first image for each class)

![](docs/example3-classes.jpg)