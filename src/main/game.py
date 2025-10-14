# game.py

import pygame
from ball import Ball
from ball_state import BallState
from dashed_line import DashedLine
from event import Event
from goal import Goal
from paddle import Paddle
from scene import Scene
from side import Side
from wall import Wall


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
        self.left_goal = Goal(self.screen, Side.LEFT, self.settings)
        self.right_goal = Goal(self.screen, Side.RIGHT, self.settings)
        self.left_paddle = Paddle(self.screen, Side.LEFT, self.settings)
        self.right_paddle = Paddle(self.screen, Side.RIGHT, self.settings)
        self.ball = Ball(self.screen, self.settings)

        # Sprites group
        self.sprites = pygame.sprite.LayeredUpdates()
        self.sprites.add(self.top_wall)
        self.sprites.add(self.bottom_wall)
        self.sprites.add(self.left_goal)
        self.sprites.add(self.right_goal)
        self.sprites.add(self.left_paddle)
        self.sprites.add(self.right_paddle)
        self.sprites.add(self.ball)
        self.sprites.add(DashedLine(self.screen, self.settings).get())

        # Sounds
        self.start_sound = pygame.mixer.Sound(self.settings["start.sound"])
        self.collision_sound = pygame.mixer.Sound(self.settings["collision.sound"])
        self.collision_sound_cooldown = self.settings["collision.sound.cooldown"]
        self.score_sound = pygame.mixer.Sound(self.settings["score.sound"])
        self.winner_sound = pygame.mixer.Sound(self.settings["winner.sound"])
        self.restart_sound = pygame.mixer.Sound(self.settings["restart.sound"])

        # Channels
        self.start_channel = pygame.mixer.Channel(1)
        self.start_channel.set_volume(self.settings["sound.volume"])
        self.collision_channel = pygame.mixer.Channel(2)
        self.collision_channel.set_volume(self.settings["sound.volume"])
        self.score_channel = pygame.mixer.Channel(3)
        self.score_channel.set_volume(self.settings["sound.volume"])
        self.winner_channel = pygame.mixer.Channel(4)
        self.winner_channel.set_volume(self.settings["sound.volume"])
        self.restart_channel = pygame.mixer.Channel(5)
        self.restart_channel.set_volume(self.settings["sound.volume"])

        # Score
        self.score_font = pygame.font.Font(self.settings["font.family"], self.settings["game.score.font.size"])
        self.left_score = 0
        self.left_score_text = self.render_text(str(self.left_score), self.score_font)
        self.right_score = 0
        self.right_score_text = self.render_text(str(self.right_score), self.score_font)

        # Winner
        self.winner_font = pygame.font.Font(self.settings["font.family"], self.settings["game.winner.font.size"])
        self.winner_text = self.render_text("Winner", self.winner_font)

        # Options
        self.option_font = pygame.font.Font(self.settings["font.family"], self.settings["game.option.font.size"])
        self.restart_text = self.render_text(self.settings["submenu.restart.text"], self.option_font)
        self.exit_text = self.render_text(self.settings["submenu.exit.text"], self.option_font)

        # Paddles
        self.paddles = [self.left_paddle, self.right_paddle]
        self.paddles_rects = [self.left_paddle.rect, self.right_paddle.rect]

        # Walls
        self.walls = [self.top_wall, self.bottom_wall]
        self.walls_rects = [self.top_wall.rect, self.bottom_wall.rect]

        # Goals
        self.goals = [self.left_goal, self.right_goal]
        self.goals_rects = [self.left_goal.rect, self.right_goal.rect]

        self.accumulator = 0.0
        self.time_step = 1.0 / (self.settings["game.fps"] * 2.0)
        self.running = True
        self.winner = None

    def process_events(self) -> None:
        """Processa os eventos do jogo"""
        keys = pygame.key.get_pressed()
        self.left_paddle.update_direction(keys)
        self.right_paddle.update_direction(keys)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.handle_restart()
                elif event.key == pygame.K_ESCAPE:
                    self.next_scene_name = Scene.MENU
            elif event.type == pygame.QUIT:
                self.running = False
            elif event.type == Event.START.value:
                self.start_channel.play(self.start_sound)

    def play_collision_sound(self) -> None:
        """Reproduz o som de colisão"""
        if self.collision_sound_cooldown <= 0:
            self.collision_channel.play(self.collision_sound)
            self.collision_sound_cooldown = self.settings["collision.sound.cooldown"]

    def handle_goal(self, side: Side) -> None:
        """Gerencia a atualização do placar"""
        if side == Side.LEFT:
            self.right_score += 1
            self.right_score_text = self.render_text(str(self.right_score), self.score_font)
        elif side == Side.RIGHT:
            self.left_score += 1
            self.left_score_text = self.render_text(str(self.left_score), self.score_font)

        if self.left_score >= self.settings["game.points.max"] or self.right_score >= self.settings["game.points.max"]:
            self.handle_endgame()
        else:
            self.score_channel.play(self.score_sound)
            self.ball.state = BallState.READY

    def handle_restart(self) -> None:
        """Gerencia o reinício do jogo"""
        self.restart_channel.play(self.restart_sound)
        self.left_score = 0
        self.left_score_text = self.render_text(str(self.left_score), self.score_font)
        self.right_score = 0
        self.right_score_text = self.render_text(str(self.right_score), self.score_font)
        self.ball.state = BallState.READY
        self.winner = None

    def handle_endgame(self) -> None:
        """Gerencia o fim do jogo"""
        self.winner_channel.play(self.winner_sound)
        self.ball.state = BallState.WAITING

        if self.left_score > self.right_score:
            self.winner = Side.LEFT
        else:
            self.winner = Side.RIGHT

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

            # Colisão com os gols
            collided_goal_index = self.ball.rect.collidelist(self.goals_rects)

            if collided_goal_index != -1 and self.ball.state == BallState.RUNNING:
                collided_goal = self.goals[collided_goal_index]
                self.handle_goal(collided_goal.side)

            self.accumulator -= self.time_step

    def process_frames(self) -> None:
        """Processa os frames do jogo"""
        self.screen.fill(pygame.color.THECOLORS[self.settings["screen.color"]])

        # Left score
        left_score_rect = self.left_score_text.get_rect()
        left_score_rect.centerx = round(self.screen.get_rect().width * self.settings["screen.grid.width.03.12"])
        left_score_rect.centery = round(self.screen.get_rect().height * self.settings["screen.grid.height.02.12"])
        self.screen.blit(self.left_score_text, left_score_rect)

        # Right score
        right_score_rect = self.right_score_text.get_rect()
        right_score_rect.centerx = round(self.screen.get_rect().width * self.settings["screen.grid.width.09.12"])
        right_score_rect.centery = round(self.screen.get_rect().height * self.settings["screen.grid.height.02.12"])
        self.screen.blit(self.right_score_text, right_score_rect)

        if self.winner is not None:
            winner_rect = self.winner_text.get_rect()

            if self.winner == Side.LEFT:
                position = round(self.screen.get_rect().width * self.settings["screen.grid.width.03.12"])
            elif self.winner == Side.RIGHT:
                position = round(self.screen.get_rect().width * self.settings["screen.grid.width.09.12"])

            winner_rect.centerx = position
            winner_rect.centery = round(self.screen.get_rect().height * self.settings["screen.grid.height.07.12"])
            self.screen.blit(self.winner_text, winner_rect)

            restart_rect = self.restart_text.get_rect()
            restart_rect.centerx = position
            restart_rect.centery = round(self.screen.get_rect().height * self.settings["screen.grid.height.09.12"])
            self.screen.blit(self.restart_text, restart_rect)

            exit_rect = self.exit_text.get_rect()
            exit_rect.centerx = position
            exit_rect.centery = round(self.screen.get_rect().height * self.settings["screen.grid.height.10.12"])
            self.screen.blit(self.exit_text, exit_rect)

        self.sprites.draw(self.screen)
        pygame.display.flip()

    def render_text(self, text: str, font: pygame.font.Font) -> pygame.surface.Surface:
        """Rederiza o texto"""
        return font.render(text, True, pygame.color.THECOLORS[self.settings["font.color"]])
