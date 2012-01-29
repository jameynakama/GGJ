import pygame, Box2D
import math
from common import *
import entropy
from game_state import GameState, state

class Unit(pygame.sprite.Sprite, object):

  def __init__(self):
    super(Unit, self).__init__()

  def doGravity(self):
    grav = -self.pos
    len = grav.Normalize()
    grav *= params.home.gravitational_constant * Home.instance.mass / (len*len)
    self.body.ApplyForce(grav, self.pos)
  
  def draw(self, screen):
    super(Unit, self).draw(screen)

  @property
  def screen_coords(self):
    return GameState.current.toScreen(self.pos)

class Home(Unit):

  class Ent(Unit):

    image = None

    def __init__(self, home):
      super(Home.Ent, self).__init__()

      self.home = home
      #Cooldown for allowing the player to fire SOILORBS
      self.shot_cool = 20
      #shot_angle |[-90, 90]|
      self.shot_angle = 0.0
      self.start_angle = 0.0
      self.cw = True
      

      Home.Ent.image = self.image = Media.media.cannon[1]
      self.c_front = Media.media.cannon[2]
      self.rect = self.image.get_rect()

      state().cannon_group.add(self)
      
    #Returns [x,y] coordinates for the ent moving around the planet
    #Param: angle -- angle of the ent relative to the Home
    #Param: radius ---- the radius...
    @property
    def pos(self):
      rad = math.radians(self.home.angle)
      return vec(math.cos(rad)*self.home.radius, math.sin(rad)*self.home.radius)

    def update(self):
      self.shot_cool -= 1
    
    def angle_point(self, radius):
       return (400 + int(math.cos(math.radians(self.home.angle))*radius),400 + int(math.sin(math.radians(self.home.angle))*radius))

    def angle_to(self, origin, point):  
      return math.degrees(math.atan2(origin[0]-point[0], origin[1]-point[1]))
        
    @property 
    def cannon_origin(self):
      return (math.cos(math.radians(self.home.angle)), math.sin(math.radians(self.home.angle)))

    def draw(self, screen):
      self.c_back = Media.media.cannon[0] 
      self.c_back = rot_center(self.c_back, -self.home.angle) 
      self.cb = self.c_back.get_rect()
      self.cb.center = self.screen_coords
      #screen.blit(self.c_back, self.cb)


      #pygame.draw.circle(screen, [255, 0, 255], self.screen_coords, 20, 0)
      self.rect = self.image.get_rect()
      self.rect.move_ip(self.screen_coords)

      mutate_pt = self.angle_point(60)
      self.image = pygame.transform.rotozoom(Home.Ent.image, -self.home.angle+(self.shot_angle*-self.home.angle_mult), 1.0)
      ang = -self.home.angle+(self.shot_angle*-self.home.angle_mult)
      self.rect = rot_point_img_rect(screen, Home.Ent.image, self.screen_coords, (400, 400), 0 , ang  )

      #print self.screen_coords, mutate_pt, self.angle_to(mutate_pt, self.screen_coords)
      #pygame.draw.circle(screen, (0,64,255), mutate_pt,  4, 0)

      self.c_front = Media.media.cannon[2]
      self.c_front = rot_center(self.c_front, -self.home.angle)
      self.cf = self.c_front.get_rect()
      self.cf.center = self.screen_coords
      screen.blit(self.c_front, self.cf)


      #super(Home.Ent, self).draw(screen)

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
    self.maxmass = 100.0


    screen = pygame.display.get_surface()
    self.image = Media.media.home
    self.rect = self.image.get_rect()
    self.bg = Media.media.back
    self.bgr = self.bg.get_rect() 
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


    scale = int(170 + 80*(self.mass / self.maxmass))
    self.image = pygame.transform.smoothscale(self.image, [scale, scale])
    self.rect = self.image.get_rect()
    self.rect.center = [400,400]
    screen.blit(self.image, self.rect)
    self.ent.draw(screen)

    #pygame.draw.circle(screen, [255,255,0], self.screen_coords, int(self.radius), 0)

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
        self.ent.shot_angle += 1.0
      print self.ent.shot_angle
    elif key[ord('w')]:
      if self.ent.shot_angle > 0.5:
        self.ent.shot_angle -= 1.0
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
  def __init__(self, image):
    super(Dragon, self).__init__()
    state().dragons.add(self)

    spawn_angle = math.pi * random.uniform(0, 2)
    speed = -random.uniform(1, 2)

    vel = polar_vec(speed, spawn_angle / random.uniform(-0.5, 0.5))

    self.body, shape = physics.dragon_body(spawn_angle, vel)
    for s in shape: s.SetUserData(self)

    self.image = image
    self.rect = self.image.get_rect()
    self.is_hit = False
    state().dragons.add(self)

    print "\nDragon spawned!\nangle: {init_angle}\nvelocity: {init_velocity}".format(
          init_angle = spawn_angle,
          init_velocity = vel,
          )

  def take_hit(self):
    self.is_hit = True
    self.body.SetLinearVelocity(self.body.GetLinearVelocity() * 0.2)

  @property
  def pos(self):
    return self.body.GetPosition()
  
  def update(self):
    self.rect.center = self.screen_coords
    if self.is_hit:
      self.doGravity()
  
  def seek_partner(self):
    pass
