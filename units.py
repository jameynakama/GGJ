import pygame, Box2D
import math
import entropy


class Home(pygame.sprite.Sprite):
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
    self.mass = 100
    screen = pygame.display.get_surface()
    self.rect = None
    self.pos = [400,400]

  @property
  def radius(self):
    return math.sqrt(float(self.mass)/math.pi)

  def update(self):
    pass    