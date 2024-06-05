import pygame
from map_objects import Map
from progress_bar import ProgresBar
from player import Player
import constants


pygame.init()
window = pygame.display.set_mode(
    (constants.WINDOW_HEIGHT, constants.WINDOW_HEIGHT)
)
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 10)


map = Map()
player = Player()
map_generator = map.generate_map()
pbar = ProgresBar((50, 500), (600, 50))

game_surface = pygame.Surface(map.map_img.get_size())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and map.is_loaded:
            if event.button == pygame.BUTTON_LEFT:
                map_col = round((-map.offset_px.x + event.pos[0])//32 + map.offset_tiles.x)
                map_row = round((-map.offset_px.y + event.pos[1])//32 + map.offset_tiles.y)
                player.set_target(pygame.Vector2(map_col, map_row), map.map)

    pressed = pygame.key.get_pressed()
    map.handle_pressed(pressed)
    window.fill((0, 0, 0))

    if not map.is_loaded:
        try:
            done, total = next(map_generator)
            pbar.update(done, total, "Map Generation...")
            pbar.draw(window)
            # print(done, "/", total)
        except StopIteration:
            map.is_loaded = True
            map.draw_map()
    else: 
        game_surface.blit(map.map_img, (0, 0))
        player.update_position()
        player.draw(game_surface, map.offset_tiles)
        window.blit(game_surface, map.offset_px)
        minimap = map.get_minimap()
        window.blit(minimap, (0, 0))

    pygame.display.update()
    clock.tick(60)
