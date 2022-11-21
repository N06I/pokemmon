import time

import pygame

from command_line import CommandLine


class Chat:
    channel_colors = {"global": [5, 22, 39],
                      "l": [245, 250, 240],
                      "p":[139, 113, 118],
                      "g": [255, 159, 28],
                      "w": [46, 196, 182],
                      "sys": [231, 29, 54]}    # global, local, party, guild, whisper, system
    chan_names = {"global": "Everyone", "l": "Here", "p": "Party", "g": "Guild", "w": "Private", "sys": "System"}

    def __init__(self, game):
        # tech setup
        self.game = game
        self.command_line = CommandLine(game)
        self.display = pygame.display.get_surface()
        reso = self.display.get_size()

        # font setup
        self.fontsize = int(reso[1] / 22)
        self.font = pygame.font.Font(None, self.fontsize)

        # chatbox setup
        self.chatbox_rect = pygame.Rect(0, reso[1]/3*2, reso[0]/3, reso[1]/3 - self.fontsize)
        self.box_chat_surf = pygame.Surface(self.chatbox_rect.size, pygame.SRCALPHA)
        self.chatbox_color = pygame.Color(55, 55, 82, 128)
        # tech
        self.shown_channels = ["global", "l", "p", "g", "w", "sys"]
        self.hidden_channels = []
        self.box_msgs = []

        # inputline setup
        self.inputline_rect = pygame.Rect(0, reso[1] - self.fontsize, reso[0]/3, self.fontsize)
        self.inputline_surf = pygame.Surface(self.inputline_rect.size, pygame.SRCALPHA)
        self.inputline_color = pygame.Color(111, 111, 130, 192)

        # input text setup
        self.in_text_rect = pygame.Rect(0, reso[1] - self.fontsize, reso[0] / 3, self.fontsize)
        self.in_text_surf = None
        # tech
        self.cursor = 0
        self.in_text = ""
        self.held_keys = {}
        self.letter = None
        self.channel = "l"

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
                elif event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                    continue
                else:
                    self.letter = event.unicode
                    self.type()
                    self.held_keys[event.key] = (tick, self.type)
            if event.type == pygame.KEYUP:
                if event.key in self.held_keys:
                    del self.held_keys[event.key]

    def type(self):
        if len(self.in_text) < 200:
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

    def send(self, text, channel=None):
        if channel is None:
            channel = self.channel
        if text != "":
            if text.startswith("/"):
                self.command_line.execute(text[1:])
            else:
                self.box_msgs.append(Message(text, channel, self.game.pid))
            self.in_text = ""
            self.cursor = 0
        print("\nChat logs:")
        for message in self.box_msgs:
            print(message.text)

    def channel_switch(self, channel):
        self.channel = channel

    def blit_messages(self, msg_list, surface):
        y = surface.get_height()
        for i in range(-1, - (len(msg_list) + 1), -1):     # basically means for msg in msg_list
            msg = msg_list[i]
            if msg.channel in self.shown_channels:
                msg_surf = self.get_message_surface(msg, surface)
                y -= msg_surf.get_height()
                surface.blit(msg_surf, (0, y))

    def get_message_surface(self, msg, box_surf):
        msg_surf = pygame.Surface((box_surf.get_width(), 2000))
        msg_surf.set_colorkey((0,0,0))
        x = 0
        y = 0
        words = msg.text.split()
        words.insert(0, f"[{msg.time}]({msg.channel}){msg.sender}:")
        for word in words:
            w_surf = self.font.render(" " + word, True, self.channel_colors[msg.channel])
            word_width = w_surf.get_width()
            if x + word_width > box_surf.get_width() and x != 0:
                y += self.fontsize
                x = 0
            msg_surf.blit(w_surf, (x, y))
            x += word_width
        return msg_surf.subsurface(0, 0, box_surf.get_width(), y + self.fontsize)

    def update(self, event_loop, dt):
        tick = pygame.time.get_ticks()
        if self.game.chatting:
            self.text_input(event_loop)
            self.inputline_surf.fill(self.inputline_color)
            # make text input surface
            self.in_text_surf = self.font.render(self.in_text, True, self.channel_colors[self.channel])

            # fix inputline rect based on message length
            right = self.in_text_rect.right
            self.in_text_rect.w = max(self.in_text_surf.get_width(), self.inputline_rect.w)
            self.in_text_rect.right = right

            # blit input text
            self.display.blit(self.inputline_surf, self.inputline_rect)
            self.display.blit(self.in_text_surf, (self.in_text_rect.x, self.in_text_rect.y + 4))
            # border
            pygame.draw.rect(self.display, self.inputline_color, self.inputline_rect, 1)

        if self.game.chatting or tick - self.box_msgs[-1].time < 3000:
            # make and blit chat surface
            self.box_chat_surf = pygame.Surface(self.chatbox_rect.size, pygame.SRCALPHA)
            self.box_chat_surf.fill(self.chatbox_color)
            self.blit_messages(self.box_msgs, self.box_chat_surf)
            self.display.blit(self.box_chat_surf, (self.chatbox_rect.x, self.chatbox_rect.y + 1))
            # border
            pygame.draw.rect(self.display, self.chatbox_color, self.chatbox_rect, 1)


class Message:
    def __init__(self, text, channel, sender):
        self.text = text
        self.channel = channel
        self.sender = sender
        self.time = pygame.time.get_ticks()
