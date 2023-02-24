"""socket_client.py: Class for Client side socket connection."""
# __author__ = "Asbjørn Stokka"
# __copyright__ = "Copyright 2022, ELEBAC"
# __credits__ = ["Asbjørn Stokka"]
# __license__ = "Apache-2.0"
# __version__ = "0.1.0"
# __maintainer__ = "Asbjørn Stokka"
# __email__ = "asbjorn@maxit-as.com"
# __status__ = "Testing"

import socket
from defines import *
from _thread import *
from abstract_storage import *
from db_handler import *

class socket_client():
    def __init__(self, storage_class: abstract_storage, connection: tuple[str, int]):
        self.storage = storage_class
        self.conn_details = connection
        self.client_socket = socket.socket()

    def start(self) -> None:
        self.running = True
        start_new_thread(self.run_server, )

    def run_server(self) -> None:
        self.client_socket.connect(self.conn_details)
        try:
            while self.running:
                data = self.client_socket.recv(1024)
                if not data == None:
                    # print('Received from server: ' + data.hex())  # show in terminal
                    try:
                        if (Message_Id(data[0]) == Message_Id.CAN_SENSOR_DATA_ID):
                            print(Message_Id(data[0]).name + " " + Position(data[1]).name + " - Sensor value: " + str(data[8]))
                            self.storage.add_log(data[1], data[2], data[8])
                        elif (Message_Id(data[0]) == Message_Id.CAN_TEST_MSG_ID):
                            print("Test message received")
                        else:
                            for x in range(len(data)):
                                print(data[x])
                    except:
                        print(error)
                        pass
                    #print(hex(data[1]))
                    #print(''.join('{:02x}'.format(x) for x in data))
        except KeyboardInterrupt:
            pass

    def send_to_all(self, message) -> None:
        self.client_socket.sendall(message)

    def stop(self) -> None:
        self.running = False
        self.client_socket.close()


if __name__ == '__main__':
    database = db_handler(":memory:")
    host = "10.0.10.95" #socket.gethostname()  # when both code is running on same pc
    port = 2004  # socket server port number
    client_conn = socket_client(database, (host, port))
    # client_conn.start()
    while True:
        pass
