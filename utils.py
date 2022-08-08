import pygame as pg
from csv import reader

def rotate_image(img: pg.Surface, angle):
    return pg.transform.rotate(img, angle)

def load_image(path: str, width=None, height=None):
    image = pg.image.load(path).convert_alpha()
    if width is None:
        return image
    if height is None:
        height = width
    return pg.transform.scale(image, (width, height))

def import_csv_layout(path):
    wall_map = []
    with open(path) as layout:
        level = reader(layout, delimiter=',')
        for row in level:
            wall_map.append(list(row))
        return wall_map

def import_cut_graphic(path, size):
    surface = load_image(path)
    tile_rows = surface.get_height() // size
    tile_cols = surface.get_width() // size
    cut_tiles = []
    for row in range(tile_rows):
        for col in range(tile_cols):
            x = col * size
            y = row * size
            new_surf = pg.Surface((size, size), pg.SRCALPHA)
            new_surf.blit(surface, (0, 0), (x, y, size, size))
            cut_tiles.append(new_surf)
    return cut_tiles

