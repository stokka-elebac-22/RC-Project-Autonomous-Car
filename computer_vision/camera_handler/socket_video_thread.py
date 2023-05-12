'''camera_handler.py: DATBAC23 camera functionality library'''
__copyright__ = 'Copyright 2023, DATBAC23'
__license__ = 'Apache-2.0'
__version__ = '0.1.0'
__status__ = 'Testing'
import socket
import base64
import time
import cv2
import numpy as np
from socket_handling.abstract_server import NetworkSettings
from PyQt6.QtCore import pyqtSignal, QThread

class SocketVideoThread(QThread):
    '''Video Thread'''
    change_pixmap_signal = pyqtSignal(np.ndarray)
    camera_id = 0

    def __init__(self, network_settings: NetworkSettings):
        super().__init__()
        self._run_flag = True
        self.network_settings = network_settings

    # pylint: disable=R0914 R0912 R0915
    def run(self): # pylint: disable=R0801
        '''Run'''
        BUFF_SIZE = 65536
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
        fps,time_step,frames_to_count,cnt = (0,0,20,0) # pylint: disable=W0612
        host_ip = self.network_settings.host
        port = self.network_settings.port
        # client_socket.connect((self.network_settings.host, self.network_settings.port))
        message = b'Hello'

        client_socket.sendto(message,(host_ip,port))
        print(f"Camera connecting to: {host_ip}:{port}")
        while self._run_flag:
            packet,_ = client_socket.recvfrom(BUFF_SIZE)
            data = base64.b64decode(packet,' /')
            npdata = np.fromstring(data,dtype=np.uint8)
            frame = cv2.imdecode(npdata,1)
            # frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
            self.change_pixmap_signal.emit(frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
                break
            if cnt == frames_to_count:
                try:
                    fps = round(frames_to_count/(time.time()-time_step))
                    time_step=time.time()
                    cnt=0
                except: # pylint: disable=W0702
                    pass
            cnt+=1

    # pylint: disable=R0801
    def stop(self):
        '''Sets run flag to False and waits for thread to finish'''
        self._run_flag = False
        self.wait()

# pylint: disable=R0902
if __name__ == '__main__':
    pass
