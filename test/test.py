import pygame, os
import math
'''
Returns the image surface resource only
'''
def load_img(name, colorkey = None):
  fullname = os.path.join('', name)
  image = pygame.image.load(fullname) 
    # To speed things up, convert the images to SDL's internal format
  image = image.convert_alpha()
  if colorkey is not None:
    if colorkey == -1:
      colorkey = image.get_at((0,0))
    image.set_colorkey(colorkey, pygame.RLEACCEL)
  return image, image.get_rect() 

def rot_center(image, angle):
  orig_rect = image.get_rect()
  center = orig_rect.center
  


  rot_image = pygame.transform.rotate(image, angle)
  rot_rect = rot_image.get_rect(center = center)
  return rot_image
"""
def point(point, origin, angle):
  sin_t = math.sin(math.radians(angle))
  cos_t = math.cos(math.radians(angle))
  return [origin.x + (cos_t * (point.x - origin.x) - sin_t * (point.y - origin.y)), origin.y + (sin_t * ( point.x - origin.x) + cos_t * (self.y - origin.y)) ]
"""

def rot_point(point, origin, angle):
  sin_t = math.sin(math.radians(angle))
  cos_t = math.cos(math.radians(angle))
  return (origin[0] + (cos_t * (point[0] - origin[0]) - sin_t * (point[1] - origin[1])), origin[1] + (sin_t * ( point[0] - origin[0]) + cos_t * (point[1] - origin[1])) )

def rot_point_img_rect(img, origin, point, point_angle, twist_angle):
  former_center = img.get_rect().center 

  new_center = rot_point(origin, point, point_angle)
  rotated = pygame.transform.rotate(img, twist_angle)
  
  rot_rect = rotated.get_rect()
  rot_rect.center = new_center
  screen.blit(rotated, rot_rect)
  pygame.draw.circle(screen, [128, 255, 128], point, 2, 0)
  pygame.draw.circle(screen, [128, 255, 255], origin, 2, 0)
  return rot_rect

def angle_to(origin, point):  
  return math.degrees(math.atan2(origin[0]-point[0], origin[1]-point[1]))

pygame.init()
#create a surface that will be seen by the user
screen =  pygame.display.set_mode((400, 400))
img, imgrect= load_img('test.png', -1) 
imgrect.center = [100, 100]
print 'CENTER:', imgrect.center

#create a varible for degrees pf rotation
degree = 0
while True:
  #clear screen at the start of every frame
  screen.fill((40, 40, 40))
  #create new surface with white BG
  surf =  pygame.Surface((100, 100))
  surf.fill((255, 128, 255))
  #set a color key for blitting
  surf.set_colorkey((255, 0, 0))


  where = [200.0, 200.0]
  point = [80, 120]
  origin =[80, 80]
  imgrect = rot_point_img_rect(img, origin, point, degree, angle_to(imgrect.center, point))
  print degree, angle_to(imgrect.center, point)
  
  """
  #get the rect of the rotated surf and set it's center to the oldCenter
  rotRect = rotatedSurf.get_rect()
  #rotRect.center = oldCenter
  rotRect.center = where
  #draw rotatedSurf with the corrected rect so it gets put in the proper spot
  screen.blit(rotatedSurf, rotRect)
  """
  #change the degree of rotation
  degree += 5
  if degree >= 360:
      degree = 0

  #show the screen surface
  pygame.display.flip()

  #wait 60 ms until loop restart
  pygame.time.wait(60)

