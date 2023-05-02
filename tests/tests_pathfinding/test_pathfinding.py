'''Importing needed libraries'''
import pytest
import numpy as np
from computer_vision.pathfinding.pathfinding import PathFinding
from computer_vision.environment.src.environment import Environment, ViewPointObject
from computer_vision.environment.src.a_star import AStar

class TestParametrized:
    '''
    DOC: Testing PathFinding
    '''

    @pytest.mark.parametrize('times, angles, expected', [
        ([1, 2, 4, 5], [0, 0, 1, -5], [[7, 5], [0.5, -5]]),
        ([0.5, 0.7, 1, 2], [-1, -2, 1, 2], [[1.2, 3], [-1.5, 1.5]]),
    ])
    def test_merge_similar_angles(self, times, angles, expected):
        '''Testing distance to point'''
        board_size = (60, 115)
        env_size = 20

        tension = 0
        velocity = 10

        view_point_object: ViewPointObject = {
            'view_point': None,
            'object_id': 10,
        }
        env = Environment(board_size, env_size, view_point_object)
        a_star = AStar()

        path_finding = PathFinding(
            env,
            a_star,
            tension,
            velocity
        )

        data = path_finding.merge_similar_angles(times, angles, 1)

        assert data['times'] == expected[0]
        assert data['angles'] == expected[1]

    @pytest.mark.parametrize('point_one, point_two, expected', [
        ((32, 29), (31.5, 28.5625), -48.81),
        ((32, 29), (31.5, 29.4375), -131.19),
        ((32, 29), (32.5, 28.5625), 48.81),
        ((32, 29), (32.5, 29.4375), 131.19),
        ((31, 28), (31, 28), 0),
        ((31, 28), (31, 29), 0),
        ((31, 28), (31, 27), 0),
        ((31, 28), (30, 28), -90),
        ((31, 28), (32, 28), 90),
        ])
    def test_get_angle(self, point_one, point_two, expected):
        '''Testing get_angle method'''
        board_size = (60, 115)
        env_size = 20

        tension = 0
        velocity = 10

        view_point_object: ViewPointObject = {
            'view_point': None,
            'object_id': 10,
        }
        env = Environment(board_size, env_size, view_point_object)
        a_star = AStar()

        path_finding = PathFinding(
            env,
            a_star,
            tension,
            velocity
        )
        assert path_finding.get_angle(point_one, point_two) == pytest.approx(expected, 0.001)

    @pytest.mark.parametrize('angles, expected', [
        ([40, 45], [40, 5]),
        ([40, 35], [40, -5]),
        ([20, 30, 35], [20, 10, 5]),
        ([175, -175], [175, 10]),
        ([-175, 175], [-175, -10])
    ])
    def test_get_angle_diff(self, angles, expected):
        '''Get the list of change in angle'''
        board_size = (60, 115)
        env_size = 20

        tension = 0
        velocity = 10

        view_point_object: ViewPointObject = {
            'view_point': None,
            'object_id': 10,
        }
        env = Environment(board_size, env_size, view_point_object)
        a_star = AStar()

        path_finding = PathFinding(
            env,
            a_star,
            tension,
            velocity
        )
        assert path_finding.get_angle_diff(angles) == expected

    @pytest.mark.parametrize('param, expected', [
        ([1, (43, 12), (12, 30), 0.5], 6.987),
        ([3, (23, 100), (43, 21), 0.2], 5.411),
        ([3, (2, 12), (32, 56), 0.5], 10.298),
        ([4, (3, 49), (45, 76), 0.3], 7.232),
    ])
    def test_catmull_t_j(self, param, expected):
        '''Testing t_j method'''
        board_size = (60, 115)
        env_size = 20

        tension = 0
        velocity = 10

        view_point_object: ViewPointObject = {
            'view_point': None,
            'object_id': 10,
        }
        env = Environment(board_size, env_size, view_point_object)
        a_star = AStar()

        path_finding = PathFinding(
            env,
            a_star,
            tension,
            velocity
        )
        assert path_finding.catmull_t_j(param[0], param[1], param[2], param[3]
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
    def test_catmull_rom_segment(self, param, expected):
        '''Testing catmull_rom_segment method'''
        board_size = (60, 115)
        env_size = 20

        tension = 0
        velocity = 10

        view_point_object: ViewPointObject = {
            'view_point': None,
            'object_id': 10,
        }
        env = Environment(board_size, env_size, view_point_object)
        a_star = AStar()

        path_finding = PathFinding(
            env,
            a_star,
            tension,
            velocity
        )
        curve, velocity = path_finding.catmull_rom_segment(
            param[0], param[1], param[2], param[3], param[4], 5)
        for i, value in enumerate(curve):
            assert value[0] == pytest.approx(expected[0][i][0], 0.001)
            assert value[1] == pytest.approx(expected[0][i][1], 0.001)
        for i, value in enumerate(velocity):
            assert value[0] == pytest.approx(expected[1][i][0], 0.001)
            assert value[1] == pytest.approx(expected[1][i][1], 0.001)

    @pytest.mark.parametrize('param, expected', [
        ([[(3, 4), (4, 4), (5, 3), (6, 3)], 0.5],
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
        ([[(3, 4), (4, 4), (5, 5), (6, 5)], 0.5],
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
        ([[(10, 2), (9, 2), (8, 3), (7, 3)], 0.5],
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
        ([[(10, 7), (9, 7), (8, 6), (7, 6), [2, 3]], 0.5], [
            np.array([[9., 7.],
                     [8.74036439, 6.80092628],
                      [8.5, 6.5],
                      [8.25963561, 6.19907372],
                      [8., 6.],
                      [8., 6.],
                      [7.77491679, 5.96303889],
                      [7.54827569, 5.99746456],
                      [7.29749674, 6.03315795],
                      [7., 6.]],
                     ),
            np.array([[-0.92732365, - 0.38411003],
                      [-0.83009301, - 0.89799471],
                      [-0.7976828, - 1.06928961],
                      [-0.83009301, - 0.89799471],
                      [-0.92732365, - 0.38411003],
                      [-0.92732365, -0.38411003],
                      [-0.88839533,  0.04167515],
                      [-0.9397868 ,  0.18698414],
                      [-1.08149807,  0.05181691],
                      [-1.31352914, -0.36382651]],
                     )]),
    ])
    def test_catmull_rom_spline(self, param, expected):
        '''Testing catmull_rom_spline method'''
        board_size = (60, 115)
        env_size = 20

        tension = 0
        velocity = 10

        view_point_object: ViewPointObject = {
            'view_point': None,
            'object_id': 10,
        }
        env = Environment(board_size, env_size, view_point_object)
        a_star = AStar()

        path_finding = PathFinding(
            env,
            a_star,
            tension,
            velocity
        )
        curve, velocity = path_finding.catmull_rom_spline(
            param[0], param[1], 5)
        for i, value in enumerate(curve):
            assert value[0] == pytest.approx(expected[0][i][0], 0.001)
            assert value[1] == pytest.approx(expected[0][i][1], 0.001)
        for i, value in enumerate(velocity):
            assert value[0] == pytest.approx(expected[1][i][0], 0.001)
            assert value[1] == pytest.approx(expected[1][i][1], 0.001)
