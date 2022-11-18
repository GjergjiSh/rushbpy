from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Modular raspberry pi robot framework'
LONG_DESCRIPTION = long_description

# Setting up
setup(
    name="rushb",
    version=VERSION,
    author="Gjergji Shkurti",
    author_email="gjergji_shkurti@yahoo.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['keyboard'],
    keywords=['python', 'robotics', 'arduino', 'rasberry pi', 'computer vision', 'ai'],
    classifiers=[
        "Programming Language :: Python :: 3"
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
