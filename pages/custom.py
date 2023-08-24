from static.settings import Colors, Duration, Skip, Winner
from utils.components import Button, ButtonGroup, Font, Image, Rectangle, Text

# components
bg = Image("assets/images/origami_bg.jpeg", 100, 100)
title = Text("Personalizzazione", 50, font=Font.semibold)
text_duration = Text("Durata", color=Colors.BLACK)
text_skip = Text("Skip")
text_winner = Text("Punti vittoria")
duration_btns = [(f"duration_{duration}", duration) for duration in Duration.options]
skip_btns = [(f"skip_{skip}", skip) for skip in Skip.options]
points_btns = [(f"points_{points}", points) for points in Winner.options]
group_durations = ButtonGroup(duration_btns, 30, index=2)
group_skip = ButtonGroup(skip_btns, 50, index=2)
group_winner = ButtonGroup(points_btns, 70)
btn_next = Button("confirm", 65)
btn_back = Button("back", 10)
shape_square = Rectangle(90, 20, trasparent=True)


def run(screen, **kwargs):
    bg.draw(screen)
    shape_square.draw(screen, 50, 27)
    shape_square.draw(screen, 50, 47)
    shape_square.draw(screen, 50, 67)
    text_duration.draw(screen, 50, 20)
    text_skip.draw(screen, 50, 40)
    text_winner.draw(screen, 50, 60)
    title.draw(screen, 50, 5)
    group_durations.draw(screen)
    group_skip.draw(screen)
    group_winner.draw(screen)
    btn_next.draw(screen, 60, 90)
    btn_back.draw(screen, 15, 90)


def manage_event(event, game, game_settings, **kwargs):
    if duration := group_durations.handle_event(event):
        duration_s = Duration.options.get(duration)
        game_settings.duration = duration_s
        game.remaining_time = duration_s
    if skip := group_skip.handle_event(event):
        skip_n = Skip.options.get(skip)
        game_settings.skips = skip_n
        game.skip_red = skip_n
        game.skip_blue = skip_n
    if winner := group_winner.handle_event(event):
        game_settings.points_to_win = Winner.options.get(winner)
    if btn_next.handle_event(event):
        group_durations.reset()
        group_skip.reset()
        group_winner.reset()
        return "select-decks"
    if btn_back.handle_event(event):
        group_durations.reset()
        group_skip.reset()
        group_winner.reset()
        return "new-game"


def resize(screen):
    bg.resize(100, 100)
    group_durations.resize(screen)
    group_skip.resize(screen)
    group_winner.resize(screen)
    btn_next.resize()
    btn_back.resize()
    shape_square.resize()
