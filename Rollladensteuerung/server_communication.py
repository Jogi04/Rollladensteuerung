import socket
import threading


class ServerSocketThread(threading.Thread):
    def __init__(self, ip, data):
        super().__init__()
        self.ip = ip
        self.data = data

    def run(self):
        print('started')
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.ip, 80))
        client_socket.send(self.data.encode())
        client_socket.close()
        print('closed')
