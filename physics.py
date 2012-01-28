
from Box2D import *
from debugdraw import *
from common import polar_vec
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
# world.SetContactListener(contact_listener.CL())

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
	filter.maskBits = 0xffff - filter.categoryBits

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
	filter.maskBits = 0xffff - filter.categoryBits

	body = world.CreateBody(bodyDef)
	shape = body.CreateShape(shapeDef)
	shape.SetFilterData(filter)
	body.SetMassFromShapes()
	body.SetLinearVelocity(vel)
	return body

def dragon_body(r, t):
	bodyDef = b2BodyDef()
	bodyDef.position = polar_vec(r,t)
	
	shapeDef = b2PolygonDef()
	shapeDef.SetAsBox(params.dragon.length, params.dragon.height)
	shapeDef.density = 1
	shapeDef.restitution = 0
	shapeDef.friction = 1

	filter = b2FilterData()

	body = world.CreateBody(bodyDef)
	shape = body.CreateShape(shapeDef)
	shape.SetFilterData(filter)
	body.SetMassFromShapes()
	return body

