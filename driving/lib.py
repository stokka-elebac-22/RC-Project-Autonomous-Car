'''This is the library for the driving logic'''
# ---------- Camera handler ----------#
from typing import List, Tuple
import cv2 as cv

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
