from datetime import datetime

import pygame

from network import NetworkManager
from sprites import ScreenManager

pygame.init()
pygame.font.init()


class Player:
    def __init__(self):
        self.client_connected_at = datetime.now()
        self.time_count = None

    @property
    def get_time_count(self):
        self.time_count = int((datetime.now() - self.client_connected_at).total_seconds())
        return str(int((datetime.now() - self.client_connected_at).total_seconds()))

    def draw(self):
        if not self.time_count:
            return


class ActionManager:
    def handle(self, event):
        pass


def main():
    net_man = NetworkManager()
    screen_man = ScreenManager()
    player = Player()

    action_man = ActionManager()

    clock = pygame.time.Clock()

    running = True

    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                break
            elif event.type == pygame.MOUSEBUTTONUP:
                net_man.send(str.encode(player.get_time_count))

        if running:
            screen_man.window.fill((0, 0, 0))
            screen_man.redraw()
            pygame.display.flip()


if __name__ == '__main__':
    main()

"""
Цвет текста - от важности
вместо ников - иконки
"""