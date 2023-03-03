import json
import socket
from _thread import start_new_thread
from datetime import datetime

from django.forms import model_to_dict

from const import SERVER_ADDRESS, TILE_SIDE_PX
from orm.config import *  # django.core.exceptions.ImproperlyConfigured
from orm.models import Player, TileTemplate, TileGeo


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

    def execute(self, connection, data=None):
        if data:
            data = json.loads(data)
            action = data.get('action')
            if action == 'GET_TILE_INFO':
                self.send_tile_info(connection, data.get('data'))
        else:
            time_count = self.get_time_count()
            print('Server time:', time_count)
            connection.send(str.encode(time_count))

    def send_tile_info(self, connection, data: dict):
        tile_info = self.data_manager.get_tile_info(data)
        connection.send(bytes(json.dumps(model_to_dict(tile_info)), encoding='utf-8'))

    def get_time_count(self):
        return str(int((datetime.now() - self.server_started_at).total_seconds()))


class DataManager:
    def __init__(self):
        pass

    @staticmethod
    def get_tile_info(data: dict):
        try:
            x = data.get('x') / TILE_SIDE_PX
            y = data.get('y') / TILE_SIDE_PX
            tile_geo = TileGeo.objects.get(x=x, y=y)
        except KeyError:
            print('KeyError > x: {}, y: {}'.format(data.get('x'), data.get('y')))
            return
        return tile_geo.template


def main():
    session_id = 0
    server = Server()

    while True:
        connection, ip = server.socket.accept()
        print('Connected to:', ip)

        if not Player.objects.all().exists():
            tts1 = TileTemplate.objects.create(type=TileTemplate.TileTypes.SWAMP, tier=1, loot_spots=2, hidden_loot_spots=1)
            TileTemplate.objects.create(type=TileTemplate.TileTypes.SWAMP, tier=2, loot_spots=1, hidden_loot_spots=2)
            TileTemplate.objects.create(type=TileTemplate.TileTypes.SWAMP, tier=3, loot_spots=4, hidden_loot_spots=2)

            ttf1 = TileTemplate.objects.create(type=TileTemplate.TileTypes.FOREST, tier=1, loot_spots=2, hidden_loot_spots=0)
            TileTemplate.objects.create(type=TileTemplate.TileTypes.FOREST, tier=2, loot_spots=2, hidden_loot_spots=1)
            TileTemplate.objects.create(type=TileTemplate.TileTypes.FOREST, tier=3, loot_spots=4, hidden_loot_spots=2)

            ttm7 = TileTemplate.objects.create(type=TileTemplate.TileTypes.MOUNTAINS, tier=1, loot_spots=1, hidden_loot_spots=0)
            TileTemplate.objects.create(type=TileTemplate.TileTypes.MOUNTAINS, tier=2, loot_spots=1, hidden_loot_spots=1)
            TileTemplate.objects.create(type=TileTemplate.TileTypes.MOUNTAINS, tier=3, loot_spots=2, hidden_loot_spots=2)

            TileGeo.objects.create(x=1, y=1, template=ttm7)
            TileGeo.objects.create(x=2, y=1, template=tts1)
            TileGeo.objects.create(x=3, y=1, template=ttf1)

            TileGeo.objects.create(x=1, y=2, template=tts1)
            TileGeo.objects.create(x=2, y=2, template=tts1)
            TileGeo.objects.create(x=3, y=2, template=ttf1)

            TileGeo.objects.create(x=1, y=3, template=ttm7)
            TileGeo.objects.create(x=2, y=3, template=tts1)
            TileGeo.objects.create(x=3, y=3, template=ttm7)

            TileGeo.objects.create(x=1, y=4, template=ttf1)
            TileGeo.objects.create(x=2, y=4, template=ttf1)
            TileGeo.objects.create(x=3, y=4, template=ttf1)

            Player.objects.create(name='Test', stamina=100)

        start_new_thread(server.handle_client, (connection, session_id))
        session_id += 1


if __name__ == '__main__':
    main()
