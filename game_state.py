import pygame, Box2D
import math
from common import *

class GameState(object):

  current = None

  def __init__(self):
    self.scroll = vec(0,0)
    # self.zoom = 1.0

  def update(self):
    pass

  def draw(self):
    pass

  def toScreen(self, v):
    p = v - self.scroll
    return (int(p.x), int(p.y))


class PlayState(GameState):

  def __init__(self):
    super(PlayState, self).__init__()
    self.scroll = vec(-400,-400)
    # self.zoom = 1.0

  def update(self):
    pass

  def draw(self):
    pass


