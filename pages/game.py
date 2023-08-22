from random import choice

from static.settings import Colors
from utils.components import Button, Font, Image, LoadingBar, Rectangle, Text

# components
loading_timer = LoadingBar(50, 14, 70)
scoreboard = Rectangle(50, 11, 95, 17)
card_word = Rectangle(50, 50, 80, 60, trasparent=True)
winner_tab = Rectangle(50, 40, 95, 70)
btn_skip = Button("word_skip", 18, 90, 30)
btn_skip_end = Button("word_skip_end", 18, 90, 30)
btn_error = Button("word_wrong", 50, 90, 30)
btn_correct = Button("word_correct", 82, 90, 30)
btn_start = Button("go", 50, 85, 30)
btn_pause = Button("pause", 90, 14, 8)
btn_resume = Button("resume", 50, 40, 65)
btn_quit = Button("quit", 50, 60, 45)
btn_menu = Button("menu", 50, 85, 45)


def run(screen, game, game_settings, **kwargs):
    screen.fill(Colors.RED if game.first_team else Colors.BLUE)

    # winner
    if not game.turn_start and (winner := winning_condition(game, game_settings)):
        winner_text = "ROSSA" if winner == "t-red" else "BLU"
        winner_color = Colors.RED if winner == "t-red" else Colors.BLUE
        screen.fill(winner_color)
        winner_tab.draw(screen)
        Text("Vittoria!!", 50, 15, color=winner_color).draw(screen)
        Text(f"Squadra {winner_text}", 50, 20, color=winner_color).draw(screen)
        Text("Punti", 50, 37, size=30).draw(screen)
        Text(game.score_red, 25, 37, 38, Colors.RED, Font.semibold).draw(screen)
        Text(game.score_blue, 75, 37, 38, Colors.BLUE, Font.semibold).draw(screen)
        Text("Skip", 50, 47, size=30).draw(screen)
        offset_skip = 2 if game_settings.skips < 0 else 0
        skip_used_red = game_settings.skips - game.skip_red - offset_skip
        skip_used_blue = game_settings.skips - game.skip_blue - offset_skip
        Text(skip_used_red, 25, 47, 38, Colors.RED, Font.semibold).draw(screen)
        Text(skip_used_blue, 75, 47, 38, Colors.BLUE, Font.semibold).draw(screen)
        Text("Accuratezza", 50, 57, size=30).draw(screen)
        Text(f"{game.acc_red:.0%}", 15, 57, 38, Colors.RED, Font.semibold).draw(screen)
        Text(f"{game.acc_blue:.0%}", 85, 57, 38, Colors.BLUE, Font.semibold).draw(
            screen
        )
        btn_menu.draw(screen)
        return

    # scoreboard
    scoreboard.draw(screen)
    Text(f"{game.score_red}", 20, 6, 42, Colors.RED, Font.bold).draw(screen)
    Text(f"{game.score_blue}", 80, 6, 42, Colors.BLUE, Font.bold).draw(screen)

    # timer
    bar_color = Colors.RED if game.first_team else Colors.BLUE
    loading_timer.draw(screen, color=bar_color)
    if game.turn_start and not game.pause:
        game.remaining_time -= 1 / 60
        if game.remaining_time <= 0:
            game.turn_start = False
            game.first_team = not game.first_team
            game.remaining_time = game_settings.duration
            game.turn += 1
    loading_timer.fill = game.remaining_time / game_settings.duration
    time_m, time_s = divmod(game.remaining_time, 60)
    Text(f"{time_m:.0f}:{int(time_s):02d}", 50, 5, 48, Colors.GRAY_S).draw(screen)

    # pause
    if game.pause:
        btn_resume.draw(screen)
        btn_quit.draw(screen)
    if not game.pause and game.turn_start:
        btn_pause.draw(screen)

    # Taboo word
    if game.turn_start and not game.pause and game.deck:
        card_word.draw(screen)
        word = game.deck.current[0].upper() + game.deck.current[1:]
        word_guess = Text(word, 50, 27, 45, Colors.BLACK, Font.semibold)
        word_guess.draw_multi(screen, 60)
        prev_multi = False
        current_y = 35
        for i, word in enumerate(game.deck.taboo):
            word = word[0].upper() + word[1:]
            current_y = current_y + 6 + (3 if prev_multi else 0)
            color = (Colors.GRAY_M, Colors.GRAY_M2)[i % 2]
            prev_multi = Text(word, 50, current_y, 35, color).draw_multi(screen, 60)
        category = Image(f"assets/icon/{game.deck.current_icon}.png")
        category.resize(15, aspect_ratio=True)
        category.draw(screen, 85, 75, relative=True)

    # buttons
    if game.turn_start and not game.pause:
        team_skip = game.skip_red if game.first_team else game.skip_blue
        if team_skip != 0:
            team_skip = team_skip if team_skip > 0 else team_skip + 1
            skip_title = Text(f"Skip: {abs(team_skip)}", 18, 82, size=18)
            skip_title.draw(screen)
        is_skippable = game.skip_red != 0 if game.first_team else game.skip_blue != 0
        (btn_skip if is_skippable else btn_skip_end).draw(screen)
        btn_error.draw(screen)
        btn_correct.draw(screen)
    if not game.turn_start:
        turn = Text(f"Turno {game.turn}", 50, 45, 60, Colors.WHITE, Font.bold)
        turn.draw(screen)
        team_text = "ROSSA" if game.first_team else "BLU"
        team = Text(f"Squadra {team_text}", 50, 55, color=Colors.WHITE, font=Font.bold)
        team.draw(screen)
        btn_start.draw(screen)


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
