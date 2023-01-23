"""Importing needed libraries"""
import pytest
import cv2
import numpy as np
from computer_vision.line_detection.parking_slot_detection import ParkingSlotDetector
PATH = "computer_vision/line_detection/assets/parking"

class TestParametrized:
    """
    DOC: Testing ParkingSlotDetector class from module line_detection
    """
    def test_cluster_lines(self, lines, expected):
        """Test cluster_lines method of ParkingSlotDetector"""
        parking_slot_detector = ParkingSlotDetector()
        clustered_lines, clustered_coords = parking_slot_detector.cluster_lines(lines)
        assert clustered_lines == expected[0]
        assert clustered_coords == expected[1]

    def test_filter_lines(self, lines, coords, slope, intercept, expected):
        """Test filter_lines method of ParkingSlotDetector"""
        parking_slot_detector = ParkingSlotDetector()
        parking_slot_detector.filter_lines(lines, coords, slope, intercept)
        assert lines == expected[0]
        assert coords == expected[1]

    def test_get_min_max_x(self, coordinates, expected):
        """Test get_min_max_x method of ParkingSlotDetector"""
        parking_slot_detector = ParkingSlotDetector()
        min_x, max_x = parking_slot_detector.get_min_max_x(coordinates)
        assert min_x == expected[0]
        assert max_x == expected[1]

    def test_get_closest_line(self, line_coords, points, amount, expected):
        """Test get_closest_line method of ParkingSlotDetector"""
        parking_slot_detector = ParkingSlotDetector()
        lines = parking_slot_detector.get_closest_line(line_coords, points, amount)
        assert lines == expected

    def detect_parking_lines(self, image, qr_size_px, qr_size_mm, qr_distance):
        """Test parking_lines method of ParkingSlotDetector"""
        parking_slot_detector = ParkingSlotDetector()
        parking_slot_detector.detect_parking_lines(image, qr_size_px, qr_size_mm, qr_distance)

    def test_get_line_coordinates_from_parameters(self):
        """Test get_line_coordinates_from_parameters method of ParkingSlotDetector"""
        parking_slot_detector = ParkingSlotDetector()