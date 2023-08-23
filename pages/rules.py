from utils.components import Button, Font, Image, Rectangle, Text

# components
bg = Image("assets/images/origami_bg.jpeg", 100, 100)
title = Text("Regole del gioco", size=50, font=Font.semibold)
goal_text = Text(
    "L'obiettivo del gioco è far indovinare ai membri della propria squadra le parole "
    "di ogni carta senza usare le parole taboo elencate sotto di essa.",
    27,
)
rules_text = Text(
    "Dividetevi in 2 squadre. Ogni turno un giocatore della squadra deve far indovinare"
    " la parola ai suoi compagni senza usare gesti, suoni, variazioni e le parole "
    "taboo. Nel mentre, un giocatore dell'altra squadra controlla che non vengano usate"
    " le parole taboo.",
    27,
)
winner_text = Text(
    "Vince chi arriva prima al punteggio stabilito. In caso di parità vince chi ha "
    "usato meno skip o chi ha ottenuto un'accuratezza maggiore.",
    27,
)
card = Rectangle(95, 82, trasparent=True)
btn_back = Button("back", 10)


def run(screen, **kwargs):
    bg.draw(screen)
    title.draw(screen, 50, 5)
    card.draw(screen, 50, 50)
    goal_text.draw_multi(screen, 50, 17, 85)
    rules_text.draw_multi(screen, 50, 37, 85)
    winner_text.draw_multi(screen, 50, 69, 85)
    btn_back.draw(screen, 15, 90)


def manage_event(event, game, game_settings, **kwargs):
    if btn_back.handle_event(event):
        return "menu"


def resize(_):
    bg.resize(100, 100)
    card.resize()
    btn_back.resize()
