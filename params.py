from Box2D import b2Vec2
vec = b2Vec2
print vec

class home:
  initial_mass = 100
  min_mass = 10
  gravitational_constant = 1.0 # raise it to strengthen gravity
  collision_category = 0x0001

class clod:
  collision_category = 0x0002

class dragon:
  length = 2.0
  height = 0.5
  spawn_distance = 10
  collision_category = 0x0004