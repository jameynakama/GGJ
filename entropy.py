import os, sys, pygame, Box2D 
from pygame.locals import *

class Game:
  def __init__(self):
    pygame.init()

    self.screen_size = [512, 512]

    self.screen = pygame.display.set_mode(self.screen_size)
    self.clock = pygame.time.Clock()
    pygame.display.set_caption('Entropy')

    self.backgd = pygame.Surface(self.screen.get_size())
    back_color = [128,128,128]

    self.frames = 0
    self.show = pygame.sprite.RenderClear()

  def run_loop():
    
    go = True
    black = [0,0,0]
    while go:
      go = True
      self.clock.tick(60)
      self.screen.fill(black)

      pygame.event.pump()
      key = pygame.key.get_pressed()

      for event in pygame.event.get():
        if even.type == pygame.QUIT:
          return
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            return

      pygame.display.flip()


def main():
  game = Game()


if __name__ == '__main__':
  main()
