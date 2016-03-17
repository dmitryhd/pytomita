import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "pytomita",
    version = "0.1",
    author = "Dmitry Khodakov",
    author_email = "dmitryhd@gmail.com",
    description = ("pyton wrapper for yandex tomita-parser"),
    license = "BSD",
    keywords = "",
    packages=['tests'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)