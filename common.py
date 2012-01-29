import os, math
import pygame, Box2D
from Box2D import *

vec = b2Vec2

import params
import random

FPS = 60

def toScreen(v):
  import game_state
  return game_state.GameState.current.toScreen(v)


def rot_point(point, origin, angle):
  sin_t = math.sin(math.radians(angle))
  cos_t = math.cos(math.radians(angle))
  return (origin[0] + (cos_t * (point[0] - origin[0]) - sin_t * (point[1] - origin[1])), origin[1] + (sin_t * ( point[0] - origin[0]) + cos_t * (point[1] - origin[1])) )

def rot_point_img(screen, img, point, origin, point_angle, twist_angle):
  former_center = img.get_rect().center 
  pygame.draw.circle(screen, [128, 255, 255], origin, 2, 0)

  new_center = rot_point(point, origin, point_angle)
  rotated = img = pygame.transform.rotate(img, twist_angle)
  
  #pygame.draw.circle(screen, [255, 0, 0], (int(point[0]), int(point[1])), 2, 0)
  #pygame.draw.circle(screen, [0,255, 0], (int(origin[0]),int(origin[1])), 2, 0)

  rot_rect = rotated.get_rect()
  rot_rect.center = new_center
  #screen.blit(rotated, rot_rect)
  return rot_rect

def rot_point_img_rect(screen, img, origin, point, point_angle, twist_angle):
  former_center = img.get_rect().center 

  new_p = rot_point(origin, point, point_angle)
  rotated = pygame.transform.rotate(img, twist_angle)
  
  rot_rect = rotated.get_rect()
  rot_rect.center = new_p
  #screen.blit(rotated, rot_rect)
  #pygame.draw.circle(screen, [128, 255, 128], (int(point[0]), int(point[1])), 2, 0)
  #pygame.draw.circle(screen, [0,255, 0], (int(origin[0]),int(origin[1])), 2, 0)
  return rot_rect
  #return rotated.get_rect()

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

  media = None

  def __init__(self):
    #Load all media needed(images, animations, sounds, etc)
    self.test = load_img('test.png') 

    dragon_scale = 0.25
    self.dragon = {
      'head': load_img('dragon/head.png', scale=dragon_scale) ,
      'base': load_img('dragon/base.png', scale=dragon_scale) ,
      'mid': load_img('dragon/mid.png', scale=dragon_scale) ,
      'tail1': load_img('dragon/tail-1.png', scale=dragon_scale) ,
      'tail2': load_img('dragon/tail-2.png', scale=dragon_scale) ,
      'tail3': load_img('dragon/tail-3.png', scale=dragon_scale) ,
      'torso': load_img('dragon/torso.png', scale=dragon_scale) 
    }

    self.cannon = [load_img('cannon_back.png'), load_img('cannon.png'), load_img('cannon_front.png')]
    self.vertcannon = load_img('upminicannon.png')
    self.home = load_img('home.png')
    self.back = load_img('clouds.png')

    self.music_seqs = []
    for i in range(1, 22):
      self.music_seqs.append(pygame.mixer.Sound(os.path.join('media/music', 'music_seq_{num}.ogg'.format(num=i))))

  
'''
Returns the image surface resource only
'''
def load_img(name, colorkey = None, scale = 1.0):
  fullname = os.path.join('media', name)
  image = pygame.image.load(fullname) 
    # To speed things up, convert the images to SDL's internal format
  image = image.convert_alpha()
  if colorkey is not None:
    if colorkey == -1:
      colorkey = image.get_at((0,0))
    image.set_colorkey(colorkey, pygame.RLEACCEL)
  if scale!=1.0:
    image = pygame.transform.scale(image, (int(image.get_width()*scale), int(image.get_height()*scale)))
  return image

# KEEP DOWN HERE
from physics import world
