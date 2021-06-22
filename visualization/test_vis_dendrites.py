import vis
import numpy as np
import pytest


def test_np_converter():
    arr1 = list(np.random.randint(100, size=30))
    arr2 = list(np.random.rand(30))
    converted1 = vis.np_converter(arr1)
    converted2 = vis.np_converter(arr2)
    for x in converted1:
        assert type(x) == int
    for x in converted2:
        assert type(x) == int
    assert converted1 == arr1
    assert converted2 != arr2


def test_points_list():
    axons = vis.points_list(is_axon=True)
    dendrites = vis.points_list(is_axon=False)
    assert axons[0] != dendrites[0]  # different nodes
    assert axons[1] != dendrites[1]  # different values
    axons_dist = vis.points_list(is_axon=True, distance=True)
    dendrites_dist = vis.points_list(is_axon=False, distance=True)
    assert axons_dist[1] != axons[1]  # values for different distance functions are different
    assert dendrites_dist[1] != dendrites[1]
    assert dendrites[1][dendrites[1] < 0].size == 0
    assert dendrites_dist[1][dendrites_dist[1] < 0].size == 0
    assert axons[1][axons[1] < 0].size == 0
    assert axons_dist[1][axons_dist[1] < 0].size == 0
