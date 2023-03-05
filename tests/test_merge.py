'''Importing needed libraries'''
import pytest
from computer_vision.line_detection.parking_slot_detection import MergeLines

class TestParametrized:
    '''
    DOC: Testing TrafficSignDetection class from module traffic_sign_detection
    '''

    @pytest.mark.parametrize('source, expected',
        [([(3, 2), (5, 4), (5, 2), (7,3), (5, 5)], [(4.883036880224505,2.779240779943874), 0.7853981633974483, (1.4257499971667364, 1.7066601391111706)])])
    def test_ok(self, source, expected):
        merge_lines = MergeLines()
        centroid = merge_lines.centroid(source[0], source[1], source[2], source[3])
        assert centroid == expected[0]
        orientation_r = merge_lines.merged_line_orientation(source[0], source[1], source[2], source[3])
        assert merge_lines.orientation(source[0], source[1]) == expected[1]
        assert merge_lines.transform_to_another_axis(centroid, source[4], orientation_r) == expected[2]
        assert merge_lines.transform_to_orig_axis(centroid, expected[2], orientation_r) == source[4]
        assert merge_lines.merge_lines(source[0], source[1], source[2], source[3]) != None