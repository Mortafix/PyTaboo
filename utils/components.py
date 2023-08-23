from math import ceil

import pygame
from static.settings import Colors, Screen


def relative_position(screen, x=None, y=None):
    width, height = Screen.size
    if screen:
        width, height = screen.get_size()
    x = x and width * x / 100
    y = y and height * y / 100
    return x, y


def relative_size(width=None, height=None):
    screen = pygame.display.get_surface()
    return relative_position(screen, width, height)


# ---- base


class Font:
    regular = "assets/font/comfortaa_regular.ttf"
    light = "assets/font/comfortaa_light.ttf"
    medium = "assets/font/comfortaa_medium.ttf"
    semibold = "assets/font/comfortaa_semibold.ttf"
    bold = "assets/font/comfortaa_bold.ttf"


class BaseComponent:
    x = 0
    y = 0
    width = 0
    height = 0


class Text(BaseComponent):
    def __init__(self, text, size=42, color=Colors.BLACK, font=Font.regular):
        self.text = str(text)
        self.size = size
        self.color = color
        self.font_file = font

    def draw(self, screen, x, y):
        self.x, self.y = relative_position(screen, x, y)
        font = pygame.font.Font(self.font_file, self.size)
        title_surf = font.render(self.text, True, self.color)
        screen.blit(title_surf, (self.x - title_surf.get_width() // 2, self.y))

    def draw_multi(self, screen, x, y, max_width):
        self.x, self.y = relative_position(screen, x, y)
        max_width, _ = relative_size(max_width)
        font = pygame.font.Font(self.font_file, self.size)
        line_spacing = font.get_linesize()
        space_width, font_h = font.size(" ")
        # line splitting
        words = self.text.split(" ")
        lines, line = [], ""
        for word in words:
            if font.size(line + word)[0] <= max_width:
                line += word + " "
            else:
                lines.append(line)
                line = word + " "
        lines.append(line)
        lines = [line for line in lines if line.strip()]
        # draw
        if len(lines) > 1:
            self.y -= font_h // 3
        for line in lines:
            title_surf = font.render(line, True, self.color)
            screen.blit(title_surf, (self.x - title_surf.get_width() // 2, self.y))
            self.y += line_spacing
        return len(lines) > 1


class Image(BaseComponent):
    def __init__(self, image, width=None, height=None):
        self.file = image
        self.background = pygame.image.load(image)
        self.width, self.height = self.background.get_size()
        if width and height:
            self.width, self.height = relative_size(width, height)
            self.background = pygame.transform.smoothscale(
                self.background, (self.width, self.height)
            )

    def draw(self, screen, x=0, y=0, relative=False):
        if relative:
            relx, rely = relative_position(screen, x, y)
            x, y = relx - self.width // 2, rely - self.height // 2
        screen.blit(self.background, (x, y))

    def resize(self, width, height=None, aspect_ratio=False):
        if aspect_ratio:
            self.old_width = self.width
            self.width, _ = relative_size(width)
            self.height = self.width * self.height / self.old_width
        else:
            self.width, self.height = relative_size(width, height)
        self.background = pygame.transform.smoothscale(
            self.background, (self.width, self.height)
        )
        return self


# ---- Buttons


class Button(BaseComponent):
    def __init__(self, button, width=100, value=None):
        self.value = value
        self.relativ_width = width
        self.image = Image(f"assets/buttons/{button}.png")
        self.resize()

    def draw(self, screen, x, y):
        self.x, self.y = relative_position(screen, x, y)
        self.x -= self.width // 2
        self.y -= self.height // 2
        self.image.draw(screen, self.x, self.y)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
                return True
        return False

    def resize(self):
        self.image.resize(self.relativ_width, aspect_ratio=True)
        self.width, self.height = self.image.width, self.image.height


class SelectableButton(Button):
    def __init__(self, button, width=100, value=None):
        super().__init__(button, width, value)
        self.button_normal = self.image
        self.button_select = Image(f"assets/buttons/{button}_select.png")
        self.button_select.resize(width, aspect_ratio=True)
        self.deselect()

    def select(self):
        self.selected = True
        self.image = self.button_select

    def deselect(self):
        self.selected = False
        self.image = self.button_normal

    def draw(self, screen, x, y):
        self.image.draw(screen, self.x, self.y)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
                return True
        return False


class ButtonGroup(BaseComponent):
    def __init__(self, button_texts, y, index=0, spacing=10, size=36):
        self.y = y
        self.spacing = spacing
        self.size = size
        self.buttons = list()
        if button_texts:
            self.buttons = [
                SelectableButton(file, 15, value) for file, value in button_texts
            ]
            self.buttons[index].select()

    def _reposition_buttons(self, screen):
        total_buttons_width = sum([btn.width for btn in self.buttons])
        total_spacing_width = self.spacing * (len(self.buttons) - 1)
        total_width = total_buttons_width + total_spacing_width
        # calculate offset
        x_offset = (screen.get_size()[0] - total_width) / 2
        for btn in self.buttons:
            _, btn.y = relative_position(screen, y=self.y)
            btn.y -= btn.height // 2
            btn.x = x_offset
            x_offset += btn.width + self.spacing

    def draw(self, screen):
        self._reposition_buttons(screen)
        for btn in self.buttons:
            btn.draw(screen, btn.y, btn.y)

    def handle_event(self, event):
        for btn in self.buttons:
            if btn.handle_event(event):
                for other_btn in self.buttons:
                    other_btn.deselect()
                btn.select()
                return btn.value
        return None

    def resize(self, screen):
        for btn in self.buttons:
            btn.resize()
        self._reposition_buttons(screen)


# ---- Deck


class Deck(BaseComponent):
    def __init__(self, title, icon, word_count):
        self.icon = Image(f"assets/icon/{icon}.png").resize(16, aspect_ratio=True)
        self.title = title
        self.word_count = word_count
        self.selected = False

        # Dimensioni e posizioni relative
        _, self.icon_padding = relative_size(height=2)
        _, self.text_padding = relative_size(height=1)
        self.width, _ = relative_size(10)
        _, padding_bottom = relative_size(height=5)
        self.height = self.icon.height + 2 * self.text_padding + padding_bottom
        folder = "assets/shape/"
        self.base = Image(f"{folder}deck.png").resize(35, aspect_ratio=True)
        self.select = Image(f"{folder}deck_select.png").resize(35, aspect_ratio=True)
        self.width, self.height = self.base.width, self.base.height

    def draw(self, screen):
        self.card = self.select if self.selected else self.base
        current_y = self.y + self.icon_padding
        self.card.draw(screen, self.x, self.y)
        self.icon.draw(screen, self.x + (self.width - self.icon.width) // 2, current_y)
        # texts
        font = pygame.font.Font(Font.semibold, 24)
        title = font.render(self.title, True, Colors.BLACK)
        font = pygame.font.Font(Font.regular, 20)
        count = font.render(f"{self.word_count} parole", True, Colors.GRAY_S)
        current_y += self.icon.height + self.text_padding
        screen.blit(
            title,
            (self.x + (self.width - title.get_width()) // 2, current_y),
        )
        current_y += title.get_height()
        screen.blit(
            count,
            (self.x + (self.width - count.get_width()) // 2, current_y),
        )
        self.total_height = current_y

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (
                self.x <= mouse_x <= self.x + self.width
                and self.y <= mouse_y <= self.y + self.height
            ):
                self.selected = not self.selected
                return True
        return False


class DeckGrid(BaseComponent):
    def __init__(self, decks, y):
        self.decks = decks
        self.y = y
        # postion
        self.rows = 3
        self.cols = 2
        self.spacing = 20
        self.xs = [120 // (self.cols + 1) * i for i in range(1, self.cols + 1)]
        self.ys = [85 // (self.rows + 1) * i for i in range(1, self.rows + 1)]
        # pages
        self.current_page = 0
        self.decks_per_page = self.rows * self.cols
        self.total_pages = ceil(len(self.decks) / self.decks_per_page)
        # buttons
        self.prev_button = Button("grid_left", 7)
        self.next_button = Button("grid_right", 7)

    def draw(self, screen):
        for i, y in enumerate(self.ys):
            for j, x in enumerate(self.xs):
                offset = self.current_page * self.decks_per_page
                index = i * self.cols + j
                if offset + index < len(self.decks):
                    deck = self.decks[offset + index]
                    deck.x, deck.y = relative_position(
                        screen, x - self.spacing // 2, y + self.y
                    )
                    deck.x -= deck.width // 2
                    deck.y -= deck.height // 2
                    deck.draw(screen)
        # buttons
        if self.current_page > 0:
            self.prev_button.draw(screen, 7, 50)
        if self.current_page < self.total_pages - 1:
            self.next_button.draw(screen, 93, 50)

    def handle_event(self, event):
        # navigation buttons
        if self.prev_button.handle_event(event) and self.current_page > 0:
            self.current_page -= 1
        if (
            self.next_button.handle_event(event)
            and self.current_page < self.total_pages - 1
        ):
            self.current_page += 1
        # decks selection
        start_idx = self.current_page * self.decks_per_page
        end_idx = start_idx + self.decks_per_page
        for deck in self.decks[start_idx:end_idx]:
            if deck.handle_event(event):
                return deck
        return None


class LoadingBar(BaseComponent):
    def __init__(self, width, height=4, fill=100):
        self.original_width, self.original_height = width, height
        self.width, self.height = relative_size(width, height)
        self.fill = 1

    def draw(self, screen, x, y, bg=Colors.GRAY_S, color=Colors.BLACK):
        self.x, self.y = relative_position(screen, x, y)
        self.x -= self.width // 2
        self.y -= self.height // 2
        pygame.draw.rect(screen, bg, (self.x, self.y, self.width, self.height))
        width_remaining = self.fill
        pygame.draw.rect(
            screen,
            color,
            (self.x, self.y, width_remaining * self.width, self.height),
        )

    def resize(self):
        self.width, self.height = relative_size(
            self.original_width, self.original_height
        )


# ---- Shapes


class Rectangle(BaseComponent):
    def __init__(self, width, height, rounded=False, trasparent=False):
        filename = "assets/shape/rectangle"
        filename += "_round" if rounded else ""
        filename += "_trasp" if trasparent else ""
        filename += ".png"
        self.original_width, self.original_height = width, height
        self.image = Image(filename, width, height)

    def draw(self, screen, x, y):
        self.x, self.y = relative_position(screen, x, y)
        self.x -= self.image.width // 2
        self.y -= self.image.height // 2
        self.image.draw(screen, self.x, self.y)

    def resize(self):
        self.image.resize(self.original_width, self.original_height)
