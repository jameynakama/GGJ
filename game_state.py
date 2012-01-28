import pygame, Box2D
import math
from common import *

class GameState(object):

  current = None

  def __init__(self):
    self.scroll = vec(0,0)
    self.zoom = 20

  def update(self):
    pass

  def draw(self):
    pass

  def toScreen(self, v):
    p = v*self.zoom - self.scroll
    return (int(p.x), int(p.y))

# just a shortcut to get the current state (in our case it's always PlayState, until we make a MenuState or something)
def state():
  return GameState.current

class PlayState(GameState):

  def __init__(self):
    super(PlayState, self).__init__()
    self.scroll = vec(-400,-400)

    self.clods = pygame.sprite.RenderClear()
    self.dragons = pygame.sprite.RenderClear()

  def update(self):
    self.clods.update()
    self.dragons.update()

  def draw(self):
    pass

