
from zombieland.player import Player
from zombieland.enemy import ZombieHorde
from zombieland.map import Map
from zombieland.item_spawner import ItemSpawner
from zombieland.sfx import SFX
from zombieland.ui import UI
from zombieland.settings import RES, FPS, LEVEL1, CHARACTERS

import random
import pygame as pg


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        pg.display.set_caption('Zombieland')

        self.delta_time = None
        self.player = None
        self.zombie_horde = None
        self.start_clk = 0
        self.score = 0
        self.survial_score = 0
        self.is_gameover = False
        self.is_running = False
        self.music_on = True
        self.sfx_on = True
        self.difficulty = 'newbie'
        self.selected_char = CHARACTERS[-1]

        self.map = Map(self)
        self.ui = UI(self)
        self.sfx = SFX()
        self.item_spawner = ItemSpawner()

    def start_new_game(self):
        self.map.load_level(LEVEL1)
        self.player = Player(self, self.selected_char)
        self.zombie_horde = ZombieHorde(self, 10)
        self.score = 0
        self.survial_score = 0
        self.start_clk = pg.time.get_ticks()
        self.is_gameover = False
        self.is_running = True

    def check_collisions(self):
        for item in self.item_spawner:
            if item.rect.colliderect(self.player.rect):
                self.sfx.coin.play()
                self.player.health += 10
                if self.player.health >= self.player.MAX_HEALTH:
                    self.player.health = self.player.MAX_HEALTH
                item.kill()

        for zombie in self.zombie_horde.group:
            if pg.sprite.spritecollide(zombie, self.player.bullet_group, True):
                if random.randrange(3) == 0:
                    self.sfx.impact.play()
                    continue
                zombie.kill()
                self.sfx.hit.play()
                self.score += 1

                luck = random.randrange(3)
                if luck == 1:
                    self.item_spawner.spawn_health_kit(zombie.rect.x, zombie.rect.y)

            if zombie.rect.colliderect(self.player.rect):
                self.player.health -= 0.5
                if self.player.prev_health - self.player.health > 10:
                    self.player.prev_health = self.player.health
                    self.sfx.damage.play()
                if self.player.health <= 0:
                    self.sfx.gameover.play()
                    self.is_gameover = True

        for wall in self.map.level.wall_sprites:
            if pg.sprite.spritecollide(wall, self.player.bullet_group, True):
                self.sfx.impact.play()

    def update(self):
        pg.display.update()
        self.ui.update()
        if self.is_gameover or not self.is_running:
            return
        self.delta_time = self.clock.tick(FPS)
        self.survial_score = round((pg.time.get_ticks()-self.start_clk)/1000, 1)
        self.zombie_horde.update()
        self.player.update()
        self.item_spawner.update()
        self.check_collisions()

    def draw(self):
        if not self.is_running or self.is_gameover:
            self.ui.draw()
            return
        self.map.draw()
        self.player.draw()
        self.item_spawner.draw(self.screen)
        self.zombie_horde.draw()
        self.ui.draw()

    def run(self):
        run = True
        while run:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    run = False
                if e.type == pg.MOUSEBUTTONUP:
                    self.ui.get_click(e.pos[0], e.pos[1])
            self.draw()
            self.update()
        pg.quit()