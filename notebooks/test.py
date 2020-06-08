import glob
import os
import numpy as np
import pandas as pd
from numpy import random
from PIL import Image
import urllib.request
import zipfile
import ipyplot

datasets_dir = '../datasets/'
zip_filename = 'gear_images.zip'

images = glob.glob(datasets_dir + 'gear_images' + '/**/*.*')
images = [image.replace('\\', '/') for image in images]
images = np.asarray(images, dtype=str) # conversion to nummpy is pretty important here


labels = [image.split('/')[-2] for image in images]
labels = np.asarray(labels, dtype=str) # conversion to nummpy is pretty important here


ipyplot.plot_class_representations(images, labels, img_width=150)