import os
import socket
import threading


class ThreadClient(threading.Thread):
    def __init__(self, server_ip, send_data, server_port=80):
        super(ThreadClient, self).__init__()
        self.send_data = send_data
        self.server_ip = server_ip
        self.server_port = server_port

    def run(self):
        if self.server_is_reachable():
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            self.client_socket.send(self.send_data.encode())
        else:
            return

    def server_is_reachable(self):
        exit_code = os.system(f'ping -c 3 {self.server_ip}')
        if exit_code == 0:
            return True
        else:
            return False
