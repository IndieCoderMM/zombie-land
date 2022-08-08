MAP_COL = 30
MAP_ROW = 20
TILEWIDTH = 32

WIDTH = MAP_COL * TILEWIDTH
HEIGHT = MAP_ROW * TILEWIDTH

RES = (WIDTH, HEIGHT)
FPS = 60

P1_SIZE = TILEWIDTH
P1_ROTATION = 0.001
P1_SPD = 0.004

FIRE_RATE = 200
RELOAD_TIME = 3000
ROUNDS = 10

BULLET_SPD = 10
FONT_PATH = 'fonts/Kartooni.ttf'

CHAR_PATH = 'assets/char/'
# CHARACTERS = {
#     'survivor': ['survivor_shoot.png', 'survivor_reload.png'],
#     'hitman': ['hitman_shoot.png', 'hitman_reload.png'],
#     'soldier': ['soldier_shoot.png', 'soldier_reload.png'],
#     'zombie': ['zombie_shoot.png', 'zombie_reload.png'],
#     'robot': ['robot_shoot.png', 'robot']
# }
CHARACTERS = ['hitman', 'soldier', 'zombie', 'robot', 'survivor']

LEVEL0 = {
    'sheet': 'levels/level0/td-map.png',
    'ground': 'levels/level0/tds_grass_layer.csv',
    'wall': 'levels/level0/tds_wall_layer.csv'
}

LEVEL1 = {
    'sheet': 'levels/level1/tdshooter_tilesheet.png',
    'ground': 'levels/level1/td_shooter_map_Ground.csv',
    'decor': 'levels/level1/td_shooter_map_Decors.csv',
    'wall': 'levels/level1/td_shooter_map_Wall.csv'
}