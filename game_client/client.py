import json

import pygame

from game_client.controllers import GameController

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
                # - LEFT CLICK
                tile_rect = game.action_man.handle_mouse_click()

                if tile_rect:
                    result = {
                        'action': 'GET_TILE_INFO',
                        'data': {
                            'x': tile_rect.x,
                            'y': tile_rect.y,
                        },
                    }
                    response = game.net_man.send(bytes(json.dumps(result), encoding='utf-8'))
                    print(response)

        if running:
            game.action_man.handle_routine()
            game.screen_man.redraw()
            pygame.display.flip()


if __name__ == '__main__':
    main()
