import pygame
from sprites import GameController

pygame.init()
pygame.font.init()

game = GameController()


def main():
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
                game.net_man.send(str.encode(game.player.get_time_count))
                game.action_man.handle_mouse_click()

        if running:
            game.action_man.handle()
            game.screen_man.redraw()
            pygame.display.flip()


if __name__ == '__main__':
    main()
