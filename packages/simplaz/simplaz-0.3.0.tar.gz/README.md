

[![GitHub license](https://img.shields.io/github/license/hugoledoux/simplaz)](https://github.com/hugoledoux/simplaz/blob/master/LICENSE) [![PyPI version](https://badge.fury.io/py/simplaz.svg)](https://pypi.org/project/simplaz/)

simplaz
=======

A Python package to read LAZ files (LAS too).
Basically it's a wrapper around [Rust las](https://docs.rs/las) and it exposes the most useful methods.

It doesn't read in memory the whole file, so you can just iterate over each point sequentially without worrying about your RAM comsumption.

Only reading at this moment; writing is for later.


Installation
============

pip
---

To install the latest release: `pip install simplaz`


Development
-----------

  1. install [Rust](https://www.rust-lang.org/) (v1.39+)
  2. install [maturin](https://github.com/PyO3/maturin) 
  3. `maturin develop`
  4. move to another folder, and `import simplaz` shouldn't return any error


Documentation
=============

The pydoc can be found [here](https://hugoledoux.github.io/simplaz/).


Example
=======

```python
import simplaz
import numpy as np

ds = simplaz.read_file("/Users/hugo/data/ahn3/crop.laz")

header = ds.header
print("LAS v{}".format(header.version))
print("Point count: {}".format(header.number_of_points))

#-- using numpy functions
#-- define a specific numpy type
mypoint = np.dtype([('x','float64'), 
                    ('y', 'float64'), 
                    ('z', 'float64'), 
                    ('intensity', 'int16')]
                    ) 
pts = np.zeros((ds.header.number_of_points,), dtype=mypoint)

#-- iterate over all the points and store in numpy array only 
#-- the ground point (classification=2)
for (i, p) in enumerate(ds):
    if p.classification == 2:
        pts[i][0] = p.x
        pts[i][1] = p.y
        pts[i][2] = p.z
        pts[i][3] = p.classification
print (len(pts))
```


What is supported and what not?
===============================

Most of [LAS v1.4](https://www.asprs.org/wp-content/uploads/2010/12/LAS_1_4_r13.pdf) is supported, except:

 - v1.4 support for extra bits after each point
 


LAS classes
===========

| Classification | description                   | 
| -------------- | ----------------------------- |
|  0             | Created, never classified     |
|  1             | Unclassfied                   |
|  2             | Ground                        |
|  3             | Low Vegetation                |
|  4             | Medium Vegetation             |
|  5             | High Vegetation               |
|  6             | Building                      |
|  7             | Low Point (noise)             |
|  8             | Model Key-point (mass point)  |
|  9             | Water                         |
| 10             | Reserved for ASPRS definition |
| 11             | Reserved for ASPRS definition |
| 12             | Overlap Points                |
| 13-31          | Reserved for ASPRS definition |


LAS Point format
================

This is well explained [on this page](https://pylas.readthedocs.io/en/latest/intro.html#point-records).
