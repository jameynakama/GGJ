import pygame, Box2D
import math
from common import *
from game_state import GameState

class Unit(object):

  @property
  def screenCoords(self):
    return GameState.current.toScreen(self.pos)

class Home(pygame.sprite.Sprite, Unit):

  class Ent(pygame.sprite.Sprite, home):
    def __init__(self):
      super(Ent, self).__init__()
      self.home = home
      #Cooldown for allowing the player to move
      self.move_cool = 5
      #Cooldown for allowing the player to fire SOILORBS
      self.shot_cool = 20
      
    #Returns [x,y] coordinates for the ent moving around the planet
    #Param: angle -- angle of the ent relative to the Home
    #Param: radius ---- the radius...
    @property
    def pos(self):
      rad = math.radians(self.home.angle)
      return vec(math.cos(rad)*self.home.radius, math.sin(rad)*self.home.radius)

    def update(self):
      self.move_cool -= 1
      self.shot_cool -= 1
      pass
    def draw(self):
      pass

  def __init__(self):
    super(Home, self).__init__()
    ent = Ent(self)
    self.angle = 0.0
    self.mass = 10000
    screen = pygame.display.get_surface()
    self.rect = None
    self.pos = vec(0,0)
    self.body = physics.home_body(self.radius)

  @property
  def radius(self):
    return math.sqrt(float(self.mass)/math.pi)

  def update(self):
    ent.update()
    pass

  def draw(self, screen):
    ent.draw()
    # pygame.draw.circle(screen, [255,255,0], self.screenCoords, int(self.radius), 0)
    pass

class Clod(pygame.sprite.Sprite, Unit):
  def __init__(self, pos, vel, mass):
    super(Clod, self).__init__()
    self.mass = mass
    self.radius = 1
    self.body = Game.world.CreateDynamicBody(
        position=pos,
        fixtures=b2FixtureDef(
           shape=b2CircleShape(radius=self.radius),
           density=0.5,
           restitution=0,
           friction=0.5
           ),
        damping=0
        )
    print dir(self.body)


class Dragon(pygame.sprite.Sprite, Unit):
  def __init__(self):
    super(Dragon, self).__init__()
    self.position = [0, 0]
    self.action = 'seeking'
    # seeking or linked
  
  def update(self):
    pass
  
  def seek_partner(self):
    pass

