import os, sys, pygame
from Box2D import *
from pygame.locals import *
from common import *
from game_state import *
import units
import cProfile

class Game:

  media = None

  def __init__(self):
    pygame.init()

    self.screen_size = [800, 800]

    self.screen = pygame.display.set_mode(self.screen_size)
    self.clock = pygame.time.Clock()
    pygame.display.set_caption('Entropy')

    self.backgd = pygame.Surface(self.screen.get_size())
    self.back_color = [128,128,128]

    physics.b2draw.surface = self.screen

    self.frames = 0
    self.show = pygame.sprite.RenderClear()

    GameState.current = PlayState()

    Game.media = Media()
    Game.media.dragon = load_img('dragon.png')



  def run_loop(self):

    home = units.Home()
    units.Home.instance = home
    # home_sprites = pygame.sprite.RenderPlain(home)

    def update():
      home.update()
      GameState.current.update()
      physics.worldStep()

    def draw():
      GameState.current.draw(self.screen)
      home.draw(self.screen)

    while 1:
      self.clock.tick(FPS)
      self.screen.fill(self.back_color)

      pygame.event.pump()
      key = pygame.key.get_pressed()

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          return
        if event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            return
    
      home.event(key)
      if (pygame.time.get_ticks() / 1000) % 2 == 0:
        units.Dragon(Game.media.dragon)
      update()
      draw()


      pygame.display.flip()

    

def main():
  game = Game()
  game.run_loop()


if __name__ == '__main__':
  main()
  # cProfile.run('main()')


