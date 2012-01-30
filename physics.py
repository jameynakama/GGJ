
from Box2D import *
from debugdraw import *
from common import *
import params
from game_state import *
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
b2draw.SetFlags(b2draw.e_shapeBit | b2draw.e_jointBit)
if(params.game.debug_draw):
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
	shapeDef.density = params.clod.density
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

def snake_body(pos, vel):
	bodyDef = b2BodyDef()
	bodyDef.position = pos
	
	shapeDef = b2CircleDef()
	shapeDef.radius = params.snake.radius
	shapeDef.density = params.snake.density
	shapeDef.restitution = 0
	shapeDef.friction = 1

	filter = b2FilterData()
	filter.categoryBits = params.dragon.collision_category
	filter.maskBits = 0xffff - params.dragon.collision_category - params.home.collision_category

	body = world.CreateBody(bodyDef)
	shape = body.CreateShape(shapeDef)
	shape.SetFilterData(filter)
	body.SetMassFromShapes()
	body.SetLinearVelocity(vel)
	return body, shape

def dragon_body(pos, vel):
	N = 7
	# size = params.dragon.rects
	order = params.dragon.order
	joint_pos = params.dragon.joint_offsets
	bodyDef = b2BodyDef()
	
	jointDef = b2RevoluteJointDef()

	shapeDef = b2PolygonDef()
	shapeDef.density = 1
	shapeDef.restitution = 0
	shapeDef.friction = 1

	filter = b2FilterData()
	filter.categoryBits = params.dragon.collision_category
	filter.maskBits = 0xffff - params.dragon.collision_category

	def get_img(i):
		return Media.media.dragon[params.dragon.order[i]]

	def make_body(i, pos):
		img = get_img(i)
		sz = vec(img.get_size()) / state().zoom
		# offset = params.dragon.joint_attachments[params.dragon.order[i]]
		# offset = vec(1,1)

		offset = joint_pos[i]
		offset.y = offset.y
		if(i==0): 
			p = pos
		else:  
			p = tail[i-1].GetPosition()
			# offset += (sz/2 - vec(get_img(i-1).get_size())/2) / 20
		bodyDef.position = p + offset
		print "p, bdp", p, bodyDef.position
		shapeDef.SetAsBox(sz.x/2, sz.y/2)
		b = world.CreateBody(bodyDef)
		s = b.CreateShape(shapeDef)
		s.SetFilterData(filter)
		b.SetMassFromShapes()
		return b, s
	
	def make_joint(i):
		jp = joint_pos[i]
		jointDef.Initialize(tail[i], tail[i+1], jp )
		j = world.CreateJoint(jointDef)
		return j
		
	tail = []
	shapes = []
	head, s = make_body(0, pos)
	tail.append(head)
	shapes.append(s)
	for i in range(0, N-2):
		b, s = make_body(i+1, pos)
		tail.append(b)
		shapes.append(s)
		# make_joint(i)
	return tail, shapes





