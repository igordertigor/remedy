import os
import re
import contextlib
import unittest
from unittest import mock

from io import StringIO

import remedy


class MockFS(object):

    def __init__(self):
        self.files = {}

    @contextlib.contextmanager
    def open(self, fname, mode='r'):
        if mode == 'w':
            self.files[fname] = StringIO()
        yield self.files[fname]


class e2eTest(unittest.TestCase):

    @mock.patch('remedy.shutil.copytree')
    def test_simple_run(self, mock_copytree):
        mock_fs = MockFS()
        with open('example/slides.md') as f:
            mock_fs.files['slides.md'] = StringIO(f.read())

        with mock.patch('remedy.open', mock_fs.open):
            remedy.main('slides.md')

        output = mock_fs.files['presentation.html'].getvalue()

        # Indicative of html
        self.assertIsNotNone(re.search(r"class='special-class'", output))

        # Indicative of subslide usage
        self.assertIsNotNone(re.search(r'<section>\s+<section', output))

        expected_origin = os.path.join(os.path.dirname(__file__),
                                       'templates/context')
        mock_copytree.assert_called_with(expected_origin, 'context')

    @mock.patch('remedy.shutil.copytree')
    def test_run_with_header_mod(self, mock_copytree):
        mock_fs = MockFS()
        with open('example/slides.md') as f:
            mock_fs.files['slides.md'] = StringIO(f.read())

        with open('example/header_mod.html') as f:
            mock_fs.files['header_mod.html'] = StringIO(f.read())

        with mock.patch('remedy.open', mock_fs.open):
            remedy.main('slides.md', header='header_mod.html')

        output = mock_fs.files['presentation.html'].getvalue()

        # Indicative of html
        self.assertIsNotNone(re.search(r"class='special-class'", output))

        # Indicative of subslide usage
        self.assertIsNotNone(re.search(r'<section>\s+<section', output))

        # Indicative of header modification applied
        self.assertIsNotNone(re.search(r'<style>.*</style>', output, re.DOTALL))

        expected_origin = os.path.join(os.path.dirname(__file__),
                                       'templates/context')
        mock_copytree.assert_called_with(expected_origin, 'context')
