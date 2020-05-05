from setuptools import setup
from setuptools import find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="ipyplot",
    version="1.0.1",
    description="Simple package that leverages IPython and HTML for more efficient, reach and interactive plotting of images in Jupyter Notebooks",
    long_description=long_description,
    long_description_content_type="text/markdown",  # This is important!
    url="http://github.com/karolzak/ipyplot",
    author="Karol Zak",
    author_email="karol.zak@hotmail.com",
    license="MIT",
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        "IPython",
        "numpy",
        "pillow"
    ],
)
