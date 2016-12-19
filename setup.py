#!/usr/bin/env python3

from setuptools import setup

try:
    import pypandoc
    description = pypandoc.convert('README.md', 'rst')
except ImportError:
    description = ''


setup(name="remedy",
      version="0.0.6",
      author="Ingo Fruend",
      author_email="Ingo.Fruend@twentybn.com",
      description="Yet another markdown to reveal translator",
      long_description=description,
      py_modules=['remedy'],
      install_requires=['jinja2==2.8', 'begins==0.9'],
      scripts=['remedy'])
