import pygame, Box2D
import math
from common import *
from game_state import GameState, state

class Unit(pygame.sprite.Sprite, object):

  def __init__(self):
    super(Unit, self).__init__()

  @property
  def screenCoords(self):
    return GameState.current.toScreen(self.pos)

class Home(Unit):

  class Ent(Unit):
    def __init__(self, home):
      super(Home.Ent, self).__init__()

      self.home = home
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
      self.shot_cool -= 1
      pass

    def draw(self):
      pass

    def shoot(self, vel):
      Clod(self.pos, vel, 0.5)

  def __init__(self):
    super(Home, self).__init__()

    self.ent = Home.Ent(self)
    self.angle = 0.0
    self.angle_delta = 0.05
    self.mass = 100

    screen = pygame.display.get_surface()
    self.rect = None
    self.pos = vec(0,0)
    self.body = physics.home_body(self.radius)
  

  instance = None

  @property
  def radius(self):
    return Home.mass_to_radius(self.mass)

  @staticmethod
  def mass_to_radius(mass):
    return math.sqrt(float(mass)/math.pi)

  def update(self):
    ent.update()
    pass

  def draw(self, screen):
    self.ent.draw()
    pygame.draw.circle(screen, [255,255,0], self.screenCoords, int(self.radius), 0)
    pass

  def event(self, key):
    if key[pygame.K_SPACE]:
      if self.ent.shot_cool < 0:
        #fire a clod
        pass
    elif key[ord('w')]:
      self.mass -= 100
      print self.mass, self.radius
    elif key[ord('a')]:
      print 'a event called'
      self.angle -= self.angle_delta 
      self.pos = self.pos + vec(-1,0)
    elif key[ord('d')]:
      print 'd event called'
      self.angle += self.angle_delta
      self.pos = self.pos + vec(1,0)
    

class Clod(Unit):

  def __init__(self, pos, vel, mass):
    super(Clod, self).__init__()
    self.mass = mass
    self.radius = Home.mass_to_radius(mass)
    self.body = physics.clod_body(self.radius, pos, vel, mass)
    state().clods.add(self)
    Home.instance.mass -= mass

  @property
  def pos(self):
    return self.body.GetPosition()

  def update(self):
    grav = -self.pos
    len = grav.Normalize()
    grav *= 0.5 * Home.instance.mass / (len*len)
    self.body.ApplyForce(grav, self.pos)


class Dragon(Unit):
  def __init__(self):
    super(Dragon, self).__init__()
    self.position = [0, 0]
    self.action = 'seeking'
    # seeking or linked
  
  def update(self):
    pass
  
  def seek_partner(self):
    pass

