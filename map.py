from level import Level

class Map:
    def __init__(self, game):
        self.game = game
        self.level: Level = None
        self.wall_layout: list[str] = None
        self.wall_coors: list[tuple[int, int]] = None

    def define_walls(self) -> list[tuple[int, int]]:
        walls = []
        for y, row in enumerate(self.wall_layout):
            for x, val in enumerate(row):
                if val != '-1':
                    walls.append((x, y))
        return walls

    def load_level(self, level):
        self.level = Level(level)
        self.wall_layout = self.level.walls_data
        self.wall_coors = self.define_walls()

    def draw(self):
        self.level.draw(self.game.screen)
        # for (x, y) in self.walls:
        #     pg.draw.rect(self.game.screen, 'red', (x*TILEWIDTH, y*TILEWIDTH, TILEWIDTH, TILEWIDTH), 1)


# TODO: Tiles transparency
