import pygame
from entity import Entity


class Character(Entity):
    def __init__(self, game, position, groups, atkables, collidables, tiles):
        super().__init__(position, groups, atkables, collidables, tiles)
        self.game = game
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        self.rect = self.image.get_rect(midbottom=position)
        self.hitbox = pygame.rect.Rect(self.rect.left, self.rect.top + self.rect.height/2, self.rect.width, self.rect.height/2)

    def action_input(self):
        keys = pygame.key.get_pressed()

        self.inputV = pygame.Vector2()
        if keys[pygame.K_UP]:
            self.inputV.y -= 1
        if keys[pygame.K_DOWN]:
            self.inputV.y += 1
        if keys[pygame.K_RIGHT]:
            self.inputV.x += 1
        if keys[pygame.K_LEFT]:
            self.inputV.x -= 1

        # handle character state
        if self.inputV.xy != (0, 0):
            self.inputV.normalize_ip()
            if keys[pygame.K_LCTRL]:
                self.set_action("run")
                self.inputV *= 1.3
            else:
                self.set_action("walk")
            if self.inputV.x > 0:
                self.set_direction("right")
            elif self.inputV.x < 0:
                self.set_direction("left")
            elif self.inputV.y > 0:
                self.set_direction("down")
            else:
                self.set_direction("up")
        else:
            self.set_action("idle")

    def update(self, dt):
        self.cool_down(dt)
        if not self.game.chatting:
            self.action_input()
        self.move(dt)
        self.animate(dt)
        # print(self.state)
        print("Char: ", self.hitbox)


class OtherPlayer(Character):
    def __init__(self, position, groups, atkables, collidables, tiles):
        self.image = pygame.Surface((0, 0))
        super().__init__(position, groups, atkables, collidables, tiles)

    def update(self, dt):
        self.cool_down(dt)
        self.move(dt)
        self.animate(dt)
