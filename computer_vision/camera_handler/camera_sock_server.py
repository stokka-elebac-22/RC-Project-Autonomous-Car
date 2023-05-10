'''camera_socket_server.py: Camera socket server.'''

import base64
from _thread import start_new_thread
import socket
import cv2
import imutils
from socket_handling.abstract_server import BasicServer, NetworkSettings

class CamSocketStream(BasicServer): # pylint: disable=R0902
    '''Class for streaming socket video'''

    def __init__(self, net_conf: NetworkSettings) -> None:
        # host_name = socket.gethostname()
        # host_ip = socket.gethostbyname(host_name)
        # print(host_ip)
        self.BUFF_SIZE = 65536   # pylint: disable=C0103
        self.WIDTH = 400         # pylint: disable=C0103
        self.host_ip = net_conf.host
        self.port = net_conf.port
        self.socket_address = (self.host_ip, self.port)
        self.frame = 0

        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF, self.BUFF_SIZE)
        self.running = False

    def start(self):
        '''start server'''
        self.running = True
        start_new_thread(self.run_socket, () )

    def run_socket(self):
        '''Run image socket server'''
        self.server_socket.bind(self.socket_address)
        print('Camera socket listening at:',self.socket_address)
        while True:
            _, client_addr = self.server_socket.recvfrom(self.BUFF_SIZE)
            print('GOT connection from ',client_addr)

            while self.running:
                try:
                    frame = imutils.resize(self.frame,width=self.WIDTH)
                    _, buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
                    message = base64.b64encode(buffer)
                    self.server_socket.sendto(message,client_addr)
                    self.frame = 0
                except: # pylint: disable=W0702
                    pass
            self.server_socket.close()

    def stop(self):
        '''Stopping server'''
        self.running = False

    def send_to_all(self, message):
        '''Send message to all!'''
        if self.running:
            self.frame = message

    def get_next_message(self): # pylint: disable=R0201
        '''Will not receive data on the socket video stream'''
        return None

# fps,st,frames_to_count,cnt = (0,0,20,0)
# Old FPS calculation here:
# frame = cv2.putText(frame,'FPS: '+str(fps),
# (10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
# cv2.imshow('TRANSMITTING VIDEO',frame)
# if cnt == frames_to_count:
#     try:
#         fps = round(frames_to_count/(time.time()-st))
#         st=time.time()
#         cnt=0
#     except: # pylint: disable=W0702
#         pass
# cnt+=1
