import pygame as pg
from enemy import Enemy
import constants as c
from buttons import Button
from turrets import Turret

#initialise pygame
pg.init()

#create clock
clock = pg.time.Clock()

#create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Medieval Meltdown")

#load images
enemy_image = pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha()
cursor_turret = pg.image.load('assets/images/turrets/cursor_turret.png').convert_alpha()

buy_turret_image = pg.image.load('assets/images/buttons/buy_turret.png').convert_alpha()
cancel_image = pg.image.load('assets/images/buttons/cancel.png').convert_alpha()

#create groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

enemy = Enemy((200, 300), enemy_image)
enemy_group.add(enemy)

turret_button = Button(c.SCREEN_WIDTH + 80 ,150, buy_turret_image)
cancel_button = Button(c.SCREEN_WIDTH + 100 ,250, cancel_image)

def create_turret(mouse_pos):
  new_turret = Turret(cursor_turret, mouse_pos)
  turret_group.add(new_turret)
#game variables
placing_turrets = False
#game loop
run = True
while run:

  clock.tick(c.FPS)

  screen.fill("grey100")

  #update groups
  enemy_group.update()

  #draw groups
  enemy_group.draw(screen)
  if placing_turrets == False:
    if turret_button.draw(screen):
      placing_turrets = True
  if placing_turrets == True:
    cursort_rect = cursor_turret.get_rect()
    cursor_pos = pg.mouse.get_pos()
    cursort_rect.center = cursor_pos
    screen.blit(cursor_turret, cursort_rect)
    if cancel_button.draw(screen):
      placing_turrets = False

  #event handler
  for event in pg.event.get():
    #quit program
    if event.type == pg.QUIT:
      run = False
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
      mouse_pos = pg.mouse.get_pos
      if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
        if placing_turrets == True:
          create_turret(mouse_pos)
    
  #update display
  pg.display.flip()

pg.quit()