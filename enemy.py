import random
from settings import MAP_COL, MAP_ROW, TILEWIDTH
from utils import load_image, rotate_image
from pathfinder import PathFinder
import pygame as pg
import math

class ZombieHorde:
    SPAWN_LOCATIONS = ['TOP', 'RIGHT', 'BOTTOM', 'LEFT']

    def __init__(self, game, max_count):
        self.game = game
        self.pathfinder = PathFinder(game.map.wall_layout, game.map.wall_coors)
        self.group = pg.sprite.Group()
        self.timer = 3000
        self.max_count = max_count
        self.spawn_clk = 0
        self.spawn()

    def spawn(self):
        now = pg.time.get_ticks()
        if now - self.spawn_clk < self.timer or len(self.group) > self.max_count:
            return
        self.spawn_clk = now
        side = random.choice(self.SPAWN_LOCATIONS)
        x, y = 2, 2     # Initial Spawn Points
        if side == 'TOP':
            x = random.randrange(2, MAP_COL-1)
        elif side == 'RIGHT':
            x = MAP_COL - 2
            y = random.randrange(2, MAP_ROW-1)
        elif side == 'LEFT':
            y = random.randrange(2, MAP_ROW-1)
        elif side == 'BOTTOM':
            x = random.randrange(2, MAP_COL-1)
            y = MAP_ROW - 2
        z = Zombie(x, y, self.game, self.pathfinder)
        self.group.add(z)

    def draw(self):
        self.group.draw(self.game.screen)

    def update(self):
        self.group.update()
        self.spawn()

class Zombie(pg.sprite.Sprite):
    def __init__(self, x, y, game, pathfinder):
        super().__init__()
        self.IMG = load_image('assets/zombie.png', TILEWIDTH)
        self.image = self.IMG
        self.rect = self.image.get_rect()
        self.rect.topleft = x * TILEWIDTH, y * TILEWIDTH
        self.game = game
        self.pathfinder = pathfinder
        self.speed = random.randint(5, 8) * 0.01
        self.last_move_clk = 0

    @property
    def pos(self):
        x_pix, y_pix = self.rect.topleft
        return x_pix / TILEWIDTH, y_pix / TILEWIDTH

    def move(self):
        dest = self.pathfinder.get_path((int(self.pos[0]), int(self.pos[1])), self.game.player.pos)
        next_x, next_y = dest[-1]
        angle = math.atan2(next_y+0.5-self.pos[1], next_x+0.5-self.pos[0])
        self.image = rotate_image(self.IMG, -math.degrees(angle))
        dx = math.cos(angle) * self.speed
        dy = math.sin(angle) * self.speed

        self.rect.x += dx * TILEWIDTH
        self.rect.y += dy * TILEWIDTH

    def update(self):
        self.move()

