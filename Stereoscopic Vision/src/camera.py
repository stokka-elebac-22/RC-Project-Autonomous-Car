import cv2 as cv
class Camera:
    def __init__(self, camera_id=0, window_name='window'):
        self.camera_id = camera_id
        self.window_name = window_name
        self.qcd = cv.QRCodeDetector()
        self.cap = cv.VideoCapture(self.camera_id)

    def show(self):
        ret, frame = self.read()
        if ret:
            cv.imshow(self.window_name, frame)

    def read(self, name=None, resize=1) -> int:
        if not name:
            ret, frame = self.cap.read()
            if not ret:
                return ret, None
        else:
            frame = cv.imread(name)
        frame = cv.resize(frame, (0, 0), fx = resize, fy = resize)
        return 1, frame