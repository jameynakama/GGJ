import os, math
import pygame, Box2D
from Box2D import *
import params

FPS = 60

vec = b2Vec2

def toScreen(v):
  import game_state
  return game_state.GameState.current.toScreen(v)

vec = b2Vec2

def polar_vec(r, t):
  return vec(r*math.cos(t), r*math.sin(t))

class Media():

  media = None

  def __init__(self):
    #Load all media needed(images, animations, sounds, etc)
    self.test = load_img('test.png') 
    self.dragon = None
    self.cannon = load_img('cannon.png')
  
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
  return image


import physics
from physics import world