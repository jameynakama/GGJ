import os, sys, pygame
from Box2D import *
from pygame.locals import *
from debugdraw import DebugDraw
import units
from game_state import *

class Game:
  def __init__(self):
    pygame.init()

    self.screen_size = [800, 800]

    self.screen = pygame.display.set_mode(self.screen_size)
    self.clock = pygame.time.Clock()
    pygame.display.set_caption('Entropy')

    self.backgd = pygame.Surface(self.screen.get_size())
    back_color = [128,128,128]

    self.frames = 0
    self.show = pygame.sprite.RenderClear()

    GameState.current = PlayState()

    ### BOX2D STUFF ###
    worldAABB=b2AABB()
    worldAABB.lowerBound = (-100, -100)
    worldAABB.upperBound = ( 100,  100)
    gravity = b2Vec2(0, 0)
    doSleep = False
    self.world = b2World(worldAABB, gravity, doSleep)
    self.timeStep = 1.0 / 60
    self.vel_iters, self.pos_iters = 10, 8

    self.b2draw = DebugDraw()
    self.b2draw.SetFlags(self.b2draw.e_shapeBit) # and whatever else you want it to draw 
    self.b2draw.viewZoom = 1.
    self.b2draw.viewCenter = b2Vec2(0,0)
    self.b2draw.viewOffset = b2Vec2(-200,50)
    self.world.SetDebugDraw(self.b2draw)

  def run_loop(self):
    
    black = [0,0,0]

    home = units.Home()
    # home_sprites = pygame.sprite.RenderPlain(home)

    def update():
      self.world.Step(self.timeStep, self.vel_iters, self.pos_iters)

    def draw():
      home.draw(self.screen)

    while 1:
      self.clock.tick(60)
      self.screen.fill(black)

      pygame.event.pump()
      key = pygame.key.get_pressed()

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          return
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            return
    
      update()
      draw()

      pygame.display.flip()


    

def main():
  game = Game()
  game.run_loop()


if __name__ == '__main__':
  main()
