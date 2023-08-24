from utils.components import Button, Font, Image, Text

# components
bg = Image("assets/images/origami_bg.jpeg", 100, 100)
title = Text("Modalità", size=50, font=Font.semibold)
btn_base = Button("base_game", 80, sound="interface")
btn_custom = Button("custom_game", 80, sound="interface")
btn_back = Button("back", 10)


def run(screen, **kwargs):
    bg.draw(screen)
    title.draw(screen, 50, 5)
    btn_base.draw(screen, 50, 30)
    btn_custom.draw(screen, 50, 50)
    btn_back.draw(screen, 15, 90)


def manage_event(event, game, game_settings, **kwargs):
    if btn_base.handle_event(event):
        game.reset()
        game_settings.reset()
        return "game"
    if btn_custom.handle_event(event):
        return "custom-game"
    if btn_back.handle_event(event):
        return "menu"


def resize(_):
    bg.resize(100, 100)
    btn_base.resize()
    btn_custom.resize()
    btn_back.resize()
