# paddle.py

import pygame
from side import Side
from wall import WALL_HEIGHT

PADDLE_SPEED = 250
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_COLOR = pygame.color.THECOLORS["grey100"]
PADDLE_ACCELERATION = 1.0
PADDLE_ACCELERATION_INCREMENT = 0.075


class Paddle(pygame.sprite.Sprite):
    """Define uma instância de uma raquete"""

    def __init__(self, screen: pygame.surface.Surface, side: Side) -> None:
        """Inicializa uma instância de uma raquete"""
        super().__init__()
        self._layer = 2
        self.screen = screen
        self.image = pygame.surface.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(PADDLE_COLOR)
        self.rect = self.image.get_rect()
        self.side = side
        self.velocity = pygame.Vector2()
        self.acceleration = PADDLE_ACCELERATION

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
            paddle_top >= self.screen.get_rect().top + WALL_HEIGHT
            and paddle_bottom <= self.screen.get_rect().bottom - WALL_HEIGHT
        ):
            self.rect.centery += changey
        else:
            if self.velocity.y < 0:
                self.rect.top = self.screen.get_rect().top + WALL_HEIGHT
            elif self.velocity.y > 0:
                self.rect.bottom = self.screen.get_rect().bottom - WALL_HEIGHT

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
                self.acceleration += PADDLE_ACCELERATION_INCREMENT
            else:
                self.acceleration = PADDLE_ACCELERATION

            self.velocity = pygame.Vector2(0, PADDLE_SPEED * self.acceleration)
        elif keys[key_up] and not keys[key_down]:
            if self.velocity.y < 0:
                self.acceleration += PADDLE_ACCELERATION_INCREMENT
            else:
                self.acceleration = PADDLE_ACCELERATION

            self.velocity = pygame.Vector2(0, (PADDLE_SPEED * self.acceleration) * -1)
        else:
            self.velocity = pygame.Vector2()
            self.acceleration = PADDLE_ACCELERATION
