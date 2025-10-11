# ball.py

import pygame
import random
from event import Event
import math
from side import Side
from wall import WALL_HEIGHT
from paddle import PADDLE_HEIGHT
from ball_state import BallState

BALL_SPEED = 750
BALL_SIZE = 10
BALL_COLOR = pygame.color.THECOLORS["grey100"]
BALL_MAX_ANGLE = 45
BALL_WAIT_TIME_TO_APPEAR = 1.0
BALL_WAIT_TIME_TO_SETTLE_DOWN = 2.0
BALL_WAIT_TIME_TO_PLAY = 3.0
BALL_ACCELERATION = 1.0
BALL_ACCELERATION_INCREMENT = 0.10
BALL_MAX_SPEED_SQUARED = 5_000_000


class Ball(pygame.sprite.Sprite):
    """Define uma instância da bola"""

    def __init__(self, screen: pygame.surface.Surface) -> None:
        """Inicializa uma instância da bola"""
        super().__init__()
        self._layer = 3
        self.screen = screen
        self.image = pygame.surface.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill(BALL_COLOR)
        self.rect = self.image.get_rect()

        self.rect.x = -BALL_SIZE
        self.rect.y = -BALL_SIZE

        self.state = BallState.WAITING
        self.accumulator = 0.0
        self.velocity = pygame.Vector2()
        self.acceleration = BALL_ACCELERATION

    def update(self, dt: float) -> None:
        """Atualiza o estado da bola"""
        if self.state == BallState.WAITING:
            self.handle_waiting_state(dt)
        elif self.state == BallState.PLAYING:
            self.handle_playing_state(dt)

    def handle_waiting_state(self, dt: float) -> None:
        """Gerencia a bola em espera"""
        self.accumulator += dt

        if self.accumulator < BALL_WAIT_TIME_TO_APPEAR:
            pass
        elif self.accumulator < BALL_WAIT_TIME_TO_SETTLE_DOWN:
            self.reset_position()
        elif self.accumulator < BALL_WAIT_TIME_TO_PLAY:
            pass
        else:
            self.reset_velocity()
            self.accumulator = 0.0
            self.state = BallState.PLAYING

    def handle_playing_state(self, dt: float) -> None:
        """Gerencia a bola em jogo"""
        self.rect.centery += round(self.velocity.y * dt)

        changex = round(self.velocity.x * dt)

        ball_left = self.rect.left + changex
        ball_right = self.rect.right + changex

        if ball_right >= self.screen.get_rect().left and ball_left <= self.screen.get_rect().right:
            self.rect.centerx += changex
        else:
            if self.velocity.x < 0:
                self.rect.right = self.screen.get_rect().left
                pygame.event.post(pygame.event.Event(Event.LEFT_GOAL.value))
            elif self.velocity.x > 0:
                self.rect.left = self.screen.get_rect().right
                pygame.event.post(pygame.event.Event(Event.RIGHT_GOAL.value))

            self.state = BallState.WAITING

    def reset_position(self) -> None:
        """Reconfigura a posição da bola"""
        y = random.randrange(
            self.screen.get_rect().top + (WALL_HEIGHT * 2),
            self.screen.get_rect().bottom,
            BALL_SIZE * 2,
        )

        self.rect.centerx = self.screen.get_rect().centerx
        self.rect.centery = y
        pygame.event.post(pygame.event.Event(Event.START.value))

    def reset_velocity(self) -> None:
        """Reinicia o vetor velocidade da bola"""
        degrees = random.uniform(-BALL_MAX_ANGLE, BALL_MAX_ANGLE)

        if random.choice([-1, 1]) == -1:
            degrees += 180

        self.velocity = self.configure_velocity(degrees)
        self.acceleration = BALL_ACCELERATION

    def stroke(self, collision_point: float, side: Side) -> None:
        """Gerencia a rebatida da bola"""
        degrees = BALL_MAX_ANGLE * (collision_point / (PADDLE_HEIGHT / 2))

        if side == Side.RIGHT:
            degrees *= -1

        if self.velocity.x < 0:
            degrees += 180

        vector2 = self.configure_velocity(degrees) * self.acceleration

        if vector2.magnitude_squared() <= BALL_MAX_SPEED_SQUARED:
            self.velocity = vector2
            self.acceleration += BALL_ACCELERATION_INCREMENT
        else:
            self.velocity = vector2

    def configure_velocity(self, degrees: float) -> pygame.Vector2:
        """Configura o vetor velocidade da bola"""
        radians = math.radians(degrees)
        dx = BALL_SPEED * math.cos(radians)
        dy = BALL_SPEED * math.sin(radians)
        velocity = pygame.Vector2(dx, dy)

        return velocity
