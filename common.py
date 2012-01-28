import pygame, Box2D
import math
import entropy
from game_state import *
from Box2D import *

# class vec(b2Vec2, list):
#   def tup(self):
#     return (self.x, self.y)

vec = b2Vec2

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
  return image
