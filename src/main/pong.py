# pong.py

import json

import pygame
from game import Game
from menu import Menu
from pygame.locals import FULLSCREEN, QUIT
from scene import Scene


class Pong:
    """Define uma instância do jogo"""

    def __init__(self) -> None:
        """Inicializa uma instância do jogo"""
        with open("config/settings.json", "r") as file:
            self.settings = json.load(file)

        pygame.mixer.pre_init(
            self.settings["mixer.frequency"],
            self.settings["mixer.size"],
            self.settings["mixer.channels"],
            self.settings["mixer.buffer"],
        )
        pygame.init()
        flags = FULLSCREEN
        self.screen = pygame.display.set_mode((self.settings["screen.width"], self.settings["screen.height"]), flags)
        pygame.mouse.set_visible(False)
        pygame.event.set_allowed([QUIT])
        self.change_scene(Scene.MENU)
        self.clock = pygame.time.Clock()

    def change_scene(self, scene_name: Scene) -> None:
        """Troca a cena ativa"""
        self.scene_name = scene_name

        if self.scene_name == Scene.MENU:
            self.scene = Menu(self.screen, self.settings)
        elif self.scene_name == Scene.GAME:
            self.scene = Game(self.screen, self.settings)

    def run(self) -> None:
        """Executa uma instância do jogo"""
        while self.scene.running:
            dt = self.clock.tick(self.settings["game.fps"]) / 1000.0
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
