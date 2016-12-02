#!/usr/bin/env python3

from setuptools import setup

setup(name="remedy",
      version="0.0.2",
      author="Ingo Fruend",
      author_email="Ingo.Fruend@twentybn.com",
      description="Yet another markdown to reveal translator",
      long_description=open('README.md').read(),
      py_modules=['remedy'],
      install_requires=['jinja2==2.8', 'begins==0.9'],
      console_scripts=['remedy = remedy.py'])
