from datetime import datetime

import pygame


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
    def __init__(self, game_controller):
        self.game_controller = game_controller
        # TODO: не место здесь
        self.focus_image = game_controller.screen_man.focus_image

    def handle(self):
        self.handle_mouse_hover()

    def handle_mouse_hover(self):
        self.game_controller.screen_man.focus_group.remove(self.game_controller.screen_man.focus_image)
        for tile in self.game_controller.screen_man.get_tiles_as_list():
            if tile.rect.collidepoint(pygame.mouse.get_pos()):
                self.focus_image.rect = tile.rect
                self.game_controller.screen_man.focus_group.add(self.focus_image)

    def handle_mouse_click(self):
        pass
