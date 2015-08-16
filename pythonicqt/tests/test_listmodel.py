"""This module contains all of the tests for the ListModel class in listmodel.py"""
import pytest
from pythonicqt.models.listmodel import ListModel

class TestListModel:
    """This class has all the tests that should run for ListModel."""

    def test_basic_list(self):
        """Test if list works similar to a normal list."""
        normal_list = [1,2,'three']
        test_list = ListModel(normal_list)
        #make sure not same object
        assert test_list is not normal_list
        #but equality is true though
        assert test_list == normal_list
        #other test
        assert test_list[0] == 1
        assert test_list != [None]

    def test_add_remove_list(self):
        """Test if basic adding, inserting, poping work."""
        test_list = ListModel()
        test_list.append(0)
        assert test_list[-1] == 0
        test_list.insert(0, True)
        assert test_list[-1] == 0
        assert test_list[0] == True
        #add a 3 to the end, pop off the True and check if it is gone
        test_list.append(3)
        assert test_list[-1] == 3
        last_element = test_list.pop()
        assert last_element == 3
        assert test_list[-1] != 3
        

        