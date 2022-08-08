
from settings import *
from utils import *
import pygame as pg
import math

class Player:
    MAX_HEALTH = 100

    def __init__(self, game, character):
        self.game = game
        self.SHOOT_IMG = load_image(CHAR_PATH + character + '_shoot.png', TILEWIDTH)
        self.RELOAD_IMG = load_image(CHAR_PATH + character + '_reload.png', TILEWIDTH)

        self.bullet_group = pg.sprite.Group()
        self.x, self.y = 10, 7
        self.angle = 0
        self.reloading = False
        self.last_fire_clk = 0
        self.reload_clk = 0
        self.ammo = ROUNDS
        self.health = self.MAX_HEALTH
        self.prev_health = self.MAX_HEALTH

    @property
    def pos(self):
        return int(self.x), int(self.y)

    @property
    def rect(self):
        return pg.Rect(self.x*TILEWIDTH, self.y*TILEWIDTH, P1_SIZE, P1_SIZE)

    def movement(self):
        speed = P1_SPD * self.game.delta_time
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a
        dx, dy = 0, 0

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin

        if self.is_walkable(self.x + dx, self.y):
            self.x += dx
        if self.is_walkable(self.x, self.y + dy):
            self.y += dy

    def fire(self):
        now = pg.time.get_ticks()
        if now - self.last_fire_clk < FIRE_RATE:
            return
        self.last_fire_clk = now
        if self.reloading:
            self.game.sfx.noammo.play()
            return
        self.game.sfx.machine_gun.play()
        bullet = Bullet(self.x + 0.5, self.y + 0.5, self.angle)
        self.bullet_group.add(bullet)
        self.ammo -= 1

    def is_walkable(self, x, y):
        player_rect = pg.Rect(x * TILEWIDTH, y * TILEWIDTH, P1_SIZE, P1_SIZE)
        for wx, wy in self.game.map.wall_coors:
            if pg.Rect(wx*TILEWIDTH, wy*TILEWIDTH, TILEWIDTH, TILEWIDTH).colliderect(player_rect):
                return False
        return True

    def draw(self):
        self.bullet_group.draw(self.game.screen)
        image = self.RELOAD_IMG if self.reloading else self.SHOOT_IMG
        self.game.screen.blit(rotate_image(image, -math.degrees(self.angle)),
                              (self.x * TILEWIDTH, self.y * TILEWIDTH))
        bar_width = 50
        health_color = 'red' if self.health < self.MAX_HEALTH/3 else 'green'
        pg.draw.rect(self.game.screen, 'grey', ((self.x-0.3) * TILEWIDTH, (self.y-0.5) * TILEWIDTH, bar_width, 10))
        pg.draw.rect(self.game.screen, health_color, ((self.x-0.3)*TILEWIDTH, (self.y-0.5)*TILEWIDTH, bar_width*(self.health/self.MAX_HEALTH), 10))
        self.game.ui.write('.'*self.ammo, 'orange', 22, (self.x+0.5)*TILEWIDTH, (self.y-0.2)*TILEWIDTH)

    def get_direction(self):
        mx, my = pg.mouse.get_pos()[0] / TILEWIDTH, pg.mouse.get_pos()[1] / TILEWIDTH
        dx, dy = mx - self.x, my - self.y
        angle = math.atan2(dy, dx)
        self.angle = angle
        self.angle %= math.tau

    def update(self):
        self.get_direction()
        self.movement()
        self.bullet_group.update()

        if self.ammo <= 0 and not self.reloading:
            self.reloading = True
            self.game.sfx.reload.play()
            self.reload_clk = pg.time.get_ticks()
        if self.reloading:
            now = pg.time.get_ticks()
            if now - self.reload_clk > RELOAD_TIME:
                self.ammo = ROUNDS
                self.reloading = False
                self.game.sfx.reload.play()

        if pg.key.get_pressed()[pg.K_SPACE]:
            self.fire()
        if pg.key.get_pressed()[pg.K_r] and not self.reloading and self.ammo < ROUNDS:
            self.reloading = True
            self.reload_clk = pg.time.get_ticks()
            self.game.sfx.reload.play()

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = load_image('assets/bullet.png', 14)
        self.image = pg.transform.rotate(self.image, -math.degrees(angle))
        self.origin = x * TILEWIDTH, y * TILEWIDTH
        self.rect = self.image.get_rect(topleft=self.origin)
        self.dx = BULLET_SPD * math.cos(angle)
        self.dy = BULLET_SPD * math.sin(angle)

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if abs(self.rect.x - self.origin[0]) > 250 or abs(self.rect.y - self.origin[1]) > 250:
            self.kill()




