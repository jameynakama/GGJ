import pygame, Box2D
import math
from Box2D import *

vec = b2Vec2

import physics
from physics import world

def toScreen(v):
  import game_state
  return game_state.GameState.current.toScreen(v)

# class vec(b2Vec2, list):
#   def tup(self):
#     return (self.x, self.y)

