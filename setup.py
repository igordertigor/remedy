#!/usr/bin/env python3

from setuptools import setup

setup(name="remedy",
      version="0.0.1",
      author="Ingo Fruend",
      author_email="Ingo.Fruend@twentybn.com",
      py_modules=['remedy'],
      install_requires=['jinja2==2.8', 'begins==0.9'],
      console_scripts=['remedy = remedy.py'])
