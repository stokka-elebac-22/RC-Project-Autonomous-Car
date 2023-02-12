'''tmp module.'''

def detect_qr_code(self, frame, resize=1, verbose=1):
    '''tmp docstring.'''
    ret_qr, decoded_info, points, rest = self.qcd.detectAndDecodeMulti(frame)
    if not ret_qr:
        return
    self.qr_code.update(ret_qr, decoded_info, points, rest)
    self.qr_code.display(frame, resize, verbose=verbose)
