from utils.components import Button, Image

# components
bg = Image("assets/images/origami.jpeg", 100, 100)
btn_new_game = Button("play", 70)
btn_rules = Button("rules", 10)


def run(screen, **kwargs):
    bg.draw(screen)
    btn_new_game.draw(screen, 50, 50)
    btn_rules.draw(screen, 50, 90)


def manage_event(event, **kwargs):
    if btn_new_game.handle_event(event):
        return "new-game"
    if btn_rules.handle_event(event):
        return  # TODO: state missing


def resize(_):
    bg.resize(100, 100)
    btn_new_game.resize()
    btn_rules.resize()