from utils.components import Button, Image

# components
bg = Image("assets/images/origami.png", 100, 100)
btn_new_game = Button("play", 50, 50, 70)
btn_rules = Button("rules", 50, 90, 10)


def run(screen, **kwargs):
    bg.draw(screen)
    btn_new_game.draw(screen)
    btn_rules.draw(screen)


def manage_event(event, **kwargs):
    if btn_new_game.handle_event(event):
        return "new-game"
    if btn_rules.handle_event(event):
        return  # TODO: state missing
