# ball.py

import math
import random

import pygame
from ball_state import BallState
from event import Event
from side import Side


class Ball(pygame.sprite.Sprite):
    """Define uma instância da bola"""

    def __init__(self, screen: pygame.surface.Surface, settings: dict) -> None:
        """Inicializa uma instância da bola"""
        super().__init__()
        self.settings = settings
        self._layer = 3
        self.screen = screen
        self.image = pygame.surface.Surface((self.settings["ball.size"], self.settings["ball.size"]))
        self.image.fill(pygame.color.THECOLORS[self.settings["ball.color"]])
        self.rect = self.image.get_rect()

        self.rect.x = -self.settings["ball.size"]
        self.rect.y = -self.settings["ball.size"]

        self.state = BallState.WAITING
        self.accumulator = 0.0
        self.velocity = pygame.Vector2()
        self.acceleration = self.settings["ball.acceleration"]

    def update(self, dt: float) -> None:
        """Atualiza o estado da bola"""
        if self.state == BallState.WAITING:
            self.handle_waiting_state(dt)
        elif self.state == BallState.PLAYING:
            self.handle_playing_state(dt)

    def handle_waiting_state(self, dt: float) -> None:
        """Gerencia a bola em espera"""
        self.accumulator += dt

        if self.accumulator < self.settings["ball.waiting.time.appear"]:
            pass
        elif self.accumulator < self.settings["ball.waiting.time.settledown"]:
            self.reset_position()
        elif self.accumulator < self.settings["ball.waiting.time.play"]:
            pass
        else:
            self.reset_velocity()
            self.accumulator = 0.0
            self.state = BallState.PLAYING

    def handle_playing_state(self, dt: float) -> None:
        """Gerencia a bola em jogo"""
        self.rect.centerx += round(self.velocity.x * dt)
        self.rect.centery += round(self.velocity.y * dt)

    def reset_position(self) -> None:
        """Reconfigura a posição da bola"""
        y = random.randrange(
            self.screen.get_rect().top + (self.settings["wall.size"] * 2),
            self.screen.get_rect().bottom,
            self.settings["ball.size"] * 2,
        )

        self.rect.centerx = self.screen.get_rect().centerx
        self.rect.centery = y
        pygame.event.post(pygame.event.Event(Event.START.value))

    def reset_velocity(self) -> None:
        """Reinicia o vetor velocidade da bola"""
        degrees = random.uniform(-self.settings["ball.angle.max"], self.settings["ball.angle.max"])

        if random.choice([-1, 1]) == -1:
            degrees += 180

        self.velocity = self.configure_velocity(degrees)
        self.acceleration = self.settings["ball.acceleration"]

    def stroke(self, collision_point: float, side: Side) -> None:
        """Gerencia a rebatida da bola"""
        degrees = self.settings["ball.angle.max"] * (collision_point / (self.settings["paddle.height"] / 2))

        if side == Side.RIGHT:
            degrees *= -1

        if self.velocity.x < 0:
            degrees += 180

        vector2 = self.configure_velocity(degrees) * self.acceleration

        if vector2.magnitude_squared() <= self.settings["ball.speed.max"]:
            self.velocity = vector2
            self.acceleration += self.settings["ball.acceleration.increment"]
        else:
            self.velocity = vector2

    def configure_velocity(self, degrees: float) -> pygame.Vector2:
        """Configura o vetor velocidade da bola"""
        radians = math.radians(degrees)
        dx = self.settings["ball.speed"] * math.cos(radians)
        dy = self.settings["ball.speed"] * math.sin(radians)
        velocity = pygame.Vector2(dx, dy)

        return velocity
