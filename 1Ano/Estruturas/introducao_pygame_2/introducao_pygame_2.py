import pygame as pg
from os import path

def get_file_path(file: str) -> str:
    base_dir: str = path.dirname(path.abspath(__file__))

    return path.join(base_dir, file)

pg.init()

BASE_RSLT = (800, 600)
screen = pg.display.set_mode(BASE_RSLT)
pg.display.set_caption("Pygame game")
clock = pg.time.Clock()
FPS = 60.0

cherry = pg.transform.scale(pg.image.load(get_file_path("images/cereja.png")).convert_alpha(), (50, 50))
ghost = pg.transform.scale(pg.image.load(get_file_path("images/fantasma.png")).convert_alpha(), (50, 50))
pacmans = [
    pg.transform.scale(pg.image.load(get_file_path("images/pacman.png")).convert_alpha(), (50, 50)),
    pg.transform.scale(pg.image.load(get_file_path("images/pacman2.png")).convert_alpha(), (50, 50))
]

cherry_1_pos = [300, 400]
ghost_1_pos = [300, 200]
pacman_1_pos = [0, 0]
pac_sprite = 0
pac_sprite_img = pacmans[pac_sprite]
sized, rotated = False, False

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.fill((0, 0, 0))
    clock.tick(FPS)

    pac_sprite += 0.1
    pac_sprite %= 2

    pac_sprite_img = pacmans[int(pac_sprite)]

    keys = pg.key.get_pressed()

    if keys[pg.K_w]:
        pacman_1_pos[1] -= 5
    if keys[pg.K_s]:
        pacman_1_pos[1] += 5
    if keys[pg.K_a]:
        pacman_1_pos[0] -= 5
        rotated = True
    if keys[pg.K_d]:
        pacman_1_pos[0] += 5
        rotated = False

    if sized:
        pac_sprite_img = pg.transform.scale(pac_sprite_img, [i//2 for i in pac_sprite_img.size])
    if rotated:
        pac_sprite_img = pg.transform.flip(pac_sprite_img, True, False)

    ghost_1_pos[0] += 5

    if ghost_1_pos[0] >= screen.get_width():
        ghost_1_pos[0] = -ghost.width

    screen.blit(cherry, cherry_1_pos)
    screen.blit(ghost, ghost_1_pos)
    screen.blit(pac_sprite_img, pacman_1_pos)

    if pg.Rect(pacman_1_pos, pacmans[0].size).colliderect(cherry.get_rect(topleft=cherry_1_pos)):
        sized = False
    if pg.Rect(pacman_1_pos, pacmans[0].size).colliderect(ghost.get_rect(topleft=ghost_1_pos)):
        sized = True

    pg.display.flip()

pg.quit()