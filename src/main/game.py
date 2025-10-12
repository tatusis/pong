# game.py

import pygame
from paddle import Paddle
from ball import Ball
from side import Side
from event import Event
from wall import Wall
from dashed_line import DashedLine
from scene import Scene


class Game:
    """Define uma sessão do jogo"""

    def __init__(self, screen: pygame.surface.Surface, settings: dict) -> None:
        """Inicializa uma sessão do jogo"""
        self.settings = settings
        self.scene_name = Scene.GAME
        self.next_scene_name = Scene.GAME
        self.screen = screen

        # Sprites
        self.top_wall = Wall(self.screen, Side.TOP, self.settings)
        self.bottom_wall = Wall(self.screen, Side.BOTTOM, self.settings)
        self.left_paddle = Paddle(self.screen, Side.LEFT, self.settings)
        self.right_paddle = Paddle(self.screen, Side.RIGHT, self.settings)
        self.ball = Ball(self.screen, self.settings)

        # Sprites group
        self.sprites = pygame.sprite.LayeredUpdates()
        self.sprites.add(self.top_wall)
        self.sprites.add(self.bottom_wall)
        self.sprites.add(self.left_paddle)
        self.sprites.add(self.right_paddle)
        self.sprites.add(self.ball)
        self.sprites.add(DashedLine(self.screen, self.settings).get())

        # Sounds
        self.start_sound = pygame.mixer.Sound(self.settings["start.sound"])
        self.start_sound.set_volume(0.2)
        self.collision_sound = pygame.mixer.Sound(self.settings["collision.sound"])
        self.collision_sound.set_volume(0.2)
        self.collision_sound_cooldown = self.settings["collision.sound.cooldown"]
        self.score_sound = pygame.mixer.Sound(self.settings["score.sound"])
        self.score_sound.set_volume(0.2)

        # Channels
        self.start_channel = pygame.mixer.Channel(0)
        self.collision_channel = pygame.mixer.Channel(1)
        self.score_channel = pygame.mixer.Channel(2)

        # Score text
        self.score_font = pygame.font.Font(self.settings["font.family"], self.settings["game.score.font.size"])
        self.left_score = 0
        self.left_score_text = self.render_score_text(str(self.left_score))
        self.right_score = 0
        self.right_score_text = self.render_score_text(str(self.right_score))

        # Paddles
        self.paddles = [self.left_paddle, self.right_paddle]
        self.paddles_rects = [self.left_paddle.rect, self.right_paddle.rect]

        # Walls
        self.walls = [self.top_wall, self.bottom_wall]
        self.walls_rects = [self.top_wall.rect, self.bottom_wall.rect]

        self.accumulator = 0.0
        self.time_step = 1.0 / (self.settings["game.fps"] * 2.0)
        self.running = True

    def process_events(self) -> None:
        """Processa os eventos do jogo"""
        keys = pygame.key.get_pressed()
        self.left_paddle.update_direction(keys)
        self.right_paddle.update_direction(keys)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_scene_name = Scene.MENU
            elif event.type == pygame.QUIT:
                self.running = False
            elif event.type == Event.START.value:
                self.start_channel.play(self.start_sound)
            elif event.type == Event.LEFT_GOAL.value:
                self.handle_goal(Side.LEFT)
            elif event.type == Event.RIGHT_GOAL.value:
                self.handle_goal(Side.RIGHT)
            elif event.type == Event.WALL_COLLISION.value:
                self.play_collision_sound()

    def play_collision_sound(self) -> None:
        """Reproduz o som de colisão"""
        if self.collision_sound_cooldown <= 0:
            self.collision_channel.play(self.collision_sound)
            self.collision_sound_cooldown = self.settings["collision.sound.cooldown"]

    def handle_goal(self, side: Side) -> None:
        """Gerencia a atualização do placar"""
        self.score_channel.play(self.score_sound)

        if side == Side.LEFT:
            self.right_score += 1
            self.right_score_text = self.render_score_text(str(self.right_score))
        elif side == Side.RIGHT:
            self.left_score += 1
            self.left_score_text = self.render_score_text(str(self.left_score))

    def process_logic(self, dt: float) -> None:
        """Processa a lógica do jogo"""
        self.accumulator += dt

        if self.collision_sound_cooldown > 0:
            self.collision_sound_cooldown -= dt

        while self.accumulator >= self.time_step:
            self.sprites.update(self.time_step)

            # Colisão com as raquetes
            collided_paddle_index = self.ball.rect.collidelist(self.paddles_rects)

            if collided_paddle_index != -1:
                collided_paddle = self.paddles[collided_paddle_index]

                if (self.ball.velocity.x > 0 and collided_paddle.side == Side.RIGHT) or (
                    self.ball.velocity.x < 0 and collided_paddle.side == Side.LEFT
                ):
                    self.play_collision_sound()
                    self.ball.velocity.x *= -1
                    self.ball.stroke(self.ball.rect.centery - collided_paddle.rect.centery, collided_paddle.side)

            # Colisão com as paredes
            collided_wall_index = self.ball.rect.collidelist(self.walls_rects)

            if collided_wall_index != -1:
                collided_wall = self.walls[collided_wall_index]

                if (self.ball.velocity.y > 0 and collided_wall.side == Side.BOTTOM) or (
                    self.ball.velocity.y < 0 and collided_wall.side == Side.TOP
                ):
                    self.play_collision_sound()
                    self.ball.velocity.y *= -1

            self.accumulator -= self.time_step

    def process_frames(self) -> None:
        """Processa os frames do jogo"""
        self.screen.fill(pygame.color.THECOLORS[self.settings["screen.color"]])

        # Left score
        left_score_rect = self.left_score_text.get_rect()
        left_score_rect.centerx = round(self.screen.get_rect().right * (4 / 12))
        left_score_rect.centery = round(self.screen.get_rect().bottom * (2 / 12))
        self.screen.blit(self.left_score_text, left_score_rect)

        # Right score
        right_score_rect = self.right_score_text.get_rect()
        right_score_rect.centerx = round(self.screen.get_rect().right * (8 / 12))
        right_score_rect.centery = round(self.screen.get_rect().bottom * (2 / 12))
        self.screen.blit(self.right_score_text, right_score_rect)

        self.sprites.draw(self.screen)
        pygame.display.flip()

    def render_score_text(self, text: str) -> pygame.surface.Surface:
        """Rederiza o texto"""
        return self.score_font.render(text, True, pygame.color.THECOLORS[self.settings["font.color"]])
