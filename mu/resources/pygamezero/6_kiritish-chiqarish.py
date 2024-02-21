from pgzhelper import *

WIDTH = 960
HEIGHT = 540

xazina = Actor("xazina_sandig'i", (WIDTH / 2, HEIGHT / 2))
input_box = Rect(350, 400, 200, 50)
user_text = ''
input_done = False

parol = '1234'

def draw():
    screen.blit("cho'l", (0, 0))
    xazina.draw()
    xazina.say("Parolingizni kiriting!", (500, 50))
    screen.draw.filled_rect(input_box,'pink')
    ptext.drawbox(user_text, input_box)

    if input_done:
        if user_text == parol:
            xazina.say("Xazinaga ega bo'ldingiz!", (500, 50), background='white', color='black')
            sounds.olqish.play()
            game.exit()
        else:
            xazina.say("Oishga muvaffaqiyatsizlik!", (500, 50), background='white', color='black')
            sounds.xavf_ogohlantirish.play()
            game.exit()

def on_key_down(key, unicode):
    global user_text, input_done

    if key == keys.RETURN:
        input_done = True
    elif key == keys.BACKSPACE:
        user_text = user_text[:-1]
    else:
        user_text += unicode

