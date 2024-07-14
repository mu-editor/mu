from pgzhelper import *

WIDTH = 960
HEIGHT = 540

treasure = Actor("treasure_box", (WIDTH / 2, HEIGHT / 2))

input_text = ""
input_done = False
input_rect = Rect(350, 400, 200, 50)

guide_rect = Rect(300, 100, 400, 50)
password = "1234"

def draw():
    screen.blit("desert", (0, 0))
    treasure.draw()
    screen.draw.textbox("Please input a password.", guide_rect)
    screen.draw.filled_rect(input_rect, "pink")
    screen.draw.textbox(input_text, input_rect)

    if input_done:
        screen.blit("desert", (0, 0))
        treasure.draw()

        if input_text == password:    
            screen.draw.textbox("You got it!", guide_rect)
            sounds.cheer.play()
        else:
            screen.draw.textbox("You failed!", guide_rect)
            sounds.warning.play()

        pygame.display.update()
        game.exit()

def on_key_down(key, unicode):
    global input_text, input_done

    if key == keys.RETURN:
        input_done = True
    elif key == keys.BACKSPACE:
        input_text = input_text[:-1]
    else:
        input_text += unicode
