# seaborn-image: image data visualization

[![Tests](https://github.com/SarthakJariwala/seaborn-image/workflows/Tests/badge.svg)](https://github.com/SarthakJariwala/seaborn-image/actions?workflow=Tests)
[![Codecov](https://codecov.io/gh/SarthakJariwala/seaborn-image/branch/master/graph/badge.svg)](https://codecov.io/gh/SarthakJariwala/seaborn-image)
[![PyPI](https://img.shields.io/pypi/v/seaborn-image.svg)](https://pypi.org/project/seaborn-image/)
[![Documentation Status](https://readthedocs.org/projects/seaborn-image/badge/?version=latest)](https://seaborn-image.readthedocs.io/en/latest/?badge=latest)

<div class="row">

  <a>
  <img src="./examples/image_0.png" height="180" width="200">
  </a>

  <a>
  <img src="./examples/image_1.png" height="180" width="200">
  </a>

  <a>
  <img src="./examples/image_3.png" height="165" width="400">
  </a>

</div>

<div class="row">

  <a>
  <img src="./examples/image_5.png" height="250" width="375">
  </a>

</div>

<div class="row">

  <a>
  <img src="./examples/image_4.png" height="600" width="600">
  </a>

</div>

Seaborn-like image data visualization using matplotlib, scikit-image and scipy.

## Description

Seaborn-image is a seaborn like python **image** visualization and processing library
based on matplotlib, scipy and scikit-image.

The aim of seaborn-image is to provide a high-level API to **process and plot attractive images quickly and effectively**.

## Documentation

Check out the docs [here](https://seaborn-image.readthedocs.io/)


## Installation

```bash
pip install seaborn-image
```

## Usage
### Simple usage

```python

import seaborn_image as isns

"""Plot image"""
isns.imgplot(data)

"""Plot image with scalebar"""
isns.imgplot(data, dx=0.01, units="um")

"""Add colorbar label"""
isns.imgplot(data, dx=0.01, units="um", cbar_label="Height (nm)")
```
<a>
<img src="./examples/image_0.png" height="275" width="300">
</a>

### Plot image with a histogram

```python
import seaborn_image as isns

isns.imghist(data, dx=150, units="nm", cbar_label="Height (nm)", cmap="ice")
```

<a>
<img src="./examples/image_5.png" height="300" width="450">
</a>

### Set context like seaborn

```python

import seaborn_image as isns

isns.set_context("notebook") # Other options include paper, talk, presentation, poster
```

### Apply image filters (from scipy and skimage) and plot

```python

import seaborn_image as isns

isns.filterplot(data, filter="gaussian", sigma=5, cbar_label="Height (nm)")
```

<a>
<img src="./examples/image_3.png" height="260" width="600">
</a>

Check out the more information [here](https://seaborn-image.readthedocs.io/)
