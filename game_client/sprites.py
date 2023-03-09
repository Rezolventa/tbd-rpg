from collections import OrderedDict

import pygame

from const import TILE_SIDE_PX

WHITE = (255, 255, 255)


def get_scaled_image(image, k):
    """
    Подгружает спрайт и увеличивает его размер в k раз.
    Сейчас это функция-хелпер, но чуть позже станет понятно, в какой класс её отнести.
    """
    image = pygame.image.load(image)

    if image.get_alpha():
        image = image.convert_alpha()
    else:
        image = image.convert()
        image.set_colorkey(WHITE)

    size = image.get_size()
    return pygame.transform.scale(image, (int(size[0] * k), int(size[1] * k)))


class ScreenManager:
    """Менеджер объектов на экране клиента."""
    group_list = ['map', 'hover', 'focus', 'player', 'actions']

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

        self.sprite_groups = self.init_groups()
        self.sprite_store = self.init_sprites()

        # map_frame
        map_frame = self.sprite_store['map_frame']
        map_frame.move_to(32, 32, self.get_group('map'))

        self.tiles = self.init_map()

        # info_frame
        info_frame = self.sprite_store['info_frame']
        info_frame.move_to(576, 32, self.get_group('map'))

        # action_frame
        action_frame = UIPanel(self.get_group('actions'), 576, 448, self.sprite_store['action_frame'])
        action_frame.add_button(self.sprite_store['move_icon'])

        # player
        player = self.sprite_store['player']
        player.move_to(32, 32, self.get_group('player'))

        self.hover_image = self.sprite_store['hover_image']
        self.focus_image = self.sprite_store['focus_image']

        pygame.display.set_caption('Client')

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
        return self.sprite_store[key]

    @staticmethod
    def init_sprites():
        """Инициализирует основные спрайты UI."""
        # Фреймы - окна интерфейса
        map_frame = CommonSprite('img/map_frame.jpg')
        info_frame = CommonSprite('img/info_frame.jpg')
        action_frame = CommonSprite('img/action_frame.jpg')
        player = CommonSprite('img/player.png', 2)

        # Элементы UI
        hover_image = CommonSprite('img/tile_focus.png', 2)
        focus_image = CommonSprite('img/tile_focus.png', 2)
        move_icon = CommonSprite('img/icon_move.jpg', 2)

        return {
            'map_frame': map_frame,
            'info_frame': info_frame,
            'action_frame': action_frame,
            'player': player,
            'hover_image': hover_image,
            'focus_image': focus_image,
            'move_icon': move_icon,
        }

    def init_map(self):
        """Подгружает и располагает спрайты тайлов на карте."""
        tiles = []
        for i in range(16):
            row = []
            for j in range(16):
                tile_symbol = self.map_scheme[i][j]
                if tile_symbol == 'X':
                    continue
                x = self.sprite_store['map_frame'].rect.x + j * TILE_SIDE_PX
                y = self.sprite_store['map_frame'].rect.x + i * TILE_SIDE_PX
                sprite = CommonSprite('img/{}.jpg'.format(self.tile_mapping[tile_symbol]), 2)
                sprite.move_to(x, y)
                self.sprite_groups['map'].add(sprite)
                row.append(sprite)
            tiles.append(row)
        return tiles

    def get_tiles_as_list(self):
        """Представляет тайлы в виде списка."""
        tiles_as_list = []
        for row in self.tiles:
            tiles_as_list += [tile for tile in row]
        return tiles_as_list

    def redraw(self):
        """
        Отрисовывает спрайт-группы в установленном в self.sprite_groups порядке.
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

    def get_scaled_image(self, image, k):
        return get_scaled_image(image, k)

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


# class Textbox(pygame.sprite.Sprite):
#     font = pygame.font.SysFont('serif', 18)
#
#     def __init__(self, text):
#         super().__init__()
#         self.text = text
#         self.image = self.font.render(text, False, (0, 255, 0))
#         self.rect = self.image.get_rect()
#         self.pos_x = 30
#         self.pos_y = 30
#
#     def draw(self, win):
#         win.blit(self.image, (self.pos_x, self.pos_y))
