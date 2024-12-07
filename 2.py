# Add a title text

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

    ###############################################################################
    font_title = pg.font.Font(None, 64)
    text = font_title.render("Pummel The Chimp, And Win $$$", True, (10, 10, 10))
    textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
    background.blit(text, textpos)
    ##############################################################################

    clock = pg.time.Clock()

    going = True
    while going:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False

        screen.blit(background, (0, 0))
        pg.display.flip()
    
    pg.quit()

main()
