import os, sys, pygame, Box2D 
from pygame.locals import *
import units

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

  def run_loop(self):
    
    black = [0,0,0]

    home = units.Home()
    home_sprites = pygame.sprite.RenderPlain(home)

    go = True
    while go:
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

      home_sprites.update()
      # the radius is hard-coded below just to get the ball rolling.
      # the update method for Home should calculate its position eventually
      pygame.draw.circle(self.screen, [255,255,0], [400,400], int(home.radius), 0)
      # we should also eventually be able to say something like
      # home_sprites.draw(screen) instead of this
      pygame.display.flip()


def main():
  game = Game()
  game.run_loop()


if __name__ == '__main__':
  main()
