import pygame, Box2D
import math
from Box2D import *
import params

class CL(Box2D.b2ContactListener):

  def Add(self, contact):
    a = contact.shape1.userData
    b = contact.shape2.userData
    dragon_str = "<class 'units.Dragon'>"
    clod_str = "<class 'units.Clod'>"
    if(str(type(a))==dragon_str and str(type(b))==clod_str):
      a.take_hit()
    elif(str(type(b))==clod_str and str(type(a))==dragon_str):
      b.take_hit()
    # print (a.GetUserData), (b.GetUserData)