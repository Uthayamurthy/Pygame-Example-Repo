# Make fist move with mouse movements

import os
import pygame as pg

def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)
    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()

def create_fist():
    image, rect = load_image("fist.png", -1)
    return {"image": image, "rect": rect, "offset": (-235, -80), "punching": False}

def create_chimp():
    image, rect = load_image("chimp.png", -1, 4)
    rect.y += 100
    return {"image": image, "rect": rect, "move": 18, "dizzy": False, "original": image}

def walk_chimp(chimp, screen_rect):
    newpos = chimp["rect"].move((chimp["move"], 0))
    if not screen_rect.contains(newpos):
        if chimp["rect"].left < screen_rect.left or chimp["rect"].right > screen_rect.right:
            chimp["move"] = -chimp["move"]
            newpos = chimp["rect"].move((chimp["move"], 0))
            chimp["image"] = pg.transform.flip(chimp["image"], True, False)
    chimp["rect"] = newpos

#######################################
def update_fist(fist):
    pos = pg.mouse.get_pos()
    fist["rect"].topleft = pos
    fist["rect"].move_ip(fist["offset"])
    if fist["punching"]:
        fist["rect"].move_ip(15, 25)
########################################

def update_chimp(chimp, screen_rect):
    walk_chimp(chimp, screen_rect)

def main():
    # Initialize Pygame
    pg.init()

    global data_dir
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    data_dir = os.path.join(main_dir, "data")

    screen = pg.display.set_mode((1280, 480), pg.SCALED)
    pg.display.set_caption("Monkey Fever")
    ############################
    pg.mouse.set_visible(False)
    ###########################

    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((170, 238, 187)) # (R,, G, B) colors

    font_title = pg.font.Font(None, 64)
    text = font_title.render("Pummel The Chimp, And Win $$$", True, (10, 10, 10))
    textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
    background.blit(text, textpos)

    fist = create_fist()
    chimp = create_chimp()

    clock = pg.time.Clock()

    going = True
    while going:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False

        #################################
        update_fist(fist)
        #################################
        update_chimp(chimp, screen.get_rect())

        screen.blit(background, (0, 0))
        screen.blit(fist["image"], fist["rect"])
        screen.blit(chimp["image"], chimp["rect"])
        pg.display.flip()


    pg.quit()

main()
