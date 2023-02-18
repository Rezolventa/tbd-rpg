import socket
from _thread import start_new_thread
from datetime import datetime

from const import SERVER_ADDRESS
from orm.config import *  # django.core.exceptions.ImproperlyConfigured
from orm.models import Player, TileInfo


class Server:
    def __init__(self):
        self.server_started_at = datetime.now()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.bind(SERVER_ADDRESS)
        except socket.error as e:
            print(e)

        self.socket.listen(2)  # limiter?
        print('Waiting for connections. Server started.')

    def get_time_count(self):
        return str(int((datetime.now() - self.server_started_at).total_seconds()))

    def handle_client(self, connection, player):
        connection.send(str.encode(self.get_time_count()))

        while True:
            try:
                data = connection.recv(2048).decode()

                if not data:
                    print('Client disconnected')
                    break

                print('Incoming message:', data)

                # -- tile info test --
                if data == 'GET_TILE_INFO':
                    tile_info = TileInfo.objects.first()
                    print(
                        'TILE INFO',
                        'loot spots:',
                        tile_info.loot_spots,
                        'hidden loot spots',
                        tile_info.hidden_loot_spots,
                    )

                time_count = self.get_time_count()
                print('Server time:', time_count)

                # TODO: send json
                connection.send(str.encode(str(tile_info.loot_spots)))
            except Exception as e:
                print('Error in handling client', e)
                break


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
