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
        self.hover_image = game_controller.screen_man.hover_image
        self.focus_image = game_controller.screen_man.focus_image
        self.tiles = self.game_controller.screen_man.get_tiles_as_list()

    def handle_routine(self):
        self.handle_mouse_hover()

    def handle_mouse_hover(self):
        self.game_controller.screen_man.hover_group.remove(self.game_controller.screen_man.hover_image)
        for tile in self.tiles:
            if tile.rect.collidepoint(pygame.mouse.get_pos()):
                self.hover_image.rect = tile.rect
                self.game_controller.screen_man.hover_group.add(self.hover_image)

    def handle_mouse_click(self):
        self.game_controller.screen_man.focus_group.remove(self.game_controller.screen_man.focus_image)
        for tile in self.tiles:
            if tile.rect.collidepoint(pygame.mouse.get_pos()):
                self.focus_image.rect = tile.rect
                self.game_controller.screen_man.focus_group.add(self.focus_image)
