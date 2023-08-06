import socket

from const import SERVER_ADDRESS


class NetworkManager:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = SERVER_ADDRESS

        self.client.connect(self.address)
        self.client.recv(2048).decode()  # data for start: player_info

    def send(self, data):
        try:
            self.client.send(data)
            return self.client.recv(2048).decode()
        except socket.error as e:
            print('socket.error:', e)
