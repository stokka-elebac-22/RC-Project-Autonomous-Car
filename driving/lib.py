'''This is the library for the driving logic'''
# ---------- Camera handler ----------#
from typing import List, Tuple
import cv2 as cv

def get_available_cameras() -> Tuple[bool, List[int]]:
    '''
    Returns the index of the available cameras and
    a bool value, indicating if the list is empty or not'''
    cameras: List[int] = []
    index = 0
    while True:
        ret, cap = cv.VideoCapture(index)
        if not ret:
            break
        cap.release()
        cameras.append(index)
        index += 1
    if len(cameras) == 0:
        return False, None
    return True, cameras
