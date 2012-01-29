import os, math
import pygame, Box2D
from Box2D import *
import params

vec = b2Vec2
FPS = 60
def toScreen(v):
  import game_state
  return game_state.GameState.current.toScreen(v)

vec = b2Vec2

def polar_vec(r, t):
  return vec(r*math.cos(t), r*math.sin(t))

def rotate_img(img, angle):
  rotate = pygame.transform.rotate
  dup = img
  img = rotate(dup, angle)
  return img, img.get_rect()

def rot_center(image, angle):
  former_center = image.get_rect().center
  rot_image = pygame.transform.rotate(image, angle)
  rot_rect = rot_image.get_rect()
  rot_rect.center = former_center

  return rot_image
  
class Media():
  def __init__(self):
    #Load all media needed(images, animations, sounds, etc)
    self.test = load_img('test.png') 
  
'''
Returns the image surface resource only
'''
def load_img(name, colorkey = None):
  fullname = os.path.join('media', name)
  image = pygame.image.load(fullname) 
    # To speed things up, convert the images to SDL's internal format
  image = image.convert_alpha()
  if colorkey is not None:
    if colorkey == -1:
      colorkey = image.get_at((0,0))
    image.set_colorkey(colorkey, pygame.RLEACCEL)
  return image, image.get_rect()


import physics
from physics import world