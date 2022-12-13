from zombieland.utils import *
from zombieland.settings import *

class HealthKit(pg.sprite.Sprite):
    TIMER = 5000

    def __init__(self, x, y):
        super().__init__()
        self.image = load_image('./resources/assets/health_kit.png', TILEWIDTH)
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.spawn_clk = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_clk > self.TIMER:
            self.kill()

class ItemSpawner(pg.sprite.Group):
    def spawn_health_kit(self, x, y):
        health_kit = HealthKit(x, y)
        self.add(health_kit)
