import pygame, Box2D
import math
from Box2D import *
import params

class CL(Box2D.b2ContactListener):

  def Add(self, contact):
    print contact