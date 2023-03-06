'''Importing needed libraries'''
import pytest
from computer_vision.line_detection.lib import MergeLines

class TestParametrized:
    '''
    DOC: Testing MergeLines class from module LineDetection
    '''

    @pytest.mark.parametrize('source, expected',
        [([(0, 0), (3, 4)], 5),
         ([(1.07, 1.92), (2.85, 2.37)], 1.84),
         ([(0.95, 3.68), (2.05, 3.16)], 1.22)])
    def test_length(self, source, expected):
        '''Test the method length'''
        merge_lines = MergeLines()
        length = merge_lines.length(source[0][0], source[0][1], source[1][0], source[1][1])
        assert length == pytest.approx(expected, 0.01)

    @pytest.mark.parametrize('source, expected',
        [([(0, 0), (3, 4), (2, 3), (1, 2)], (1.5, 2.1102406046057713)),
         ([(1.07, 1.92), (2.85, 2.37), (2.32, 4.23), (0.21, 0.31)],
          (1.4679360135050359, 2.233500716995497)),
         ([(0.95, 3.68), (2.05, 3.16), (1.07, 1.92), (2.85, 2.37)],
          (1.7766585402644914, 2.653174698179942))])
    def test_centroid(self, source, expected):
        '''Test the method centroid'''
        merge_lines = MergeLines()
        centroid = merge_lines.centroid(source[0], source[1], source[2], source[3])
        for i, val in enumerate(centroid):
            assert val == pytest.approx(expected[i], 0.01)

    @pytest.mark.parametrize('source, expected',
        [([(0, 0), (3, 4)], 0.9272952180016122),
         ([(1.07, 1.92), (2.85, 2.37)], 0.24762066490566068),
         ([(0.95, 3.68), (2.05, 3.16)], 2.700000291282502)])
    def test_orientation(self, source, expected):
        '''Test the method orientation'''
        merge_lines = MergeLines()
        orientation = merge_lines.orientation(source[0], source[1])
        assert orientation == pytest.approx(expected, 0.01)

    @pytest.mark.parametrize('source, expected',
        [([(0, 0), (3, 4), (2, 3), (1, 2)], 0.8960095838189298),
         ([(1.07, 1.92), (2.85, 2.37), (2.32, 4.23), (0.21, 0.31)], 0.8348310150309226),
         ([(0.95, 3.68), (2.05, 3.16), (1.07, 1.92), (2.85, 2.37)], -0.6643914592731471)])
    def test_merged_line_orientation(self, source, expected):
        '''Test the method centroid'''
        merge_lines = MergeLines()
        orientation = merge_lines.merged_line_orientation(
            source[0], source[1], source[2], source[3])
        assert orientation == expected

    @pytest.mark.parametrize('source, expected',
        [([(0, 0), (3, 4), 0.8960095838189298],
          (4.997553222317881, 0.15640265375038176)),
         ([(1.07, 1.92), (2.85, 2.37), 0.8348310150309226],
          (1.5284516220506221, -1.017219562852987)),
         ([(0, 0), (3, 4), 0.8960095838189298],
          (5, 0.15640265375038176))])
    def test_transform_to_another_axis(self, source, expected):
        '''Test the method transform_to_another_axis'''
        merge_lines = MergeLines()
        point = merge_lines.transform_to_another_axis(source[0], source[1], source[2])
        assert point[0] == pytest.approx(expected[0], 0.01)
        assert point[1] == pytest.approx(expected[1], 0.01)

    @pytest.mark.parametrize('source, expected',
        [([(0, 0), (4.997553222317881, 0.15640265375038176), 0.8960095838189298], (3, 4)),
         ([(1.07, 1.92), (1.5284516220506221, -1.017219562852987), 0.8348310150309226], (3, 2)),
         ([(0, 0), (5, 0.15640265375038176), 0.8960095838189298], (3, 4))])
    def test_transform_to_orig_axis(self, source, expected):
        '''Test the method transform_to_orig_axis'''
        merge_lines = MergeLines()
        point = merge_lines.transform_to_orig_axis(source[0], source[1], source[2])
        assert point[0] == pytest.approx(expected[0], 0.01)
        assert point[1] == pytest.approx(expected[1], 0.01)

    @pytest.mark.parametrize('source, expected',
        [([(0, 0), (3, 4), (2, 3), (1, 2)], [3, 4, 0, 0]),
         ([(1.07, 1.92), (2.85, 2.37), (2.32, 4.23), (0.21, 0.31)], None),
         ([(0.95, 3.68), (2.05, 3.16), (1.07, 1.92), (2.85, 2.37)], None),
         ([(4, 4), (6, 6), (3.05, 2.08), (8.13, 7.41)], [8, 8, 3, 2]),
         ([(0.92, 1.58), (6, 6), (3.05, 2.08), (8.13, 7.41)], [8, 8, 1, 1])])
    def test_merge_lines(self, source, expected):
        '''Test the method merge_lines'''
        merge_lines = MergeLines()
        line = merge_lines.merge_lines(source[0], source[1], source[2], source[3])
        if line is None:
            assert line == expected
        else:
            assert line[0] == pytest.approx(expected[0], 0.01)
            assert line[1] == pytest.approx(expected[1], 0.01)
            assert line[2] == pytest.approx(expected[2], 0.01)
            assert line[3] == pytest.approx(expected[3], 0.01)

    @pytest.mark.parametrize('source, expected',
        [([[0, 0, 3, 4], [2, 3, 1, 2],
           [1.07, 1.92, 2.85, 2.37], [2.32, 4.23, 0.21, 0.31],
           [0.95, 3.68, 2.05, 3.16], [1.07, 1.92, 2.85, 2.37],
           [4, 4, 6, 6], [3.05, 2.08, 8.13, 7.41],
            [0.92, 1.58, 6, 6], [3.05, 2.08, 8.13, 7.41]
           ], 3)])
    def test_merge_all_lines(self, source, expected):
        '''Test the method merge_all_lines'''
        merge_lines = MergeLines()
        lines = merge_lines.merge_all_lines(source)
        assert len(lines) == expected
