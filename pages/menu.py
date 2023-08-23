from static.settings import Colors
from utils.components import Button, Image, Text

# components
bg = Image("assets/images/origami.jpeg", 100, 100)
title = Image("assets/images/title.png").resize(80, aspect_ratio=True)
caption = Text("Pronti a parlare senza dire troppo?", 35, color=Colors().TRASPARENT)
btn_new_game = Button("play", 50)
btn_rules = Button("rules", 10)


def run(screen, **kwargs):
    bg.draw(screen)
    title.draw(screen, 50, 11, relative=True)
    caption.draw_multi(screen, 70, 28, 40)
    btn_new_game.draw(screen, 45, 94)
    btn_rules.draw(screen, 83, 94)


def manage_event(event, **kwargs):
    if btn_new_game.handle_event(event):
        return "new-game"
    if btn_rules.handle_event(event):
        return "rules"


def resize(_):
    bg.resize(100, 100)
    btn_new_game.resize()
    btn_rules.resize()
