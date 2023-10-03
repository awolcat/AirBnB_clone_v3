#!/usr/bin/python3
"""Module defines tests for index view functions"""
import inspect
import unittest
import pep8 as pycodestyle
import api
import requests
from unittest import mock
from flask import Flask, Blueprint
from api.v1.views import index


module_doc = api.v1.views.index.__doc__


class TestBaseModelDocs(unittest.TestCase):
    """Tests to check the documentation and style of index views"""

    @classmethod
    def setUpClass(self):
        """Set up for docstring tests"""
        self.index_funcs = inspect.getmembers(index, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/base_model.py conforms to PEP8."""
        for path in ['api/v1/views/index.py',
                     'tests/test_api/test_v1/test_views/test_index.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNot(module_doc, None,
                         "index.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "index.py needs a longer docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in index.py methods"""
        for func in self.index_funcs:
            with self.subTest(function=func):
                self.assertIsNot(
                    func[1].__doc__,
                    None,
                    "{:s} method needs a docstring".format(func[0])
                )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )
