# A black rectangle to play with ...

import pygame as pg

def main():
    # Initialize Pygame
    pg.init()

    screen = pg.display.set_mode((1280, 480), pg.SCALED)
    pg.display.set_caption("Monkey Fever")
    # pg.mouse.set_visible(False)

    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((170, 238, 187)) # (R,, G, B) colors

    clock = pg.time.Clock()

    going = True
    while going:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
        #####################################
        rect = pg.draw.rect(background, (0, 0, 0), (0, 0, 50, 50))
        #####################################
        screen.blit(background, (0, 0))
        pg.display.flip()
    
    pg.quit()

main()
