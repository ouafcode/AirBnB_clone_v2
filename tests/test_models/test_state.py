#!/usr/bin/python3
"""test state"""
from tests.test_models.test_base_model import test_basemodel
from models.state import State
import os


class test_state(test_basemodel):
    """test class state"""

    def __init__(self, *args, **kwargs):
        """test init"""
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """test name"""
        new = self.value()
        self.assertEqual(type(new.name), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))
