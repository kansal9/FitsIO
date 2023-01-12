import subprocess
from setuptools
from setuptools import find_packages

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

version = "0.0.1"

setuptools.setup(
      name='FitsIO',
      version=version,
      author='Vanshika Kansal',
      author_email='vanshikakansal@gmail.com',
      description='A library to read and write Fits files',
      long_description=long_description,
      long_description_content_type = 'text/markdown',
      url='',
      classifiers=[
        'Development Status :: 0 -> Under-development/Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Astronomy',
      ],

      license='Other/Proprietary License',
      packages=find_packages(),
      install_requires=[
        'astropy>=5.1.1',
        'numpy>=1.23.4',
      ],
      python_requires='>=3.9.5',
     )
