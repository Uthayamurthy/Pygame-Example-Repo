# Add a title window

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

def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(data_dir, name)
    return pg.mixer.Sound(fullname)

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

def spin_chimp(chimp):
    center = chimp["rect"].center
    chimp["dizzy"] += 12
    if chimp["dizzy"] >= 360:
        chimp["dizzy"] = False
        chimp["image"] = chimp["original"]
    else:
        chimp["image"] = pg.transform.rotate(chimp["original"], chimp["dizzy"])
    chimp["rect"] = chimp["image"].get_rect(center=center)

def update_fist(fist):
    pos = pg.mouse.get_pos()
    fist["rect"].topleft = pos
    fist["rect"].move_ip(fist["offset"])
    if fist["punching"]:
        fist["rect"].move_ip(15, 25)

def update_chimp(chimp, screen_rect):
    if chimp["dizzy"]:
        spin_chimp(chimp)
    else:
        walk_chimp(chimp, screen_rect)
        
def punch_fist(fist, chimp):
    if not fist["punching"]:
        fist["punching"] = True
        hitbox = fist["rect"].inflate(-5, -5)
        return hitbox.colliderect(chimp["rect"])
    return False

def punch_chimp(chimp):
    if not chimp["dizzy"]:
        chimp["dizzy"] = True

def unpunch_fist(fist):
    fist["punching"] = False

def update_score_display(screen, font, score):
    score_text = font.render(f"Score: ${score}", True, (0, 0, 0))
    screen.blit(score_text, (screen.get_width() - 150, 10))

#############################################
def title_screen(screen):
    screen.fill((170, 238, 187))

    font_title = pg.font.Font(None, 64)
    title_text = font_title.render("Pummel The Chimp!", True, (10, 10, 10))
    title_rect = title_text.get_rect(center=(screen.get_width() / 2, 150))
    screen.blit(title_text, title_rect)

    font_instruction = pg.font.Font(None, 36)
    start_text = font_instruction.render("Press Enter to Start", True, (0, 0, 0))
    start_rect = start_text.get_rect(center=(screen.get_width() / 2, 250))
    screen.blit(start_text, start_rect)

    instruction_text = font_instruction.render("Hit Chimp to earn $ and press Spacebar to restart", True, (0, 0, 0))
    instruction_rect = instruction_text.get_rect(center=(screen.get_width() / 2, 300))
    screen.blit(instruction_text, instruction_rect)

    pg.display.flip()
#############################################


def main():
    # Initialize Pygame
    pg.init()

    global data_dir
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    data_dir = os.path.join(main_dir, "data")

    screen = pg.display.set_mode((1280, 480), pg.SCALED)
    pg.display.set_caption("Monkey Fever")
    pg.mouse.set_visible(False)

    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((170, 238, 187)) # (R,, G, B) colors

    font_title = pg.font.Font(None, 64)
    text = font_title.render("Pummel The Chimp, And Win $$$", True, (10, 10, 10))
    textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
    background.blit(text, textpos)

    whiff_sound = load_sound("whiff.wav")
    punch_sound = load_sound("punch.wav")

    fist = create_fist()
    chimp = create_chimp()

    font = pg.font.Font(None, 36)
    score = 0

    clock = pg.time.Clock()

    ########################################################################
    going = False

    # Show title screen
    title_shown = True
    while title_shown:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                title_shown = False

        title_screen(screen)
    ############################################################################

    going = True
    while going:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    score = 0
            elif event.type == pg.MOUSEBUTTONDOWN:
                if punch_fist(fist, chimp):
                    punch_chimp(chimp)
                    punch_sound.play()
                    score += 10
                else:
                    whiff_sound.play()
            elif event.type == pg.MOUSEBUTTONUP:
                unpunch_fist(fist)
    
        update_fist(fist)
        update_chimp(chimp, screen.get_rect())

        screen.blit(background, (0, 0))
        screen.blit(fist["image"], fist["rect"])
        screen.blit(chimp["image"], chimp["rect"])

        update_score_display(screen, font, score)
        
        pg.display.flip()


    pg.quit()

main()
