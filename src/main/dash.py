# dash.py

import pygame


class Dash(pygame.sprite.Sprite):
    """Define uma instância de um traço do traçado central"""

    def __init__(self, screen: pygame.surface.Surface, settings: dict) -> None:
        """Inicializa uma instância de um traço do traçado central"""
        super().__init__()
        self.settings = settings
        self._layer = 1
        self.screen = screen
        self.image = pygame.surface.Surface((self.settings["dash.size"], self.settings["dash.size"]))
        self.image.fill(pygame.color.THECOLORS[self.settings["dash.color"]])
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen.get_rect().centerx
