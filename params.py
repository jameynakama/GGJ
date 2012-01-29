
from common import *

class game:
  debug_draw = True
  max_distance = 100
  px_scale = 20

class home:
  initial_mass = 200
  min_mass = 10
  gravitational_constant = 1.0 # raise it to strengthen gravity
  collision_category = 0x0001

class clod:
  collision_category = 0x0002

class snake:
  radius = 64
  
class dragon:
  length = 2.0
  height = 0.5
  spawn_distance = 15
  collision_category = 0x0004

  order = ('head', 'torso', 'mid', 'base', 'tail1', 'tail2', 'tail3')
  # rects = {
  #   'head': (317, 277),
  #   'base': (293, 157),
  #   'mid': (448, 215),
  #   'tail1': (237, 96),
  #   'tail2': (282, 108),
  #   'tail3': (315, 69),
  #   'torso': (416, 310)
  # }
  x = 4
  joint_attachments = {
    'head': (None, (178/x,175/x)),
    'torso': ((383/x,86/x), (124/x,114/x)),
    'mid': ((424/x,93/x), (165/x,84/x)),  
    'base': ((255/x,61/x), (95/x,62/x)),
    'tail1': ((187/x,64/x), (31/x,54/x)),
    'tail2': ((236/x,34/x), (47/x,78/x)),
    'tail3': ((306/x,17/x), (None))
  }
  ja = joint_attachments
  jo = [vec(0,0)]
  for i in range(0, len(ja)-1):
    v = vec(ja[order[i]][1]) - vec(ja[order[i+1]][0])
    jo.append( v / game.px_scale )
  joint_offsets = jo
  print jo





