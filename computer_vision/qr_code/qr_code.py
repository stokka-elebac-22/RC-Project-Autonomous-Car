'''QR code module.'''
import dataclasses
from typing import TypedDict, Tuple, List
import numpy as np
import cv2 as cv
from computer_vision.stereoscopic_vision.src.camera import Camera

QRSize = TypedDict('QRSize', {
    'px': int,
    'mm': int,
    'distance': int,
})
@dataclasses.dataclass
class QRGeometry:
    '''PointSet, used by qrcode.'''
    def __init__(self, size: QRSize=None, pts: List[Tuple[int, int]]=None):
        self.size = size
        if size is None:
            self.size = {}
        if self.size.get('px') is None:
            self.size['px'] = 1
        if self.size.get('mm') is None:
            self.size['mm'] = 1
        if self.size.get('distance') is None:
            self.size['distance'] = 1

        if pts is None or len(pts) < 4:
            pts = [[0,0],[0,0],[0,0],[0,0]]
        self.update(pts)

    def update(self, pts):
        '''update points, used by qrcode.'''
        if pts is None:
            return
        self.points = pts
        self.side_a = abs(self.points[0][0] - self.points[1][0])
        self.side_b = abs(self.points[1][1] - self.points[2][1])
        self.side_c = abs(self.points[2][0] - self.points[3][0])
        self.side_d = abs(self.points[3][1] - self.points[0][1])

    def get_width(self) -> int:
        '''Return the width'''
        width_px = max(abs(self.points[0][0] - self.points[1][0]),
        abs(self.points[2][0] - self.points[2][0]))
        return width_px

    def get_height(self) -> int:
        '''Return the height'''
        height_px = max(abs(self.points[2][1] - self.points[0][1]),
        abs(self.points[2][1] - self.points[1][1]))
        return height_px

    def get_angle(self) -> float:
        '''Return the angle'''
        width = self.get_width()
        height = self.get_height()
        if height == 0:
            return None
        ratio = width/height
        angle = (1 - ratio) * 90
        d_side = self.points[0][1] - self.points[3][1]
        b_side = self.points[1][1] - self.points[2][1]
        if d_side < b_side:
            angle = -angle
        return angle

    def get_distance(self) -> float:
        '''Return the distance'''
        height_px = self.get_height()
        focal_length = (self.size.get('px') / self.size.get('mm')) * self.size.get('distance')
        distance = (self.size.get('mm') * focal_length) / height_px
        return distance

QRData = TypedDict('QRData', {
    'ret': bool,
    'distances': List[float],
    'angles': List[float],
    'info': List[str],
    'points': List[Tuple],
    'rest': int,
})

DisplayData = TypedDict('DisplayData', {
    'distances': List[float],
    'angles': List[float],
    'info': List[str],
})

class QRCode:
    '''QRCode, doing calculations for QR code placement estimation.'''
#                          c
#            p2 ---------- p3
#            |             |
#         b  |             |  d
#            |             |
#            |             |
#            p1 ---------- p0
#                    a

    def __init__(self, size: QRSize, pts=None):
        self.qr_geometries = [QRGeometry(size, pts)]
        self.qr_display = DisplayQRCode()

    def get_data(self, frame: np.ndarray) -> QRData:
        '''Update values
        The resize variable is only relevant if not using video
        This function returns in a dict:
        - ret: bool, stating if it could detect the qr code
        - distances, angles: a float value for distance and angle
        - info: the decoded info
        - points: a list of points (formatted like [[[0, 0], ..., [1, 1]]])
        - rest: return straight value
        get_measurements(self, frame, resize=1) -> bool, float, float
        '''
        qcd = cv.QRCodeDetector()
        ret_qr, decoded_info , points_qr, rest_qr = qcd.detectAndDecodeMulti(frame)

        # add more QRGeometry if needed or delete if too many
        if not ret_qr:
            return {
            'ret': ret_qr,
            'distances': None,
            'angles': None,
            'info': None,
            'points': None,
            'rest': None
            }
        if len(self.qr_geometries) > len(points_qr):
            for _ in range(len(self.qr_geometries) - len(points_qr)):
                self.qr_geometries.pop()
        else:
            for i in range(len(points_qr) - len(self.qr_geometries)):
                size = {
                    'px': self.qr_geometries[i].size.get('px'),
                    'mm': self.qr_geometries[i].size.get('mm'),
                    'distance': self.qr_geometries[i].size.get('distance')
                }
                self.qr_geometries.append(QRGeometry(size))

        distances = []
        angles = []
        for i, points in enumerate(points_qr):
            self.qr_geometries[i].update(points)
            angles.append(self.qr_geometries[i].get_angle())
            distances.append(self.qr_geometries[i].get_distance())
        return {
            'ret': ret_qr,
            'distances': distances,
            'angles': angles,
            'info': decoded_info,
            'points': points_qr,
            'rest': rest_qr
            }

    def display(self, frame: np.ndarray, data: DisplayData, verbose=1):
        '''Displays the qr code with data'''
        self.qr_display.display(
            frame,
            self.qr_geometries,
            data,
            verbose=verbose
        )
class DisplayQRCode:
    '''DisplayQRCode, QR code placement estimation.'''
    def __init__(self):
        ##### DISPLAY #####
        self.color_frame_green = (0, 255, 0)
        self.color_frame_red = (0, 0, 255)

        self.font = cv.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.5
        self.text_color = (255, 0, 255)
        self.text_thickness = 1

    def display(self, frame: np.ndarray, qrgs: QRGeometry, data: DisplayData, verbose: int=1):
        '''
        Display
        returns a frame
        '''
        for i, qrg in enumerate(qrgs):
            if data['angles'] is None:
                angle = qrgs[i].get_angle()
            else:
                angle = data['angles'][i]
            if data['distances'] is None:
                distance = qrgs[i].get_distance()
            else:
                distance = data['distances'][i]

            if data['info'][i] is None:
                color = self.color_frame_green
            else:
                color = self.color_frame_red
            frame = cv.polylines(frame, [qrgs[i].points.astype(int)], True, color, 4)
            if verbose > 0:
                display_data = {'distance': distance, 'angle': angle}
                self.display_values(frame, qrg, display_data, verbose)
        return frame

    DisplayInfoData = TypedDict('DisplayInfoData', {
        'distance': int,
        'angle': int,
    })

    def display_values(self, frame, qrg: QRGeometry, data: DisplayData, verbose: int=1):
        '''Display values'''
        if verbose > 1:
            text_location_a = (int(min(qrg.points[0][0], qrg.points[1][0]) + \
                                    qrg.side_a/2), int(qrg.points[0][1]))
            text_location_b = (int(qrg.points[1][0]), int(min(qrg.points[1][1], \
                                    qrg.points[2][1]) + qrg.side_b/2))
            text_location_c = (int(min(qrg.points[2][0], qrg.points[3][0]) + \
                                    qrg.side_c/2), int(qrg.points[2][1]))
            text_location_d = (int(qrg.points[3][0]), int(min(qrg.points[2][1], \
                                    qrg.points[0][1]) + qrg.side_d/2))

            cv.putText(frame, str(int(qrg.side_a)), text_location_a, self.font, \
                        self.font_scale, self.text_color, self.text_thickness, cv.LINE_AA)
            cv.putText(frame, str(int(qrg.side_b)), text_location_b, self.font, \
                        self.font_scale, self.text_color, self.text_thickness, cv.LINE_AA)
            cv.putText(frame, str(int(qrg.side_c)), text_location_c, self.font, \
                        self.font_scale, self.text_color, self.text_thickness, cv.LINE_AA)
            cv.putText(frame, str(int(qrg.side_d)), text_location_d, self.font, \
                        self.font_scale, self.text_color, self.text_thickness, cv.LINE_AA)

        angle = data['angle']
        distance = data['distance']
        cv.putText(frame, f'angle    = {int(angle)}', (10, 20), self.font, \
                            self.font_scale * 1.5, self.text_color, self.text_thickness, cv.LINE_AA)
        cv.putText(frame, f'distance = {int(distance)}', (10, 50), \
                self.font, self.font_scale * 1.5, self.text_color, self.text_thickness, cv.LINE_AA)

# def local_read_camera(name: str=None, resize: int=1):
#     '''Local read camera '''
#     if not name:
#         ret, frame = cap.read()
#         if not ret:
#             raise SystemError
#     else:
#         frame = cv.imread(name)
#     frame = cv.resize(frame, (0, 0), fx = resize, fy = resize)
#     return frame


if __name__ == '__main__':
    # ----- ORIGINAL MEASUREMENTS -----
    # QR Code measured, 55mm lense
    SIZE = {
        'px': 76,
        'mm': 52,
        'distance': 500
    }
    qr_code = QRCode(SIZE)
    CAMERA_ID = 0
    DELAY = 1
    WINDOW_NAME = 'window'
    # cap = cv.VideoCapture(CAMERA_ID)
    cam = Camera(CAMERA_ID)
    VERBOSE = 1

    ##### VALUES #####
    VALUES_LENGTH = 10

    def filter_angle(angles):
        '''Filter angle'''
        for i, angle in enumerate(angles):
            if angle is None:
                return
            angles_lists[i].pop(0)
            angles_lists[i].append(angle)

    def filter_distance(distances):
        '''filter distance values'''
        for i, distance in enumerate(distances):
            if distance is None:
                return
            distances_lists[i].pop(0)
            distances_lists[i].append(distance)

    angles_lists = [[0 for _ in range(VALUES_LENGTH)]]
    distances_lists = [[0 for _ in range(VALUES_LENGTH)]]

    while True:
        # img = cv.imread('tests/images/qr_code/logi_1080p/distance/distance_30.jpg')
        # img = local_read_camera()
        ret, img = cam.read()
        if not ret:
            continue
        qr_data = qr_code.get_data(img)

        if len(angles_lists) < len(qr_data['angles']):
            for _ in range(len(qr_data['angles']) - len(angles_lists)):
                angles_lists.append([0 for _ in range(VALUES_LENGTH)])
        if len(distances_lists) < len(qr_data['distances']):
            for _ in range(len(qr_data['distances']) - len(distances_lists)):
                distances_lists.append([0 for _ in range(VALUES_LENGTH)])
        filter_angle(qr_data['angles'])
        filter_distance(qr_data['distances'])
        if qr_data['ret']:
            average_angles = [int(sum(angles_list)//VALUES_LENGTH) \
                for angles_list in angles_lists]
            average_distance = [int(sum(distances_list)//VALUES_LENGTH) \
                for distances_list in distances_lists]
            qr_code_measurements = {
                'distances': average_distance,
                'angles': average_angles,
                'info': qr_data['info']}
            qr_code.display(img, qr_code_measurements, verbose=2)
        cv.imshow(WINDOW_NAME, img)
        if cv.waitKey(DELAY) & 0xFF == ord('q'):
            break
    cv.destroyWindow(WINDOW_NAME)
