# pong.py

import pygame
from menu import Menu
from game import Game, FPS
from pygame.locals import QUIT, FULLSCREEN
from scene import Scene

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
MIXER_FREQUENCY = 44100
MIXER_SIZE = 16
MIXER_CHANNELS = 2
MIXER_BUFFER = 512


class Pong:
    """Define uma instância do jogo"""

    def __init__(self) -> None:
        """Inicializa uma instância do jogo"""
        pygame.mixer.pre_init(MIXER_FREQUENCY, MIXER_SIZE, MIXER_CHANNELS, MIXER_BUFFER)
        pygame.init()
        flags = FULLSCREEN
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
        pygame.mouse.set_visible(False)
        pygame.event.set_allowed([QUIT])
        self.change_scene(Scene.MENU)
        self.clock = pygame.time.Clock()

    def change_scene(self, scene_name: Scene) -> None:
        """Troca a cena ativa"""
        self.scene_name = scene_name

        if self.scene_name == Scene.MENU:
            self.scene = Menu(self.screen)
        elif self.scene_name == Scene.GAME:
            self.scene = Game(self.screen)

    def run(self) -> None:
        """Executa uma instância do jogo"""
        while self.scene.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.scene.process_events()
            self.scene.process_logic(dt)
            self.scene.process_frames()

            if self.scene.next_scene_name != self.scene_name:
                scene_name = self.scene.next_scene_name
                self.scene.next_scene_name = self.scene.scene_name
                self.change_scene(scene_name)

        pygame.quit()


if __name__ == "__main__":
    Pong().run()
