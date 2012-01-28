import pygame, Box2D
import math
import entropy
from game_state import GameState
from common import *

class Unit(object):

  @property
  def screenCoords(self):
    p = self.pos - GameState.current.scroll
    return (int(p.x), int(p.y))

class Home(pygame.sprite.Sprite, Unit):

  class Ent(pygame.sprite.Sprite):
    def __init__(self):
      super(Ent, self).__init__()

      #Angle in relation to Home
      self.position = 0.0
      self.firing = False

    def update(self):
      if self.firing == True:
        print 'Firing!'

  def __init__(self):
    super(Home, self).__init__()
    self.angle = 0.0
    self.mass = 10000
    screen = pygame.display.get_surface()
    self.rect = None
    self.pos = vec(0,0)

  @property
  def radius(self):
    return math.sqrt(float(self.mass)/math.pi)

  def update(self):
    pass

  def draw(self, screen):

    pygame.draw.circle(screen, [255,255,0], self.screenCoords, int(self.radius), 0)


class Dragon(pygame.sprite.Sprite):
  def __init__(self):
    super(Dragon, self).__init__()
    self.position = [0, 0]
    self.action = 'seeking'
    # seeking or linked
  
  def update(self):
    pass
  
  def seek_partner(self):
    pass

