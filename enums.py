#!/usr/bin/env python3

from enum import Enum
from rpi_ws281x import Color as Col

class Color(Enum):
    BLANK = Col(0,0,0)
    RED = Col(255,0,0)
    YELLOW = Col(255, 255, 0)
    GREEN = Col(0, 255, 0)
    CYAN = Col(0, 255, 255)
    BLUE = Col(0, 0, 255)
    MAGENTA = Col(255, 0, 255)
    WHITE = Col(255, 255, 255)

class Status(Enum):
    GOOD = "GOOD"
    BAD = "BAD"
    NEUTRAL = "NEUTRAL"
    FUTURE = "FUTURE"