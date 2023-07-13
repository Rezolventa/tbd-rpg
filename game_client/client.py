import json

import pygame

from game_client.controllers import GameController

pygame.init()
pygame.font.init()


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
                # - LEFT CLICK
                obj = game.action_man.handle_mouse_click()

                if game.action_man.state == 'idle':
                    if obj:
                        tile_rect = obj.rect
                        result = {
                            'action': 'GET_TILE_INFO',
                            'data': {
                                'x': tile_rect.x,
                                'y': tile_rect.y,
                            },
                        }
                        response = game.net_man.send(bytes(json.dumps(result), encoding='utf-8'))
                        print(response)
                elif game.action_man.state == 'choose_tile_to_move':
                    if obj:
                        tile_rect = obj.rect
                        result = {
                            'action': 'MOVE_PLAYER',
                            'data': {
                                'x': tile_rect.x,
                                'y': tile_rect.y,
                            },
                        }
                        response = json.loads(game.net_man.send(bytes(json.dumps(result), encoding='utf-8')))
                        print(response)
                        game.screen_man.sprites['player_image'].move_to(response['x'], response['y'])

        if running:
            game.action_man.handle_routine()
            game.screen_man.redraw()
            pygame.display.flip()


if __name__ == '__main__':
    main()
