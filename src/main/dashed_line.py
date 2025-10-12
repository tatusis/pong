# dashed_line.py

import pygame
from dash import Dash


class DashedLine:
    """Define uma instância do traçado central"""

    def __init__(self, screen: pygame.surface.Surface, settings: dict) -> None:
        """Inicializa uma instância do traçado central"""
        self.settings = settings
        self.dash_sprites: list[Dash] = []
        dashes_count = round(
            (screen.get_rect().height - (self.settings["wall.size"] * 2)) / self.settings["dash.size"] * 2
        )

        for i in range(dashes_count):
            dash_sprite = Dash(screen, self.settings)
            dash_sprite.rect.centery = (i + 1) * self.settings["dash.size"] * 2
            self.dash_sprites.append(dash_sprite)

    def get(self) -> list[Dash]:
        """Retorna os traços do traçado central"""
        return self.dash_sprites
