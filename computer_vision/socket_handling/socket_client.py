"""socket_client.py: Class for Client side socket connection."""

import socket
from _thread import start_new_thread
from socket_handling.abstract_server import NetworkSettings
from socket_handling.abstract_storage import AbstractStorage
from socket_handling.db_handler import DbHandler
try:
    from computer_vision.defines import MessageId, Position
except ImportError:
    from defines import MessageId, Position

class SocketClient():
    '''Socket Client'''
    def __init__(self, storage_class: AbstractStorage):
        self.storage = storage_class
        self.connection = NetworkSettings("", 0)
        self.client_socket = socket.socket()
        self.running = False

    def start(self, connection: NetworkSettings) -> None:
        '''Start Socket client'''
        self.running = True
        self.connection = connection
        start_new_thread(self.run_server, )

    def run_server(self) -> None:
        '''Run socket client'''
        self.client_socket.connect(self.conn_details)
        try:
            while self.running:
                data = self.client_socket.recv(1024)
                if not data is None:
                    # print('Received from server: ' + data.hex())  # show in terminal
                    try:
                        if MessageId(data[0]) == MessageId.CAN_SENSOR_DATA_ID:
                            print(MessageId(data[0]).name + " " +
                                  Position(data[1]).name + " - Sensor value: " + str(data[8]))
                            self.storage.add_log(data[1], data[2], data[8])
                        elif MessageId(data[0]) == MessageId.CAN_TEST_MSG_ID:
                            print("Test message received")
                        else:
                            for x in range(len(data)):  # pylint: disable=C0200
                                print(data[x])
                    except:  # pylint: disable=W0702
                        print("error")

                    #print(hex(data[1]))
                    #print(''.join('{:02x}'.format(x) for x in data))
        except KeyboardInterrupt:
            pass

    def send_to_all(self, message) -> None:
        '''Send message to all connections'''
        self.client_socket.sendall(message)

    def stop(self) -> None:
        '''Stop running/Disconnect'''
        self.running = False
        self.client_socket.close()


if __name__ == '__main__':
    database = DbHandler(":memory:")
    HOST = "10.0.10.95"
    PORT = 2004
    # client_conn = SocketClient(database, (HOST, PORT))
    while True:
        pass
