import pygame as pg
from enemy import Enemy
import constants as c
from buttons import Button

#initialise pygame
pg.init()

#create clock
clock = pg.time.Clock()

#create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Medieval Meltdown")

#load images
enemy_image = pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha()
buy_turret_image = pg.image.load('assets/images/buttons/buy_turret.png').convert_alpha()
cancel_image = pg.image.load('assets/images/buttons/cancel.png').convert_alpha()

#create groups
enemy_group = pg.sprite.Group()

enemy = Enemy((200, 300), enemy_image)
enemy_group.add(enemy)

turret_button = Button(c.SCREEN_WIDTH + 80 ,150, buy_turret_image)
cancel_button = Button(c.SCREEN_WIDTH + 100 ,200, cancel_image)


#game loop
run = True
while run:

  clock.tick(c.FPS)

  screen.fill("grey100")

  #update groups
  enemy_group.update()

  #draw groups
  enemy_group.draw(screen)

  turret_button.draw(screen)
  cancel_button.draw(screen)

  #event handler
  for event in pg.event.get():
    #quit program
    if event.type == pg.QUIT:
      run = False

  #update display
  pg.display.flip()

pg.quit()