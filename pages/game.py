from random import choice

from static.settings import Colors, Screen
from utils.components import Button, Font, Image, LoadingBar, Rectangle, Text

# components
loading_timer = LoadingBar(70)
scoreboard = Rectangle(95, 17)
card_word = Rectangle(80, 60, trasparent=True)
winner_tab = Rectangle(95, 70)
btn_skip = Button("word_skip", 30)
btn_skip_end = Button("word_skip_end", 30)
btn_error = Button("word_wrong", 30)
btn_correct = Button("word_correct", 30)
btn_start = Button("go", 30)
btn_pause = Button("pause", 8)
btn_resume = Button("resume", 65)
btn_quit = Button("quit", 45)
btn_menu = Button("menu", 45)


def run(screen, game, game_settings, **kwargs):
    screen.fill(Colors.RED if game.first_team else Colors.BLUE)

    # winner
    if not game.turn_start and (winner := winning_condition(game, game_settings)):
        winner_text = "ROSSA" if winner == "t-red" else "BLU"
        winner_color = Colors.RED if winner == "t-red" else Colors.BLUE
        screen.fill(winner_color)
        winner_tab.draw(screen, 50, 40)
        Text("Vittoria!!", color=winner_color).draw(screen, 50, 15)
        Text(f"Squadra {winner_text}", color=winner_color).draw(screen, 50, 20)
        Text("Punti", 30).draw(screen, 50, 37)
        Text(game.score_red, 38, Colors.RED, Font.semibold).draw(screen, 25, 37)
        Text(game.score_blue, 38, Colors.BLUE, Font.semibold).draw(screen, 75, 37)
        Text("Skip", size=30).draw(screen, 50, 47)
        offset_skip = 2 if game_settings.skips < 0 else 0
        skip_used_red = game_settings.skips - game.skip_red - offset_skip
        skip_used_blue = game_settings.skips - game.skip_blue - offset_skip
        Text(skip_used_red, 38, Colors.RED, Font.semibold).draw(screen, 25, 47)
        Text(skip_used_blue, 38, Colors.BLUE, Font.semibold).draw(screen, 75, 47)
        Text("Accuratezza", size=30).draw(screen, 50, 57)
        acc_red_text = Text(f"{game.acc_red:.0%}", 38, Colors.RED, Font.semibold)
        acc_red_text.draw(screen, 15, 57)
        acc_blue_text = Text(f"{game.acc_blue:.0%}", 38, Colors.BLUE, Font.semibold)
        acc_blue_text.draw(screen, 85, 57)
        btn_menu.draw(screen, 50, 85)
        return

    # scoreboard
    scoreboard.draw(screen, 50, 11)
    Text(f"{game.score_red}", 42, Colors.RED, Font.bold).draw(screen, 20, 6)
    Text(f"{game.score_blue}", 42, Colors.BLUE, Font.bold).draw(screen, 80, 6)

    # timer
    bar_color = Colors.RED if game.first_team else Colors.BLUE
    loading_timer.draw(screen, 50, 14, color=bar_color)
    if game.turn_start and not game.pause:
        game.remaining_time -= 1 / Screen.fps
        if game.remaining_time <= 0:
            game.turn_start = False
            game.first_team = not game.first_team
            game.remaining_time = game_settings.duration
            game.turn += 1
            game.deck.next_word()
    loading_timer.fill = game.remaining_time / game_settings.duration
    time_m, time_s = divmod(game.remaining_time, 60)
    Text(f"{time_m:.0f}:{int(time_s):02d}", 48, Colors.GRAY_S).draw(screen, 50, 5)

    # pause
    if game.pause:
        btn_resume.draw(screen, 50, 40)
        btn_quit.draw(screen, 50, 60)
    if not game.pause and game.turn_start:
        btn_pause.draw(screen, 90, 14)

    # Taboo word
    if game.turn_start and not game.pause and game.deck:
        card_word.draw(screen, 50, 50)
        word = game.deck.current[0].upper() + game.deck.current[1:]
        word_guess = Text(word, 45, Colors.BLACK, Font.semibold)
        word_guess.draw_multi(screen, 50, 27, 60)
        prev_multi = False
        current_y = 35
        for i, word in enumerate(game.deck.taboo):
            word = word[0].upper() + word[1:]
            current_y = current_y + 6 + (3 if prev_multi else 0)
            color = (Colors.GRAY_M, Colors.GRAY_M2)[i % 2]
            prev_multi = Text(word, 35, color).draw_multi(screen, 50, current_y, 60)
        category = Image(f"assets/icon/{game.deck.current_icon}.png")
        category.resize(15, aspect_ratio=True)
        category.draw(screen, 85, 75, relative=True)

    # buttons
    if game.turn_start and not game.pause:
        team_skip = game.skip_red if game.first_team else game.skip_blue
        if team_skip != 0:
            team_skip = team_skip if team_skip > 0 else team_skip + 1
            Text(f"Skip: {abs(team_skip)}", 18).draw(screen, 18, 82)
        is_skippable = game.skip_red != 0 if game.first_team else game.skip_blue != 0
        (btn_skip if is_skippable else btn_skip_end).draw(screen, 18, 90)
        btn_error.draw(screen, 50, 90)
        btn_correct.draw(screen, 82, 90)
    if not game.turn_start:
        Text(f"Turno {game.turn}", 60, Colors.WHITE, Font.bold).draw(screen, 50, 45)
        team_text = "Squadra " + ("ROSSA" if game.first_team else "BLU")
        Text(team_text, color=Colors.WHITE, font=Font.bold).draw(screen, 50, 55)
        btn_start.draw(screen, 50, 85)


def manage_event(event, game, game_settings, **kwargs):
    if game.end:
        if btn_menu.handle_event(event):
            game.reset()
            game_settings.reset()
            return "menu"
    if not game.turn_start:
        if btn_start.handle_event(event):
            game.turn_start = True
            return
    if game.turn_start and not game.pause:
        if btn_correct.handle_event(event):
            if game.first_team:
                game.score_red += 1
            else:
                game.score_blue += 1
            game.deck.next_word()
        if btn_error.handle_event(event):
            if game.first_team:
                game.score_red -= 1
                game.error_red += 1
            else:
                game.score_blue -= 1
                game.error_blue += 1
            game.deck.next_word()
        is_skippable = game.skip_red != 0 if game.first_team else game.skip_blue != 0
        if btn_skip.handle_event(event) and is_skippable:
            if game.first_team:
                game.skip_red -= 1
            else:
                game.skip_blue -= 1
            game.deck.next_word()
        if btn_pause.handle_event(event):
            game.pause = True
            return
    if game.pause:
        if btn_resume.handle_event(event):
            game.pause = False
        if btn_quit.handle_event(event):
            game.reset()
            game_settings.reset()
            return "menu"


def resize(_):
    loading_timer.resize()
    scoreboard.resize()
    card_word.resize()
    winner_tab.resize()
    btn_skip.resize()
    btn_skip_end.resize()
    btn_error.resize()
    btn_correct.resize()
    btn_start.resize()
    btn_pause.resize()
    btn_resume.resize()
    btn_quit.resize()
    btn_menu.resize()


# ---- utils


def calculate_accuracy(game):
    correct_red = game.score_red + game.error_red
    total_red = correct_red + game.error_red + game.skip_red
    game.acc_red = correct_red / total_red if total_red else 0
    correct_blue = game.score_blue + game.error_blue
    total_blue = correct_blue + game.error_blue + game.skip_blue
    game.acc_blue = correct_blue / total_blue if total_blue else 0


def winning_condition(game, game_settings):
    calculate_accuracy(game)
    if not game.first_team:
        return False
    to_win = game_settings.points_to_win
    if game.score_blue >= to_win or game.score_red >= to_win:
        game.end = True
        if game.score_red == game.score_blue:
            if game.skip_red == game.skip_blue:
                if game.acc_red == game.acc_blue:
                    return choice(["t-red", "t-blue"])
                return "t-red" if game.acc_red > game.acc_blue else "t-blue"
            return "t-red" if game.skip_red > game.skip_blue else "t-blue"
        return "t-red" if game.score_red > game.score_blue else "t-blue"
    return False
