# paddle.py

import pygame
from side import Side


class Paddle(pygame.sprite.Sprite):
    """Define uma instância de uma raquete"""

    def __init__(self, screen: pygame.surface.Surface, side: Side, settings: dict) -> None:
        """Inicializa uma instância de uma raquete"""
        super().__init__()
        self.settings = settings
        self._layer = 2
        self.screen = screen
        self.image = pygame.surface.Surface((self.settings["paddle.width"], self.settings["paddle.height"]))
        self.image.fill(pygame.color.THECOLORS[self.settings["paddle.color"]])
        self.rect = self.image.get_rect()
        self.side = side
        self.velocity = pygame.Vector2()
        self.acceleration = self.settings["paddle.acceleration"]

        if side == Side.LEFT:
            self.rect.left = self.screen.get_rect().left + (self.rect.width * 3)
            self.rect.centery = self.screen.get_rect().centery
        elif side == Side.RIGHT:
            self.rect.right = self.screen.get_rect().right - (self.rect.width * 3)
            self.rect.centery = self.screen.get_rect().centery

    def update(self, dt: float) -> None:
        """Atualiza o estado de uma raquete"""
        changey = round(self.velocity.y * dt)

        paddle_top = self.rect.top + changey
        paddle_bottom = self.rect.bottom + changey

        if (
            paddle_top >= self.screen.get_rect().top + self.settings["wall.height"]
            and paddle_bottom <= self.screen.get_rect().bottom - self.settings["wall.height"]
        ):
            self.rect.centery += changey
        else:
            if self.velocity.y < 0:
                self.rect.top = self.screen.get_rect().top + self.settings["wall.height"]
            elif self.velocity.y > 0:
                self.rect.bottom = self.screen.get_rect().bottom - self.settings["wall.height"]

    def update_direction(self, keys: pygame.key.ScancodeWrapper) -> None:
        """Atualiza a direção de uma raquete"""
        if self.side == Side.LEFT:
            self.process_interaction(keys, pygame.K_w, pygame.K_s)
        elif self.side == Side.RIGHT:
            self.process_interaction(keys, pygame.K_UP, pygame.K_DOWN)

    def process_interaction(self, keys: pygame.key.ScancodeWrapper, key_up: int, key_down: int) -> None:
        """Processa a interação do jogador com a raquete"""
        if keys[key_down] and not keys[key_up]:
            if self.velocity.y > 0:
                self.acceleration += self.settings["paddle.acceleration.increment"]
            else:
                self.acceleration = self.settings["paddle.acceleration"]

            self.velocity = pygame.Vector2(0, self.settings["paddle.speed"] * self.acceleration)
        elif keys[key_up] and not keys[key_down]:
            if self.velocity.y < 0:
                self.acceleration += self.settings["paddle.acceleration.increment"]
            else:
                self.acceleration = self.settings["paddle.acceleration"]

            self.velocity = pygame.Vector2(0, (self.settings["paddle.speed"] * self.acceleration) * -1)
        else:
            self.velocity = pygame.Vector2()
            self.acceleration = self.settings["paddle.acceleration"]
