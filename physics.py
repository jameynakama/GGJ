
from Box2D import *
from debugdraw import *
### BOX2D STUFF ###
worldAABB=b2AABB()
worldAABB.lowerBound = (-100, -100)
worldAABB.upperBound = ( 100,  100)
gravity = b2Vec2(0, 0)
doSleep = False

world = b2World(worldAABB, gravity, doSleep)
timeStep = 1.0 / 60
vel_iters, pos_iters = 10, 8

b2draw = DebugDraw()
b2draw.SetFlags(b2draw.e_shapeBit)
b2draw.viewZoom = 1.
b2draw.viewCenter = b2Vec2(0,0)
b2draw.viewOffset = b2Vec2(-200,50)
world.SetDebugDraw(b2draw)

def worldStep():
	global world
	world.Step(timeStep, vel_iters, pos_iters)

def home_body(radius):
	bodyDef = b2BodyDef()
	bodyDef.position = (0, 0)
	
	shapeDef = b2CircleDef()
	shapeDef.radius = radius
	shapeDef.density = 1
	shapeDef.restitution = 0
	shapeDef.friction = 1

	body = world.CreateBody(bodyDef)
	body.CreateShape(shapeDef)
	return body