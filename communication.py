import os
import socket


class Client:
    def __init__(self, send_data, server_ip):
        self.send_data = send_data
        self.server_ip = server_ip
        if self.server_is_reachable():
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(self.server_ip)
            self.client_socket.send(self.send_data.encode())
        else:
            return

    def server_is_reachable(self):
        ip = list(self.server_ip)[0]
        print(ip)
        if os.system(f'ping -c 1 {ip}') is 0:
            return True
        else:
            return False
