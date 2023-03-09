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
    """Обработчик всяких разных событий на клиенте."""

    def __init__(self, game_controller):
        self.game_controller = game_controller
        self.hover_image = game_controller.screen_man.hover_image
        self.focus_image = game_controller.screen_man.focus_image
        self.tiles = self.game_controller.screen_man.get_tiles_as_list()
        self.icons = self.game_controller.screen_man.icons

    def get_hovered_object(self):
        """Возвращает спрайт, над которым в текущий момент находится курсор."""
        for tile in self.tiles:
            if tile.rect.collidepoint(pygame.mouse.get_pos()):
                return tile, 'tile'

        for icon in self.icons:
            if icon.rect.collidepoint(pygame.mouse.get_pos()):
                return icon, 'icon'
        return None, None

    def handle_routine(self):
        """Обрабатывает регулярные события."""
        self.handle_mouse_hover()

    def handle_mouse_hover(self):
        """Обрабатывает событие hover/cursor_over/mouse_over."""
        self.get_group('hover').remove(self.hover_image)
        obj, obj_type = self.get_hovered_object()
        if obj:
            self.hover_image.rect = obj.rect
            self.get_group('hover').add(self.hover_image)

    def handle_mouse_click(self):
        """Обрабатывает событие left mouse click."""
        self.get_group('focus').remove(self.focus_image)
        tile, obj_type = self.get_hovered_object()
        if tile:
            self.focus_image.rect = tile.rect
            self.get_group('focus').add(self.focus_image)
            return tile.rect

    def get_group(self, group_name):
        return self.game_controller.screen_man.get_group(group_name)
