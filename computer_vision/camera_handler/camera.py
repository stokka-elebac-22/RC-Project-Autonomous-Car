import cv2 as cv

class Camera:
    def __init__(self, qr_code, camera_id=0, delay=1, window_name='window'):
        self.camera_id = camera_id
        self.delay = delay
        self.window_name = window_name
        self.qcd = cv.QRCodeDetector()
        self.cap = cv.VideoCapture(self.camera_id)
        self.qr_code = qr_code

    def run(self, name=None, resize=1, verbose=1):
        if not name:
            self.run_video(verbose)
        else:
            self.run_image(name, resize, verbose)

    def run_video(self, verbose=1):
        while True:
            frame = self.read()
            self.detect_qr_code(frame, verbose=verbose)
            cv.imshow(self.window_name, frame)
            if cv.waitKey(self.delay) & 0xFF == ord('q'):
                break
        cv.destroyWindow(self.window_name)

    def run_image(self, name, resize, verbose=1):
        img = self.read(name, resize)
        self.detect_qr_code(img, resize, verbose)
        cv.imshow(name, img)
        cv.waitKey(0)

    def read(self, name=None, resize=1):
        if not name:
            ret, frame = self.cap.read()
            return ret, frame
        else:
            frame = cv.imread(name)
        frame = cv.resize(frame, (0, 0), fx = resize, fy = resize)
        return frame