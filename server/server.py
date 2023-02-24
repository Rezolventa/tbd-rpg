import json
import socket
from _thread import start_new_thread
from datetime import datetime

from django.forms import model_to_dict

from const import SERVER_ADDRESS
from orm.config import *  # django.core.exceptions.ImproperlyConfigured
from orm.models import Player, TileInfo


class Server:
    def __init__(self):
        self.api = API()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.bind(SERVER_ADDRESS)
        except socket.error as e:
            print(e)

        self.socket.listen(2)  # limiter?
        print('Waiting for connections. Server started.')

    def handle_client(self, connection, player):
        self.api.execute(connection)

        while True:
            try:
                data = connection.recv(2048).decode()

                if not data:
                    print('Client disconnected')
                    break

                print('Incoming message:', data)
                self.api.execute(connection, data)
            except Exception as e:
                print('Error in handling client', e)
                break


class API:
    """Интерфейс клиент-серверного взаимодействия."""

    def __init__(self):
        self.server_started_at = datetime.now()
        self.data_manager = DataManager()

    def execute(self, connection, command=None):
        if command == 'GET_TILE_INFO':
            self.send_tile_info(connection)
        else:
            time_count = self.get_time_count()
            print('Server time:', time_count)
            connection.send(str.encode(time_count))

    def send_tile_info(self, connection):
        tile_info = self.data_manager.get_tile_info()
        connection.send(bytes(json.dumps(model_to_dict(tile_info)), encoding='utf-8'))

    def get_time_count(self):
        return str(int((datetime.now() - self.server_started_at).total_seconds()))


class DataManager:
    def __init__(self):
        pass

    @staticmethod
    def get_tile_info():
        tile_info = TileInfo.objects.first()
        print(
            'TILE INFO',
            'loot spots:',
            tile_info.loot_spots,
            'hidden loot spots',
            tile_info.hidden_loot_spots,
        )
        return tile_info


def main():
    session_id = 0
    server = Server()

    Player.objects.get_or_create(name='Rez', defaults={'stamina': 100})

    while True:
        connection, ip = server.socket.accept()
        print('Connected to:', ip)

        start_new_thread(server.handle_client, (connection, session_id))
        session_id += 1


if __name__ == '__main__':
    main()
