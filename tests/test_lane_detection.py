'''Importing needed libraries'''
import pytest
import cv2
import numpy as np
from computer_vision.line_detection.lane_detection import LaneDetector
PATH = 'computer_vision/line_detection/assets/'


class TestParametrized:
    '''
    DOC: Testing TrafficSignDetection class from module traffic_sign_detection
    '''

    def get_image(self, source):
        '''Helping function for tests to get a cv2 image from a source file'''
        image = cv2.imread(PATH + source)
        return image

    @pytest.mark.parametrize('img_source', ['bike_park.jpg', 'curve.jpg', '1.jpg', '2.jpg'])
    def test_get_lane_region(self, img_source):
        '''Test if the output image is not equal to the input image'''
        lane_detector = LaneDetector()
        original_image = self.get_image(img_source)

        new_image = lane_detector.get_region_of_interest(original_image)
        difference = cv2.subtract(original_image, new_image)
        b_color, g_color, r_color = cv2.split(difference)
        assert new_image.shape != original_image.shape or cv2.countNonZero(
            b_color) != 0 or cv2.countNonZero(g_color) != 0 or cv2.countNonZero(r_color) != 0

    @pytest.mark.parametrize('img_source, line, expected', [
        ('bike_park.jpg', [-0.8819273, 822.19240925],
         [-2469, 3000, -632, 1380]),
        ('curve.jpg', [-0.123, 423.], [-20951, 3000, -7780, 1380]),
        ('1.jpg', [1.881, -0.493], [1595, 3000, 733, 1380]),
        ('2.jpg', [2.34, 423.1924], [1101, 3000, 408, 1380])])
    def test_get_line_coordinates_from_parameters(self, img_source, line, expected):
        '''Test if the output coordinates are equal to the expected coordinates'''
        lane_detector = LaneDetector()
        image = self.get_image(img_source)

        coordinates = lane_detector.get_line_coordinates_from_parameters(
            image, line)

        assert coordinates[0] == expected[0]
        assert coordinates[1] == expected[1]
        assert coordinates[2] == expected[2]
        assert coordinates[3] == expected[3]

    @pytest.mark.parametrize('lines, expected', [
        ([np.array([300, 327, 1059, 600]), np.array([0, 781, 272, 561]),
          np.array([573, 339, 780, 336])],
         [np.array([-0.412, 564.152]),
          np.array([0.3596837944664031, 219.09486166007926])]),

        ([np.array([751, 327, 1059, 500]), np.array([0, 781, 272, 561])],
         [np.array([-0.809, 781.0]), np.array([0.5616883116883115, -94.82792207792211])]),

        ([np.array([123, 434, 343, 767]), np.array([0, 781, 272, 561]),
          np.array([394, 781, 122, 561]), np.array([573, 339, 780, 336])],
         [np.array([-0.4116581415174767, 564.1521739130434]),
          np.array([1.161229946524065, 355.0731283422457])]),

        ([np.array([100, 327, 509, 811])],
         [None, np.array([1.18337408, 208.66259169])])])
    def test_get_average_lines(self, lines, expected):
        '''Test if the output average lines is equal to the expected average lines'''
        lane_detector = LaneDetector()
        avg_lines = lane_detector.get_average_lines(lines)

        if expected[0] is None:
            assert avg_lines[0] is None
        else:
            avg_lines[0] = np.array([np.round(i, 3) for i in avg_lines[0]])
            expected[0] = np.array([np.round(i, 3) for i in expected[0]])
            assert (avg_lines[0] == expected[0]).all()
        if expected[1] is None:
            assert avg_lines[1] is None
        else:
            avg_lines[1] = np.array([np.round(i, 3) for i in avg_lines[1]])
            expected[1] = np.array([np.round(i, 3) for i in expected[1]])
            assert (avg_lines[1] == expected[1]).all()

    @pytest.mark.parametrize('img_source, lines, expected', [
        ('bike_park.jpg', [np.array([300, 327, 1059, 600]),
         np.array([0, 781, 272, 561])], 92.5),
        ('curve.jpg', [np.array([751, 327, 1059, 500]),
         np.array([0, 781, 272, 561])], 81.225),
        ('1.jpg', [np.array([123, 434, 343, 767]),
         np.array([0, 781, 272, 561])], 96.925),
        ('2.jpg', [np.array([100, 327, 509, 811]), np.array([573, 339, 780, 336])], 83.175)])
    def test_get_diff_from_center_info(self, img_source, lines, expected):
        '''Test if the output value is equal to the manual calculation value'''
        lane_detector = LaneDetector()
        image = self.get_image(img_source)
        diff = np.round(
            lane_detector.get_diff_from_center_info(image, lines), 3)
        assert diff == expected

    @pytest.mark.parametrize('img_source, lines, expected', [
        ('bike_park.jpg', [np.array([300, 327, 1059, 600]),
         np.array([0, 781, 272, 561])], (193, 823)),
        ('curve.jpg', [np.array([751, 327, 1059, 500]),
         np.array([0, 781, 272, 561])], (-657, 1044)),
        ('1.jpg', [np.array([123, 434, 343, 767]),
         np.array([0, 781, 272, 561])], (953, 1034)),
        ('2.jpg', [np.array([100, 327, 509, 811]), np.array([573, 339, 780, 336])], (546, 333))])
    def test_get_next_point(self, img_source, lines, expected):
        '''
        Test if the output value from
        get_next_point is equal to manual calculation
        '''
        lane_detector = LaneDetector()
        image = self.get_image(img_source)
        new_point = lane_detector.get_next_point(image, lines)
        assert new_point == expected

    @pytest.mark.parametrize('img_source, lines, expected', [
        ('bike_park.jpg',
         [np.array([300, 327, 1059, 600]), np.array([0, 781, 272, 561])],
         [(3000, 300, 3),
          np.array(
             [[4.66628436e-02, -1.29732961e-01,  2.84238251e+01],
              [1.54723157e-01, -3.12223397e+00,  1.70948856e+03],
              [-7.81961244e-04, -1.59153913e-03,  1.00000000e+00]]),
          np.array([(2000, 3000), (1075, 2400), (150, 1800)]),
          np.array([np.array([7.01241782e-04, -1.50766983e+00,  3.21037253e+03]),
                    np.array([-7.01241782e-04,  1.50766983e+00,  1.58962747e+03])])]),

        ('curve.jpg',
         [np.array([751, 327, 1059, 500]), np.array([0, 781, 272, 561])],
         [(3000, 751, 3),
          np.array(
             [[-9.35875535e-02,  1.66618303e-01,  1.58000675e+01],
              [2.27146016e-01,  2.93055597e+00, -1.70582562e+03],
              [-1.13845455e-03, -1.03160965e-03,  1.00000000e+00]]
         ),
             np.array([(2000, 3000), (1187, 2400), (375, 1800)]),
             np.array([np.array([9.08876084e-04, -2.15858070e+00,  3.68165706e+03]),
                      np.array([-9.08876084e-04,  2.15858070e+00,  1.11834294e+03])])]),


        ('1.jpg',
         [np.array([123, 434, 343, 767]), np.array([0, 781, 272, 561])],
         [(3000, 123, 3),
          np.array([[-7.12919550e-01,  4.70997901e-01, -1.16723984e+02],
                    [-1.76094441e+01,  6.06927443e+00,  1.38490585e+03],
                    [-7.81450264e-03,  1.33376405e-03,  1.00000000e+00]
                    ]),
          np.array([(2000, 3000), (1030, 2400), (61, 1800)]),
          np.array([np.array([6.38345409e-04, -1.31562989e+00,  3.07787814e+03]),
                    np.array([-6.38345409e-04,  1.31562989e+00,  1.72212186e+03])])]),

        ('2.jpg',
         [np.array([100, 327, 509, 811]), np.array([0, 781, 272, 561])],
         [(3000, 100, 3),
          np.array([[3.55484821e-01, -3.00399363e-01,  6.26821097e+01],
                    [1.07330901e+01, -1.01749694e+01,  2.78875734e+03],
                    [3.16837462e-03, -3.48181553e-03,  1.00000000e+00]]),
          np.array([(2000, 3000), (1025, 2400), (50, 1800)]),
          np.array([np.array([6.31163708e-04, -1.29388560e+00,  3.06311637e+03]),
                    np.array([-6.31163708e-04,  1.29388560e+00,  1.73688363e+03])])])])
    def test_get_course(self, img_source, lines, expected):
        '''Test if the output value is equal to the manual calculation value'''
        lane_detector = LaneDetector()
        image = self.get_image(img_source)
        data = lane_detector.get_course(
            image, lines)
        assert data['warped_shape'] == expected[0]
        assert data['perspective_transform'] == pytest.approx(expected[1], rel=1e-3)
        assert (data['points'] == expected[2]).all()
        assert data['polys'] == pytest.approx(expected[3], rel=1e-3)

    @pytest.mark.parametrize('img_source, shape, transform, points, polys', [
        ('bike_park.jpg',
         (3000, 300, 3),
         np.array(
             [[4.66628436e-02, -1.29732961e-01,  2.84238251e+01],
              [1.54723157e-01, -3.12223397e+00,  1.70948856e+03],
              [-7.81961244e-04, -1.59153913e-03,  1.00000000e+00]]),
         np.array([(2000, 3000), (1075, 2400), (150, 1800)]),
         np.array([np.array([7.01241782e-04, -1.50766983e+00,  3.21037253e+03]),
                  np.array([-7.01241782e-04,  1.50766983e+00,  1.58962747e+03])])),

        ('curve.jpg',
         (3000, 751, 3),
         np.array(
             [[-9.35875535e-02,  1.66618303e-01,  1.58000675e+01],
              [2.27146016e-01,  2.93055597e+00, -1.70582562e+03],
              [-1.13845455e-03, -1.03160965e-03,  1.00000000e+00]]
         ),
            np.array([(2000, 3000), (1187, 2400), (375, 1800)]),
            np.array([np.array([9.08876084e-04, -2.15858070e+00,  3.68165706e+03]),
                      np.array([-9.08876084e-04,  2.15858070e+00,  1.11834294e+03])])),


        ('1.jpg',
         (3000, 123, 3),
         np.array([[-7.12919550e-01,  4.70997901e-01, -1.16723984e+02],
                  [-1.76094441e+01,  6.06927443e+00,  1.38490585e+03],
                  [-7.81450264e-03,  1.33376405e-03,  1.00000000e+00]
                   ]),
         np.array([(2000, 3000), (1030, 2400), (61, 1800)]),
         np.array([np.array([6.38345409e-04, -1.31562989e+00,  3.07787814e+03]),
                  np.array([-6.38345409e-04,  1.31562989e+00,  1.72212186e+03])])),

        ('2.jpg',
         (3000, 100, 3),
         np.array([[3.55484821e-01, -3.00399363e-01,  6.26821097e+01],
                  [1.07330901e+01, -1.01749694e+01,  2.78875734e+03],
                  [3.16837462e-03, -3.48181553e-03,  1.00000000e+00]]),
         np.array([(2000, 3000), (1025, 2400), (50, 1800)]),
         np.array([np.array([6.31163708e-04, -1.29388560e+00,  3.06311637e+03]),
                  np.array([-6.31163708e-04,  1.29388560e+00,  1.73688363e+03])]))])

    def test_show_course(self, img_source, shape, transform, points, polys): # pylint: disable=R0913
        '''Test if the output value is equal to the manual calculation value'''
        lane_detector = LaneDetector()
        image = self.get_image(img_source)
        images = lane_detector.show_course(
            image, shape, points, transform, polys)
        difference = cv2.subtract(image, images['weighted'])
        b_color, g_color, r_color = cv2.split(difference)
        assert image.shape != images['warped'].shape
        assert image.shape != images['weighted'].shape or cv2.countNonZero(
            b_color) != 0 or cv2.countNonZero(g_color) != 0 or cv2.countNonZero(r_color) != 0
