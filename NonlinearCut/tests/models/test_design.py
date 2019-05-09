"""
test
"""
# pylint: disable=redefined-outer-name
from math import isclose

import numpy as np

import pytest


@pytest.fixture(scope='module')
def design():
    """
    design config
    """
    from tests.config import config
    from src.models.design import Design

    return Design(config['design_path_test_v1'])


def test_get(design):
    """
    design
    """
    # pylint: disable=line-too-long

    section = {('樓層', ''): 'RF', ('編號', ''): 'B1', ('RC 梁寬', ''): 60.0, ('RC 梁深', ''): 80.0, ('箍筋', '左'): '2#4@15', ('箍筋', '中'): '#4@12', ('箍筋', '右'): '2#4@15', (
        '箍筋長度', '左'): 177.5000050663947, ('箍筋長度', '中'): 355.0000101327894, ('箍筋長度', '右'): 177.5000050663947, ('梁長', ''): 800.0, ('支承寬', '左'): 45.0, ('支承寬', '右'): 45.0, ('主筋量', ''): 22142.12094137667, ('箍筋量', ''): 22142.12094137667}

    # col is None
    assert design.get(1) == section

    # col is '主筋'
    assert design.get(3, ('主筋', '左1')) == '7-#7'
    assert design.get(3, 5) == '7-#7'

    # col is '主筋長度'
    assert isclose(design.get(9, ('主筋長度', '中')), 330.000019073486)
    assert isclose(design.get(2, ('主筋長度', '左1')), 109.9999964237209)

    # col is others
    assert design.get(3, ('RC 梁寬', '')) == 60


def test_len(design):
    """
    test len
    """
    assert design.get_len() == (12, 23)


def test_get_abs_length(design):
    """
    test abs_length
    """
    assert np.allclose(design.get_abs_length(1, 8), (0.45, 2.25))


def test_get_group_num(design):
    """
    test group_num
    """
    assert design.get_group_num() == 3


def test_get_colname_by_length(design):
    """
    test get_colname_by_length
    """
    assert design.get_colname_by_length(2, 3.0) == ('中', '中')


def test_total_area(design):
    """
    test total_area
    """
    assert design.get_total_area(11, ('主筋', '左1')) == 0.0027097


def test_area_by_length(design):
    """
    test area_by_length
    """
    assert design.get_area_by_length(11, 0.24) == (0.0050323, 0.0027097)


def test_num(design):
    """
    test num
    """
    assert design.get_num(6, ('主筋', '右1')) == 0
    assert design.get_num(8, ('主筋', '右1')) == 9


def test_dia(design):
    """
    test dia
    """

    assert design.get_diameter(6, ('箍筋', '右')) == 0.0127
    assert design.get_diameter(6, ('主筋', '右1')) == 0


def test_area(design):
    """
    test area
    """

    assert design.get_area(6, ('主筋', '右1')) == 0
    assert design.get_area(6, ('箍筋', '右')) == 0.0002534


def test_spacing(design):
    """
    test spacing
    """

    assert design.get_spacing(10, ('箍筋', '右')) == 0.15


def test_shear(design):
    """
    test shear
    """

    assert isclose(design.get_shear(10, ('箍筋', '右')), 0.0016893333333333333)
    assert design.get_shear(10, ('箍筋', '中')) == 0.001267
