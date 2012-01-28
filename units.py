import pygame, Box2D
import math, random
from common import *
from game_state import GameState, state

class Unit(pygame.sprite.Sprite, object):

  def __init__(self):
    super(Unit, self).__init__()

  def doGravity(self):
    grav = -self.pos
    len = grav.Normalize()
    grav *= params.home.gravitational_constant * Home.instance.mass / (len*len)
    self.body.ApplyForce(grav, self.pos)

  @property
  def screen_coords(self):
    return GameState.current.toScreen(self.pos)

class Home(Unit):

  class Ent(Unit):
    def __init__(self, home):
      super(Home.Ent, self).__init__()

      self.home = home
      #Cooldown for allowing the player to fire SOILORBS
      self.shot_cool = 20
      #shot_angle |[-90, 90]|
      self.shot_angle = 45.0
      self.cw = True
      
    #Returns [x,y] coordinates for the ent moving around the planet
    #Param: angle -- angle of the ent relative to the Home
    #Param: radius ---- the radius...
    @property
    def pos(self):
      rad = math.radians(self.home.angle)
      return vec(math.cos(rad)*self.home.radius, math.sin(rad)*self.home.radius)

    def update(self):
      self.shot_cool -= 1

    def draw(self, screen):
      pygame.draw.circle(screen, [255, 0, 255], self.screen_coords, 20, 0)

    def shoot(self, vel):
      if(Home.instance.mass > params.home.min_mass):
        Clod(self.pos, vel, 2.5)
      else:
        print "Home mass too small to shoot!  hah!"

    def fire(self, angle):
      speed = 10.0
      vel = vec(math.cos(math.radians(angle)) * speed, math.sin(math.radians(angle)) * speed)
      print 'firing object', vec.x, vec.y
      Clod(self.pos, vel, 0.5 )

  def __init__(self):
    super(Home, self).__init__()

    self.ent = Home.Ent(self)
    self.angle = 0.0
    self.angle_mult = 1.0
    self.angle_delta = 5.0 
    self.mass = params.home.initial_mass


    screen = pygame.display.get_surface()
    self.rect = None
    self.pos = vec(0,0)
    self.body = physics.home_body(self.radius)
    # shape.SetUserData(self)

  instance = None

  @property
  def radius(self):
    return Home.mass_to_radius(self.mass)

  @staticmethod
  def mass_to_radius(mass):
    return math.sqrt(float(mass)/math.pi)

  def update(self):
    self.ent.update()
    world.DestroyBody(self.body)
    self.body = physics.home_body(self.radius)

  def draw(self, screen):
    self.ent.draw(screen)
    pygame.draw.circle(screen, [255,255,0], self.screen_coords, int(self.radius), 0)

  def event(self, key):
    if key[pygame.K_SPACE]:
      self.ent.shot_cool -= 1
      if self.ent.shot_cool < 0:
        fireang = (self.ent.shot_angle *self.angle_mult) + self.angle
        print fireang
        self.ent.fire(fireang)
        self.ent.shot_cool = 30
    if key[ord('s')]:
      if self.ent.shot_angle < 90.0:
        self.ent.shot_angle += 0.5
      print self.ent.shot_angle
    elif key[ord('w')]:
      if self.ent.shot_angle > 0.5:
        self.ent.shot_angle -= 0.5
      print self.ent.shot_angle

    if key[ord('a')]:
      print 'a event called', self.angle
      self.angle_mult = -1.0
      self.angle = self.angle - self.angle_delta 

    elif key[ord('d')]:
      print 'd event called', self.angle
      self.angle_mult = 1.0
      self.angle = self.angle + self.angle_delta

class Clod(Unit):
  def __init__(self, pos, vel, mass):
    super(Clod, self).__init__()
    self.mass = mass
    self.radius = Home.mass_to_radius(mass)
    self.body, self.shape = physics.clod_body(self.radius, pos, vel, mass)
    self.shape.SetUserData(self)
    state().clods.add(self)
    Home.instance.mass -= mass

  def __del__(self):
    Home.instance.mass += self.mass

  @property
  def pos(self):
    return self.body.GetPosition()

  def draw(self):
    pygame.draw.circle(screen, [255,255,0], self.screen_coords, 4, 0)

  def update(self):
    self.doGravity()
    if(self.pos.Length() + self.radius < Home.instance.radius):
      world.DestroyBody(self.body)
      state().clods.remove(self)
      self.shape.ClearUserData()
      del self


class Dragon(Unit):
  def __init__(self, spawn_angle, vel=None):
    super(Dragon, self).__init__()
    state().dragons.add(self)
    if not spawn_angle:
      spawn_angle = math.pi / random.randint(1, 4)
    if not vel:
      vel = vec(random.randint(1, 4), random.randint(1,4)) 
    self.body, shape = physics.dragon_body(spawn_angle, vel)
    shape.SetUserData(self)
    self.image, self.rect = load_img('dragon.png')
    self.is_hit = False
    state().dragons.add(self)

    print "\nDragon spawned!\nangle: {init_angle}\nvelocity: {init_velocity}".format(
          init_angle = spawn_angle,
          init_velocity = vel,
          )
  
  @property
  def pos(self):
    return self.body.GetPosition()
  
  def update(self):
    self.rect.center = self.screen_coords
    # if self.is_hit:
    self.doGravity()
  
  # def seek_partner(self):
  #   pass
