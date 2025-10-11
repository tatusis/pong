# event.py

import pygame
from enum import Enum


class Event(Enum):
    """Define um enumerador de eventos para o jogo"""

    START = pygame.USEREVENT + 1
    LEFT_GOAL = pygame.USEREVENT + 2
    RIGHT_GOAL = pygame.USEREVENT + 3
    WALL_COLLISION = pygame.USEREVENT + 4
