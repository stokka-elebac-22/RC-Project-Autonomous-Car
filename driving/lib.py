'''This is the library for the driving logic'''
# ---------- Camera handler ----------#
import os
import sys
from typing import List, Tuple
import numpy as np
import cv2 as cv

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

# pylint: disable=C0413
from computer_vision.pathfinding.pathfinding import PathFinding
from computer_vision.qr_code.qr_code import QRCode, QRData

def get_available_cameras() -> Tuple[bool, List[int]]:
    '''
    Returns the index of the available cameras and
    a bool value, indicating if the list is empty or not'''
    index = 0
    cameras = []
    while True:
        cap = cv.VideoCapture(index)
        if not cap.read()[0]:
            break
        cameras.append(index)
        cap.release()
        index += 1
    if len(cameras) == 0:
        return False, None
    return True, cameras

def get_cam_center(frame: np.ndarray) -> Tuple[int, int]:
    '''Returns the shape of the frame'''
    height, width, _ = frame.shape
    return (width, height)

def get_qr_code_distance(data: QRData,
                         qr_code: QRCode,
                         path_finding: PathFinding) -> List[Tuple[int]]:
    '''Return the distances from the QR Code'''
    qr_distances: List[Tuple[int, int]] = []
    for i in range(len(data['info'])):
        min_dist = min(
            data['points'][i][0][0] - path_finding.center[0],
            data['points'][i][1][0] - path_finding.center[0],
            data['points'][i][1][0] - path_finding.center[0],
            data['points'][i][2][0] - path_finding.center[0],
        )
        distance_x = min_dist = qr_code.focal_length
        distance_y = data['distances'][0]
        qr_distances.append((distance_x, distance_y))
    return qr_distances
