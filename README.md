# FitsIO
A package to deal with Fits files which focuses on safety, user-friendliness, and performance.

# How to install.
If you would like to create a particular environment for this project, then yoi can do it via conda
```conda create -n fitsenv python=3.10```
```conda activate fitsenv```

Then you can install (Editable install as in development phase) project using command:
```pip3 install -e FitsIO/.```

## Install the package to use it for another project
```python setup.py install```

Usage:
```
from FitsIO.FitsFile import File
import os

#absolute file path

filepath='/Users/kansal/Documents/GitHub/FitsIO/data/gal.fits'
image = File.FitsFile(filepath)

image.open()
image.get_headers()
```

# Run Unit tests
Go to the directory FitsIO and run:
```
python3 tests/FitsFile_Image.py
```

which will give you output given below:

```
.
----------------------------------------------------------------------
Ran 4 tests in 0.018s

OK
```

# Tutorial
The tutorials are given in notebooks with associated documentation.


# Issues
Feel free to open issues to report bugs, new or missing features and other feedbacks.
