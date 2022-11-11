import pygame

from command_line import CommandLine


class Chat:
    def __init__(self, game, base_display):
        self.command_line = CommandLine(game)
        self.fontsize = 16
        self.font = pygame.font.Font(None, self.fontsize)
        self.b_display = base_display
        reso = base_display.get_size()
        self.box_rect = pygame.Rect(0, reso[1]/3*2, reso[0]/3, reso[1]/3)
        self.input_rect = pygame.Rect(0, reso[1] - self.fontsize, reso[0]/3 - 4, self.fontsize)
        self.in_text_surf = None

        self.cursor = 0
        self.in_text = ""

        self.held_keys = {}
        self.letter = None

    def text_input(self, event_loop):
        tick = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        for held_key, keydown_data in self.held_keys.items():
            if keys[held_key]:
                if tick - keydown_data[0] > 300:
                    keydown_data[1]()
        for event in event_loop.copy():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    continue
                elif event.key == pygame.K_BACKSPACE:
                    self.backspace()
                    self.held_keys[event.key] = (tick, self.backspace)
                elif event.key == pygame.K_DELETE:
                    self.delete()
                    self.held_keys[event.key] = (tick, self.delete)
                elif event.key == pygame.K_LEFT:
                    self.left()
                    self.held_keys[event.key] = (tick, self.left)
                elif event.key == pygame.K_RIGHT:
                    self.right()
                    self.held_keys[event.key] = (tick, self.right)
                elif event.key == pygame.K_HOME:
                    self.cursor = 0
                elif event.key == pygame.K_END:
                    self.cursor = len(self.in_text)
                elif event.key == pygame.K_RSHIFT:
                    pass
                else:
                    self.letter = event.unicode
                    self.type()
                    self.held_keys[event.key] = (tick, self.type)
            if event.type == pygame.KEYUP:
                if event.key in self.held_keys:
                    del self.held_keys[event.key]

    def type(self):
        self.in_text = self.in_text[:self.cursor] + self.letter + self.in_text[self.cursor:]
        self.cursor += 1

    def backspace(self):
        if self.cursor > 0:
            self.in_text = self.in_text[:self.cursor - 1] + self.in_text[self.cursor:]
            self.cursor -= 1

    def delete(self):
        if self.cursor < len(self.in_text):
            self.in_text = self.in_text[:self.cursor] + self.in_text[self.cursor + 1:]

    def left(self):
        self.cursor -= 1

    def right(self):
        self.cursor += 1

    def send(self):
        if self.in_text != "":
            print("Sending some shit")
            if self.in_text.startswith("/"):
                print("Command received")
                self.command_line.execute(self.in_text[1:])
            self.in_text = ""

    def update(self, event_loop):
        self.text_input(event_loop)

        # draw chat box
        pygame.draw.rect(self.b_display, pygame.Color("lightskyblue3"), self.box_rect, 1)

        # make text surface
        self.in_text_surf = self.font.render(self.in_text, True, (255, 255, 255))

        # fix rect based on message length
        right = self.input_rect.right
        self.input_rect.w = max(self.in_text_surf.get_width(), self.box_rect.w)
        self.input_rect.right = right

        # textbox_x = self.input_rect.x + self.input_rect.width - self.in_text_surf.get_width()
        self.b_display.blit(self.in_text_surf, (self.input_rect.x + 4, self.input_rect.y + 4))
