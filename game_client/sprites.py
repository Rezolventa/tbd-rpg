import pygame

from const import TILE_SIDE_PX

WHITE = (255, 255, 255)


class SpriteFactory:
    @staticmethod
    def get_scaled_image(image, k):
        image = pygame.image.load(image)

        if image.get_alpha():
            image = image.convert_alpha()
        else:
            image = image.convert()
            image.set_colorkey(WHITE)

        size = image.get_size()
        return pygame.transform.scale(image, (int(size[0] * k), int(size[1] * k)))

    def create(self, image, x, y):
        return CommonSprite(self.group, image, x, y)


class UIFactory(SpriteFactory):
    """Отвечает за иниицализацию спрайтов UI."""

    def run(self, map_group, player_group, hover_group, focus_group):
        # Фреймы - окна интерфейса
        map_frame = CommonSprite(map_group, pygame.image.load('img/map_frame.jpg'), 32, 32)
        info_frame = CommonSprite(map_group, pygame.image.load('img/info_frame.jpg'), 576, 32)
        action_frame = CommonSprite(map_group, pygame.image.load('img/action_frame.jpg'), 576, 448)
        player = PlayerFactory(32, 32).run(player_group)

        # Элементы UI
        hover_image = CommonSprite(
            hover_group, self.get_scaled_image('img/tile_focus.png', 2), 16, 16, 'hover_image'
        )
        hover_group.remove(hover_image)
        focus_image = CommonSprite(
            focus_group, self.get_scaled_image('img/tile_focus.png', 2), 16, 16, 'focus_image'
        )
        focus_group.remove(focus_image)

        result = {
            'map_frame': map_frame,
            'player': player,
            'info_frame': info_frame,
            'action_frame': action_frame,
            'hover_image': hover_image,
            'focus_image': focus_image,
        }
        return result


class PlayerFactory(SpriteFactory):
    """Отвечает за иниицализацию спрайтов игрока."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def run(self, group):
        return CommonSprite(group, self.get_scaled_image('img/player.png', 2), self.x, self.y)


class MapTilesFactory(SpriteFactory):
    """Отвечает за иниицализацию спрайтов основной карты."""

    def __init__(self, map_scheme, map_frame, group):
        self.map_scheme = map_scheme
        self.map_frame = map_frame
        self.group = group
        self.tile_mapping = {
            'M': 'mountain_tile',
            'F': 'forest_tile',
            'S': 'swamp_tile',
        }

    def run(self):
        tiles = []
        for i in range(16):
            row = []
            for j in range(16):
                tile_symbol = self.map_scheme[i][j]
                if tile_symbol == 'X':
                    continue
                x = self.map_frame.x + j * 32
                y = self.map_frame.x + i * 32
                image = self.get_scaled_image('img/{}.jpg'.format(self.tile_mapping[tile_symbol]), 2)
                sprite = self.create(image, x, y)
                row.append(sprite)
            tiles.append(row)
        return tiles


class ScreenManager:
    """Менеджер объектов на экране клиента."""

    def __init__(self):
        self.window = pygame.display.set_mode((31 * TILE_SIDE_PX, 18 * TILE_SIDE_PX))

        self.ui_group = pygame.sprite.Group()
        self.map_group = pygame.sprite.Group()
        self.hover_group = pygame.sprite.GroupSingle()
        self.focus_group = pygame.sprite.GroupSingle()
        self.player_group = pygame.sprite.GroupSingle()

        pygame.display.set_caption('Client')

        ui = UIFactory().run(self.map_group, self.player_group, self.hover_group, self.focus_group)

        map_frame = ui['map_frame']

        # TODO: should be received from server
        self.map_scheme = [
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

        self.tiles = MapTilesFactory(self.map_scheme, map_frame, self.map_group).run()
        self.hover_image = ui['hover_image']
        self.focus_image = ui['focus_image']

    def get_tiles_as_list(self):
        tiles = []
        for row in self.tiles:
            tiles += [tile for tile in row]
        return tiles

    def redraw(self):
        """Определяет порядок отображения слоёв (групп) на экране."""
        self.ui_group.update()
        self.ui_group.draw(self.window)
        self.map_group.update()
        self.map_group.draw(self.window)
        self.hover_group.update()
        self.hover_group.draw(self.window)
        self.focus_group.update()
        self.focus_group.draw(self.window)
        self.player_group.update()
        self.player_group.draw(self.window)


class CommonSprite(pygame.sprite.Sprite):
    """Модифицированный Sprite, класс-прототип для всех спрайтов."""

    def __init__(self, group, image, x, y, name=None):
        super().__init__(group)
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.name = name
        # self.focus_on = False


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
