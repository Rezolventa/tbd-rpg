import pygame

from const import TILE_SIDE_PX


class ActionManager:
    """Обработчик всяких разных событий на клиенте."""

    def __init__(self, game_controller):
        self.game_controller = game_controller
        self.tiles = game_controller.screen_man.get_tiles_as_list()
        self.icons = game_controller.screen_man.icons

        self.sprites = self.game_controller.screen_man.sprites
        self.state = 'idle'

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
        self.get_group('hover').remove(self.sprites['hover_image'])
        obj, obj_type = self.get_hovered_object()
        if obj:
            self.sprites['hover_image'].rect = obj.rect
            self.get_group('hover').add(self.sprites['hover_image'])

    def handle_mouse_click(self):
        """Обрабатывает событие left mouse click."""
        self.get_group('focus').remove(self.sprites['focus_image'])
        obj, obj_type = self.get_hovered_object()
        if obj_type == 'tile':
            # Клик на тайл карты
            if self.state == 'idle':
                self.sprites['focus_image'].rect = obj.rect
                self.get_group('focus').add(self.sprites['focus_image'])
            elif self.state == 'choose_tile_to_move':
                self.sprites['tile_move'].rect = obj.rect
                self.get_group('focus').add(self.sprites['tile_move'])
                # TODO: как вариант, через 1.5 секунды исчезает
            return obj

        if obj_type == 'icon':
            hover_image = self.sprites['move_icon_hover']
            # Клик на иконку передвижения
            if self.state == 'idle':
                hover_image.rect = obj.rect
                self.get_group('focus').add(hover_image)
                self.state = 'choose_tile_to_move'
            elif self.state == 'choose_tile_to_move':
                self.get_group('focus').remove(hover_image)
                self.state = 'idle'
            return obj

    def get_group(self, group_name):
        """Возвращает спрайт-группу."""
        return self.game_controller.screen_man.get_group(group_name)

    def move_player(self, x, y):
        self.sprites['player_image'].move_to(x * TILE_SIDE_PX, y * TILE_SIDE_PX)
