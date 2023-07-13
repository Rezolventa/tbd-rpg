from datetime import datetime
from collections import OrderedDict

import pygame

from const import TILE_SIDE_PX


WHITE = (255, 255, 255)


class ScreenManager:
    """Менеджер объектов на экране клиента."""

    group_list = ['map', 'player', 'actions', 'hover', 'focus']

    tile_mapping = {
        'M': 'mountain_tile',
        'F': 'forest_tile',
        'S': 'swamp_tile',
    }

    # TODO: should be received from server
    map_scheme = [
        'MSFXXXXXXXXXXXXX',
        'SSFXXXXXXXXXXXXX',
        'MSMXXXXXXXXXXXXX',
        'FFFXXXXXXXXXXXXX',
        'XXXXXXXXXXXXXXXX',
        'XXXXXXXXXXXXXXXX',
        'XXXXXXXXXXXXXXXX',
        'XXXXXXXXXXXXXXXX',
        'XXXXXXXXXXXXXXXX',
        'XXXXXXXXXXXXXXXX',
        'XXXXXXXXXXXXXXXX',
        'XXXXXXXXXXXXXXXX',
        'XXXXXXXXXXXXXXXX',
        'XXXXXXXXXXXXXXXX',
        'XXXXXXXXXXXXXXXX',
        'XXXXXXXXXXXXXXXX',
    ]

    def __init__(self):
        self.window = pygame.display.set_mode((31 * TILE_SIDE_PX, 18 * TILE_SIDE_PX))
        self.sprites = self.init_sprites()
        self.sprite_groups = self.init_groups()

        # map_frame
        map_frame = self.sprites['map_frame']
        map_frame.move_to(32, 32, self.get_group('map'))

        self.tiles = self.init_map()

        # info_frame
        info_frame = self.sprites['info_frame']
        info_frame.move_to(576, 32, self.get_group('map'))

        # action_frame
        action_frame = UIPanel(self.get_group('actions'), 576, 448, self.sprites['action_frame'])
        action_frame.add_button(self.sprites['move_icon'])

        self.icons = [self.sprites['move_icon']]

        # player
        player = self.sprites['player_image']
        player.move_to(32, 32, self.get_group('player'))

        self.hover_image = self.sprites['hover_image']
        self.focus_image = self.sprites['focus_image']

        pygame.display.set_caption('Client')

    @staticmethod
    def init_sprites():
        sprite_dict = dict()

        # Фреймы
        sprite_dict['map_frame'] = CommonSprite('img/map_frame.jpg')
        sprite_dict['info_frame'] = CommonSprite('img/info_frame.jpg')
        sprite_dict['action_frame'] = CommonSprite('img/action_frame.jpg')
        sprite_dict['player_image'] = CommonSprite('img/player.png', 2)

        sprite_dict['tile_move'] = CommonSprite('img/tile_move.png')

        # Элементы UI
        sprite_dict['hover_image'] = CommonSprite('img/tile_focus.png')
        sprite_dict['focus_image'] = CommonSprite('img/tile_focus.png')
        sprite_dict['move_icon'] = CommonSprite('img/icon_move.jpg', 2)
        sprite_dict['move_icon_hover'] = CommonSprite('img/icon_move_hover.jpg', 2)

        return sprite_dict

    def init_groups(self):
        """Инициализирует все спрайт-группы."""
        groups = OrderedDict()

        for group_name in self.group_list:
            groups[group_name] = pygame.sprite.Group()

        return groups

    def get_group(self, name):
        """Получает спрайт-группу по имени."""
        return self.sprite_groups.get(name)

    # TODO: Требует регламентации названия спрайтов
    def get_sprite(self, sprite_type, sprite_name):
        """Упрощает обращение к спрайтам."""
        key = '{}_{}'.format(sprite_name, sprite_type)
        # return self.sprite_store[key]

    def init_map(self):
        """Подгружает и располагает спрайты тайлов на карте."""
        tiles = []
        for i in range(16):
            row = []
            for j in range(16):
                tile_symbol = self.map_scheme[i][j]
                if tile_symbol == 'X':
                    continue
                x = self.sprites['map_frame'].rect.x + j * TILE_SIDE_PX
                y = self.sprites['map_frame'].rect.x + i * TILE_SIDE_PX
                sprite = CommonSprite('img/{}.jpg'.format(self.tile_mapping[tile_symbol]), 2)
                sprite.move_to(x, y)
                self.sprite_groups['map'].add(sprite)
                row.append(sprite)
            tiles.append(row)
        return tiles

    # TODO: вообще говоря, не используется в этом классе
    def get_tiles_as_list(self):
        """Представляет тайлы в виде списка."""
        tiles_as_list = []
        for row in self.tiles:
            tiles_as_list += [tile for tile in row]
        return tiles_as_list

    def redraw(self):
        """
        Рисует спрайт-группы в установленном в self.sprite_groups порядке.
        Вызывается каждый такт.
        """
        for name, group in self.sprite_groups.items():
            group.update()
            group.draw(self.window)


class CommonSprite(pygame.sprite.Sprite):
    """Модифицированный Sprite, класс-прототип для всех спрайтов."""

    def __init__(self, image, scaling=None):
        super().__init__()
        self.image = self.get_scaled_image(image, scaling) if scaling else pygame.image.load(image)
        self.rect = self.image.get_rect()

    @staticmethod
    def get_scaled_image(image, k):
        """
        Подгружает спрайт и увеличивает его размер в k раз.
        """
        image = pygame.image.load(image)

        if image.get_alpha():
            image = image.convert_alpha()
        else:
            image = image.convert()
            image.set_colorkey(WHITE)

        size = image.get_size()
        return pygame.transform.scale(image, (int(size[0] * k), int(size[1] * k)))

    def move_to(self, x, y, group=None):
        self.rect.topleft = (x, y)

        if group is not None:
            group.add(self)


class UIPanel:
    """
    Прототип для элемента интерфейса Панель.
    Автоматически располагает одинаковые прямоугольные кнопки.
    Если покажет себя хорошо, по его примеру сделаем остальные элементы UI.
    """

    def __init__(self, sprite_group, x, y, background_sprite):
        self.sprite_group = sprite_group
        self.x = x
        self.y = y
        self.button_width = TILE_SIDE_PX
        self.button_height = TILE_SIDE_PX
        self.spacing = TILE_SIDE_PX / 2
        self.buttons = []

        # Состояния
        self.active = False

        background_sprite.move_to(576, 448, self.sprite_group)

    def add_button(self, button: CommonSprite):
        """Определят место для новой кнопки, добавляет её спрайт в группу."""
        button_x = self.x + self.spacing + self.button_width * len(self.buttons)
        button_y = self.y + self.spacing
        button.move_to(button_x, button_y, self.sprite_group)
        self.buttons.append(button)

    def show(self):
        """Включает отображение элемента интерфейса."""
        self.active = True

    def hide(self):
        """Выключает отображение элемента интерфейса."""
        self.active = False
