# event.py

from enum import Enum

import pygame


class Event(Enum):
    """Define um enumerador de eventos para o jogo"""

    START = pygame.USEREVENT + 1
