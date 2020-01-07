# -*- coding: utf-8 -*-

"""
Geo class
"""

__author__ = "Anders Huse, Bishnu Poudel"
__email__ = "anhuse@nmbu.no; bipo@nmbu.no"

from biosim.Geography import Geo
import pytest

# class testGeo:
#     """ Tests for Geo class"""

def test_proper_letters():
    """all letters should either be: = O, M, J, S, D"""
    with pytest.raises(ValueError):
        Geo("yyyy")


def test_same_legth():
    """rows have same length"""
    with pytest.raises(ValueError):
        Geo(""""\
                OOOOOOO
                JJJJJ""")

def test_ocean_edges():
    """Should have only ocean around the edges"""
    pass



