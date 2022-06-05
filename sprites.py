import pygame

from const import TILE_SIDE_PX
from network import NetworkManager
from player import Player, ActionManager

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
    def run(self, group, focus_group):
        map_frame = CommonSprite(group, pygame.image.load('sprites/map_frame.jpg'), 32, 32)
        info_frame = CommonSprite(group, pygame.image.load('sprites/info_frame.jpg'), 576, 32)
        action_frame = CommonSprite(group, pygame.image.load('sprites/action_frame.jpg'), 576, 448)
        player = PlayerFactory(32, 32).run(group)
        # TODO: не место здесь
        focus_image = CommonSprite(focus_group, self.get_scaled_image('sprites/tile_focus.png', 2), 16, 16)
        result = {
            'map_frame': map_frame,
            'player': player,
            'info_frame': info_frame,
            'action_frame': action_frame,
            'focus_image': focus_image,
        }
        return result


class PlayerFactory(SpriteFactory):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def run(self, group):
        return CommonSprite(group, self.get_scaled_image('sprites/player.png', 2), self.x, self.y)


class MapTilesFactory(SpriteFactory):
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
                image = self.get_scaled_image('sprites/{}.jpg'.format(self.tile_mapping[tile_symbol]), 2)
                sprite = self.create(image, x, y)
                row.append(sprite)
            tiles.append(row)
        return tiles


class GameController:
    def __init__(self):
        self.screen_man = ScreenManager()
        self.net_man = NetworkManager()
        self.screen_man = ScreenManager()
        self.player = Player()
        self.action_man = ActionManager(self)


class ScreenManager:
    def __init__(self):
        self.window = pygame.display.set_mode((31 * TILE_SIDE_PX, 18 * TILE_SIDE_PX))
        self.sprite_group = pygame.sprite.Group()
        self.focus_group = pygame.sprite.GroupSingle()

        pygame.display.set_caption('Client')

        ui = UIFactory().run(self.sprite_group, self.focus_group)

        map_frame = ui['map_frame']

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

        self.tiles = MapTilesFactory(self.map_scheme, map_frame, self.sprite_group).run()
        self.focus_image = ui['focus_image']

    def get_tiles_as_list(self):
        tiles = []
        for row in self.tiles:
            tiles += [tile for tile in row]
        return tiles

    def redraw(self):
        self.sprite_group.update()
        self.sprite_group.draw(self.window)
        self.focus_group.draw(self.window)


class CommonSprite(pygame.sprite.Sprite):
    def __init__(self, group, image, x, y):
        super().__init__(group)
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.focus_on = False


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
