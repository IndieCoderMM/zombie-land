import pygame
from settings import TILEWIDTH
from utils import *

class Level:
    def __init__(self, level_data):
        self.data = level_data
        self.tilesheet = self.data['sheet']
        self.walls_data = import_csv_layout(self.data['wall'])
        self.ground_data = import_csv_layout(self.data['ground'])
        self.ground_sprites = self.get_sprite_group(self.ground_data)
        self.wall_sprites = self.get_sprite_group(self.walls_data)
        # self.decor_data = import_csv_layout(self.data['decor'])
        # self.decor_sprites = self.get_sprite_group(self.decor_data)

    def get_sprite_group(self, data):
        tile_list = import_cut_graphic(self.tilesheet, TILEWIDTH)
        sprite_group = pygame.sprite.Group()
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                if val == '-1':
                    continue
                x = j * TILEWIDTH
                y = i * TILEWIDTH
                wall_surface = tile_list[int(val)]
                sprite = StaticTile(x, y, TILEWIDTH, wall_surface)
                sprite_group.add(sprite)
        return sprite_group

    def draw(self, screen):
        self.ground_sprites.draw(screen)
        self.wall_sprites.draw(screen)
        # self.decor_sprites.draw(screen)

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

class StaticTile(Tile):
    def __init__(self, x, y, size, surface):
        super().__init__(x, y, size)
        self.image = surface
