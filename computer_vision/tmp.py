import cv2 as cv

def run(self, name=None, resize=1, verbose=1):
    """tmp docstring."""
    if not name:
        self.run_video(verbose)
    else:
        self.run_image(name, resize, verbose)

def run_video(self, verbose=1):
    """tmp docstring."""
    while True:
        frame = self.read()
        self.detect_qr_code(frame, verbose=verbose)
        cv.imshow(self.window_name, frame)
        if cv.waitKey(self.delay) & 0xFF == ord('q'):
            break
    cv.destroyWindow(self.window_name)

def run_image(self, name, resize, verbose=1):
    """tmp docstring."""
    img = self.read(name, resize)
    self.detect_qr_code(img, resize, verbose)
    cv.imshow(name, img)
    cv.waitKey(0)

def detect_qr_code(self, frame, resize=1, verbose=1):
    """tmp docstring."""
    ret_qr, decoded_info, points, rest = self.qcd.detectAndDecodeMulti(frame)
    if not ret_qr:
        # print('Cannot detect')
        return
    self.qr_code.update(ret_qr, decoded_info, points, rest)
    self.qr_code.display(frame, resize, verbose=verbose)
