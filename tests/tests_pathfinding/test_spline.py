"""Importing needed libraries"""
import pytest
import numpy as np
from computer_vision.pathfinding.spline import t_j, catmull_rom_spline, catmull_rom_chain


class TestParametrized:
    """
    DOC: Testing spline functions
    """

    @pytest.mark.parametrize('param, expected', [
        ([1, (43, 12), (12, 30), 0.5], 6.987),
        ([3, (23, 100), (43, 21), 0.2], 5.411),
        ([3, (2, 12), (32, 56), 0.5], 10.298),
        ([4, (3, 49), (45, 76), 0.3], 7.232),
    ])
    def test_t_j(self, param, expected):
        '''Testing t_j method'''
        assert t_j(param[0], param[1], param[2], param[3]
                   ) == pytest.approx(expected, 0.001)

    @pytest.mark.parametrize('param, expected', [
        ([(3, 4), (4, 4), (5, 3), (6, 3), 0.5],
         [
            np.array([[4.,         4.],
                      [4.25963561, 3.80092628],
                      [4.5,        3.5],
                      [4.74036439, 3.19907372],
                      [5.,         3.]],
                     ),
            np.array([[0.92732365, - 0.38411003],
                      [0.83009301, - 0.89799471],
                      [0.7976828, - 1.06928961],
                      [0.83009301, - 0.89799471],
                      [0.92732365, - 0.38411003]],
                     )]),
        ([(3, 4), (4, 4), (5, 5), (6, 5), 0.5],
         [
            np.array([[4.,         4.],
                      [4.25963561, 4.19907372],
                      [4.5,        4.5],
                      [4.74036439, 4.80092628],
                      [5.,         5.]],
                     ),
            np.array([[0.92732365, 0.38411003],
                      [0.83009301, 0.89799471],
                      [0.7976828, 1.06928961],
                      [0.83009301, 0.89799471],
                      [0.92732365, 0.38411003]],
                     )]),
        ([(10, 2), (9, 2), (8, 3), (7, 3), 0.5],
         [
            np.array([[9.,         2.],
                      [8.74036439, 2.19907372],
                      [8.5,        2.5],
                      [8.25963561, 2.80092628],
                      [8.,         3.]],
                     ),
            np.array([[-0.92732365,  0.38411003],
                      [-0.83009301, 0.89799471],
                      [-0.7976828,   1.06928961],
                      [-0.83009301,  0.89799471],
                      [-0.92732365,  0.38411003]],
                     )]),
        ([(10, 7), (9, 7), (8, 6), (7, 6), 0.5], [
            np.array([[9., 7.],
                     [8.74036439, 6.80092628],
                      [8.5, 6.5],
                      [8.25963561, 6.19907372],
                      [8., 6.]],
                     ),
            np.array([[-0.92732365, - 0.38411003],
                      [-0.83009301, - 0.89799471],
                      [-0.7976828, - 1.06928961],
                      [-0.83009301, - 0.89799471],
                      [-0.92732365, - 0.38411003]],
                     )]),
    ])
    def test_catmull_rom_spline(self, param, expected):
        '''Testing catmull_rom_spline method'''
        curve, velocity = catmull_rom_spline(
            param[0], param[1], param[2], param[3], param[4], 5)
        print("Curve")
        print(curve)
        for i, value in enumerate(curve):
            assert value[0] == pytest.approx(expected[0][i][0], 0.001)
            assert value[1] == pytest.approx(expected[0][i][1], 0.001)
        print("VELO")
        print(velocity)
        for i, value in enumerate(velocity):
            assert value[0] == pytest.approx(expected[1][i][0], 0.001)
            assert value[1] == pytest.approx(expected[1][i][1], 0.001)

    # @pytest.mark.parametrize('param, expected', [
    #     ([3, 4, 10, 2], [(3, 4), (4, 4), (5, 3), (6, 3), (7, 3), (8, 3), (9, 2), (10, 2)]),
    #     ([3, 4, 10, 7], [(3, 4), (4, 4), (5, 5), (6, 5), (7, 6), (8, 6), (9, 7), (10, 7)]),
    #     ([10, 2, 3, 4], [(10, 2), (9, 2), (8, 3), (7, 3), (6, 3), (5, 3), (4, 4), (3, 4)]),
    #     ([10, 7, 3, 4], [(10, 7), (9, 7), (8, 6), (7, 6), (6, 5), (5, 5), (4, 4), (3, 4)]),
    #     ])
    # def test_catmull_rom_chain(self, param, expected):
    #     '''Testing get_bresenham method'''
    #     assert catmull_rom_spline(param[0], param[1], param[2], param[3]) == expected
