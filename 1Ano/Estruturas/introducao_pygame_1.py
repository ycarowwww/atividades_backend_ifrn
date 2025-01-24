import pygame as pg

pg.init()

BASE_RSLT = (800, 600)
screen = pg.display.set_mode(BASE_RSLT)
pg.display.set_caption("Pygame game")
clock = pg.time.Clock()
FPS = 60.0

rect = pg.Rect((100, 100), (100, 100))
rect_pos = [100, 100]
rect_vel = pg.Vector2(5, 5)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.fill((0, 0, 0))
    clock.tick(FPS)

    rect_pos += rect_vel

    if rect_pos[0] + rect.width >= screen.get_width() or rect_pos[0] <= 0:
        rect_vel[0] *= -1
    if rect_pos[1] <= 0 or rect_pos[1] + rect.height >= screen.get_height():
        rect_vel[1] *= -1
    
    rect.topleft = rect_pos

    pg.draw.rect(screen, (255, 255, 255), rect)

    pg.display.flip()

pg.quit()