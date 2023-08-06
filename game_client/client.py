import pygame

from game_client.actions import ActionManager
from game_client.network import NetworkManager
from game_client.sprites import ScreenManager

pygame.init()
pygame.font.init()


class GameController:
    """Контроллер, управляющий основными процессами игры."""

    def __init__(self):
        self.net_man = NetworkManager()
        self.screen_man = ScreenManager()
        # self.player = PlayerManager()
        self.action_man = ActionManager(self)


def main():
    game = GameController()
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
                game.action_man.handle_mouse_click()

        if running:
            game.action_man.handle_routine()
            game.screen_man.redraw()
            pygame.display.flip()


if __name__ == '__main__':
    main()
