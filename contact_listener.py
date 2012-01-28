import pygame, Box2D
import math
from Box2D import *
import params

class CL(Box2D.b2ContactListener):

  def Add(self, contact):
    a = contact.shape1
    b = contact.shape2
    # print a, b