import socket
from _thread import start_new_thread
from datetime import datetime

from orm.config import *
from orm.models import Player

from const import SERVER_ADDRESS


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

    # --- db test ---
    def test_add_stamina(self):
        player = Player.objects.last()
        player.stamina += 1
        player.save()

    def handle_client(self, connection, player):
        connection.send(str.encode(self.get_time_count()))

        while True:
            try:
                data = connection.recv(2048).decode()

                if not data:
                    print('Client disconnected')
                    break

                print('Client time:', data)

                time_count = self.get_time_count()
                print('Server time:', time_count)

                connection.sendall(str.encode(time_count))
                self.test_add_stamina()
            except Exception as e:
                print('Error in handling client', e)
                break


def main():
    session_id = 0
    server = Server()

    # --- db test ---
    Player.objects.create(
        name='Rez',
        stamina=100,
    )

    while True:
        connection, ip = server.socket.accept()
        print('Connected to:', ip)

        start_new_thread(server.handle_client, (connection, session_id))
        session_id += 1


if __name__ == '__main__':
    main()
