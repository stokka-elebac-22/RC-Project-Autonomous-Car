'''
LIBRARY
Contains functions that is used in different scripts
'''
import os
import cv2 as cv
from computer_vision.camera_handler.lib import rotate_image

def display_arrow(conf, angle, distance) -> bool:
    '''Display the arrow or other symbols'''
    # ----- TEXT ----- #
    image_attributes = {
        'image_paths': conf['simulation']['image_paths'],
        'org': (25, 50),
        'font': cv.FONT_HERSHEY_SIMPLEX,
        'font_scale': 1,
        'color': (70, 70, 255),
        'thickness': 1
    }

    if angle is None or distance is None:
        return False

    distance = int(distance)
    arrow_image_path = image_attributes['image_paths']['arrow']
    if os.path.exists(arrow_image_path):
        img = cv.imread(arrow_image_path)
        img = rotate_image(img, angle) # rotate image
        img = cv.putText(
            img,
            f'Distance: {distance}',
            image_attributes['org'],
            image_attributes['font'],
            image_attributes['font_scale'],
            image_attributes['color'],
            image_attributes['thickness'],
            cv.LINE_AA)
        cv.imshow('', img)
        print(f'Move the car by {distance}mm at an angle of {angle} degrees.')
        cv.waitKey(0)
    else:
        print(f'Path does not exists: {image_attributes["image_paths"]["arrow"]}')
        raise FileNotFoundError
    return True
