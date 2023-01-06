import cv2 as cv

from qr_code import QRCode

class Camera:
    def __init__(self, qr_code, camera_id=0, delay=1, window_name='window'):
        self.camera_id = camera_id
        self.delay = delay
        self.window_name = window_name
        self.qcd = cv.QRCodeDetector()
        self.cap = cv.VideoCapture(self.camera_id)
        self.qr_code = qr_code

    def run(self, name=None, resize=1):
        if not name:
            self.run_video()
        else:
            self.run_image(name, resize)

    def run_video(self):
        while True:
            frame = self.read()
            self.detect_qr_code(frame)
            cv.imshow(self.window_name, frame)
            if cv.waitKey(self.delay) & 0xFF == ord('q'):
                break
        cv.destroyWindow(self.window_name)
    
    def run_image(self, name, resize):
        img = self.read(name, resize)
        self.detect_qr_code(img, resize)
        cv.imshow(name, img)
        cv.waitKey(0)

    def read(self, name=None, resize=1):
        if not name:
            ret, frame = self.cap.read()
            if not ret:
                raise SystemError
        else:
            frame = cv.imread(name)
        frame = cv.resize(frame, (0, 0), fx = resize, fy = resize)
        return frame

    def detect_qr_code(self, frame, resize=1):
        ret_qr, decoded_info, points, rest = self.qcd.detectAndDecodeMulti(frame)
        if not ret_qr:
            # print('Cannot detect')
            return
        self.qr_code.update(ret_qr, decoded_info, points, rest)
        self.qr_code.display(frame, resize)
