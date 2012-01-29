
from Box2D import *
from debugdraw import *
from common import *
import params

import contact_listener

### BOX2D STUFF ###
worldAABB=b2AABB()
worldAABB.lowerBound = (-1000, -1000)
worldAABB.upperBound = ( 1000,  1000)
gravity = b2Vec2(0, 0)
doSleep = False

world = b2World(worldAABB, gravity, doSleep)
timeStep = 1.0 / 60
vel_iters, pos_iters = 10, 8

b2draw = DebugDraw()
b2draw.SetFlags(b2draw.e_shapeBit)
world.SetDebugDraw(b2draw)
b2cl = contact_listener.CL()
world.SetContactListener(b2cl)

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

	filter = b2FilterData()
	filter.categoryBits = params.home.collision_category
	filter.maskBits = 0xffff - params.clod.collision_category

	body = world.CreateBody(bodyDef)
	shape = body.CreateShape(shapeDef)
	return (body)
	

def clod_body(radius, pos, vel, mass):
	bodyDef = b2BodyDef()
	bodyDef.position = pos
	
	shapeDef = b2CircleDef()
	shapeDef.radius = radius
	shapeDef.density = 1
	shapeDef.restitution = 0
	shapeDef.friction = 1

	filter = b2FilterData()
	filter.categoryBits = params.clod.collision_category
	filter.maskBits = 0xffff - params.clod.collision_category - params.home.collision_category

	body = world.CreateBody(bodyDef)
	shape = body.CreateShape(shapeDef)
	shape.SetFilterData(filter)
	body.SetMassFromShapes()
	body.SetLinearVelocity(vel)
	return body, shape

def dragon_body(spawn_angle, vel):
	N = 6
	size = (
		vec(params.dragon.length, params.dragon.height),
		vec(params.dragon.length, params.dragon.height),
		vec(params.dragon.length, params.dragon.height),
		vec(params.dragon.length, params.dragon.height),
		vec(params.dragon.length, params.dragon.height),
		vec(params.dragon.length, params.dragon.height)
	)
	joint_pos = (
		vec(0,0),
		vec(0,0),
		vec(0,0),
		vec(0,0),
		vec(0,0),
		vec(0,0)
	)
	pos = polar_vec(params.dragon.spawn_distance, spawn_angle)
	bodyDef = b2BodyDef()
	
	jointDef = b2RevoluteJointDef()

	shapeDef = b2PolygonDef()
	shapeDef.density = 1
	shapeDef.restitution = 0
	shapeDef.friction = 1

	filter = b2FilterData()

	def make_body(i, pos):

		sz = size[i]
		bodyDef.position = pos
		pos += sz
		shapeDef.SetAsBox(sz.x, sz.y)
		b = world.CreateBody(bodyDef)
		s = b.CreateShape(shapeDef)
		s.SetFilterData(filter)
		b.SetMassFromShapes()
		return b, s
	
	def make_joint(i):
		jp = joint_pos[i]
		jointDef.Initialize(tail[i], tail[i+1], vec(0,0))
		j = world.CreateJoint(jointDef)
		return j
		
	tail = []
	shapes = []
	b, s = make_body(0, pos)
	tail.append(b)
	shapes.append(s)
	for i in range(0, N-2):
		b, s = make_body(i+1, pos)
		tail.append(b)
		shapes.append(s)
		make_joint(i)
	return tail[0], shapes




# def dragon_body(spawn_angle, vel):
# 	bodyDef = b2BodyDef()
# 	bodyDef.position = polar_vec(params.dragon.spawn_distance, spawn_angle)
	
# 	shapeDef = b2PolygonDef()
# 	shapeDef.SetAsBox(params.dragon.length, params.dragon.height)
# 	shapeDef.density = 1
# 	shapeDef.restitution = 0
# 	shapeDef.friction = 1

# 	filter = b2FilterData()
# 	filter.categoryBits = params.dragon.collision_category
# 	filter.maskBits = 0xffff - params.dragon.collision_category

# 	body = world.CreateBody(bodyDef)
# 	shape = body.CreateShape(shapeDef)
# 	shape.SetFilterData(filter)
# 	body.SetMassFromShapes()
# 	body.SetLinearVelocity(vel)
# 	return body, shape


