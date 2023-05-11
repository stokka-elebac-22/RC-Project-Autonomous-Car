#!/usr/bin/env python
"""multi_socket_server.py: Multithread socket server for passing through CAN bus data from Embedded Linux."""

import socket
import time
import queue
from _thread import start_new_thread
from socket_handling.abstract_server import BasicServer, NetworkSettings

class MultiSocketServer(BasicServer):
    '''Socket Server for multiple clients'''
    def __init__(self, net_sett: NetworkSettings):
        self.server_side_socket = socket.socket()
        self.host = net_sett.host
        self.port = net_sett.port
        self.thread_count = 0
        self.running = False
        self.clients = []
        self.incoming_data  = queue.Queue()

    def __iter__(self):
        return self

    def start(self):
        '''Start server interface'''
        try:
            self.server_side_socket.bind((self.host, self.port))
        except socket.error as error:
            print(str(error))
        print('Socket is listening for connections...')
        self.server_side_socket.listen(5)
        self.running = True
        start_new_thread(self.run_socket, () )

    def stop(self):
        '''Stop server interface'''
        self.running = False

    def run_socket(self):
        '''Method for thread running socket server'''
        while self.running:
            client, address = self.server_side_socket.accept()
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            start_new_thread(self.multi_threaded_client, (client, ))
            self.clients.append(client)
            self.thread_count += 1
            print('Thread Number: ' + str(self.thread_count))
        self.server_side_socket.close()

    def multi_threaded_client(self, connection):
        '''Thread handling client'''
        connection.send(str.encode('Server is working:'))
        while True:
            try:
                data = connection.recv(2048)
                response = 'Server message: ' + data.decode('utf-8')
            except socket.error as error:
                self.thread_count -= 1
                print(f'Thread Number: {self.thread_count}')
                print(str(error))
                self.clients.remove(connection)
                break
            except UnicodeDecodeError as error:
                print(f"Decode error: {error}")
            if not data:
                break
            self.incoming_data.put(data)
            connection.sendall(str.encode(response))
        connection.close()

    def send_to_all(self, message):
        '''Send message to all connected clients'''
        if message is None:
            return
        for connection in self.clients:
            try:
                connection.sendall(message)
            except socket.error:
                continue
        print("Sending:")
        print(message)

    def get_next_message(self):
        '''Get next incoming message'''
        if not self.incoming_data.empty():
            return self.incoming_data.get()
        return None

    def __next__(self):
        '''Get next incoming message'''
        if not self.incoming_data.empty():
            return self.incoming_data.get()
        raise StopIteration

if __name__ == "__main__":
    # Receive message from socket, send message to all connected clients, and sleep.
    # This is meant for basic testing of server/client functionality by enabling basic transfer.
    print("Starting init")
    network_settings = NetworkSettings('10.0.10.95', 2004)
    socket_server = MultiSocketServer(network_settings)
    print("Created object")
    socket_server.start()
    print("Started server")
    while True:
        print("Get next available message, if any!")
        print(socket_server.get_next_message())
        print("Sending test message to any connected client")
        socket_server.send_to_all("test-message")
        print("Sleeping")
        time.sleep(1)
