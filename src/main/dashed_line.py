# dashed_line.py

import pygame
from dash import Dash, DASH_SIZE
from wall import WALL_HEIGHT


class DashedLine:
    """Define uma instância do traçado central"""

    def __init__(self, screen: pygame.surface.Surface) -> None:
        """Inicializa uma instância do traçado central"""
        self.dash_sprites: list[Dash] = []
        dashes_count = round((screen.get_rect().height - (WALL_HEIGHT * 2)) / DASH_SIZE * 2)

        for i in range(dashes_count):
            dash_sprite = Dash(screen)
            dash_sprite.rect.centery = (i + 1) * DASH_SIZE * 2
            self.dash_sprites.append(dash_sprite)

    def get(self) -> list[Dash]:
        """Retorna os traços do traçado central"""
        return self.dash_sprites
