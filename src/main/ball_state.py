# ball_state.py

from enum import Enum


class BallState(Enum):
    """Define um enumerador de estados para a bola"""

    WAITING = 0
    RUNNING = 1
    READY = 2
