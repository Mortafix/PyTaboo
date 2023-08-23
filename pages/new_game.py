from utils.components import Button, Font, Image, Text

# components
bg = Image("assets/images/origami_bg.jpeg", 100, 100)
title = Text("Modalità", 50, 5, size=50, font=Font.semibold)
btn_base = Button("base_game", 50, 30, 80)
btn_custom = Button("custom_game", 50, 50, 80)
btn_back = Button("back", 15, 90, 10)


def run(screen, **kwargs):
    bg.draw(screen)
    title.draw(screen)
    btn_base.draw(screen)
    btn_custom.draw(screen)
    btn_back.draw(screen)


def manage_event(event, game, game_settings, **kwargs):
    if btn_base.handle_event(event):
        game_settings.duration = 120
        game.remaining_time = 120
        game_settings.skips = 5
        game.skip_red = 5
        game.skip_blue = 5
        game_settings.points_to_win = 10
        return "game"
    if btn_custom.handle_event(event):
        return "custom-game"
    if btn_back.handle_event(event):
        return "menu"
