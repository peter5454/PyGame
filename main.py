import pygame as pg
import json
from enemy import Enemy
from world import World
import constants as c
from buttons import Button
from turrets import Turret
import math as mt

#initialise pygame
pg.init()

#create clock
clock = pg.time.Clock()

#create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption("Medieval Meltdown")

#load images
#map
map_image = pg.image.load('assets/images/maps/map_1.png').convert_alpha()
#enemies
enemy_image = pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha()

#load json data for level
with open('assets/images/maps/map_1.tmj') as file:
  world_data = json.load(file)

#create world
world = World(world_data, map_image)
world.process_data()

#turret
cursor_turret = pg.image.load('assets/images/turrets/cursor_turret.png').convert_alpha()

buy_turret_image = pg.image.load('assets/images/buttons/buy_turret.png').convert_alpha()
cancel_image = pg.image.load('assets/images/buttons/cancel.png').convert_alpha()

#create groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

enemy = Enemy(world.waypoints, enemy_image)
enemy_group.add(enemy)

turret_button = Button(c.SCREEN_WIDTH - 160 ,150, buy_turret_image)
cancel_button = Button(c.SCREEN_WIDTH - 200 ,250, cancel_image)

def distance(point1, point2):
  return mt.sqrt(((point1[0] - point2[0]) ** 2)+  (point1[1] - point2[1]) **2) #calculate euclidian distance

def draw_circ(R,G,B,Size):
  transparent_surface = pg.Surface((c.SCREEN_WIDTH, c.SCREEN_HEIGHT), pg.SRCALPHA)
  transparent_surface.fill((0, 0, 0, 0))
  pg.draw.circle(transparent_surface, (R, G, B, 50), cursor_pos, Size)
  screen.blit(transparent_surface, (0, 0))

def create_turret(mouse_pos):
  close = False
  new_turret = Turret(cursor_turret, mouse_pos)  
  close = overlapping_turrets(mouse_pos)
  if close == False:
    turret_group.add(new_turret)
    return True
  else:
    return False

def overlapping_turrets(mouse_pos):
  if 10 > mouse_pos[0] or mouse_pos[0] > c.SCREEN_WIDTH-10:
    return True
  if 10 > mouse_pos[1] or mouse_pos[1] > c.SCREEN_HEIGHT-10:
    return True
  for turret in turret_group:
      dist = distance(mouse_pos, turret.rect.center)
      if dist < mt.sqrt((mt.pi * turret.range)**2 ): #create circle around the point of radius 10
        return True
  return False

def selected_turret(mouse_pos):
  for turret in turret_group:
    dist = distance(mouse_pos, turret.rect.center)
    if dist < 10:
      print (turret)
      return turret

#game variables
placing_turrets = False
selected_turret = None
#game loop
run = True
while run:

  clock.tick(c.FPS)
  screen.fill("grey100")

  #draw level
  world.draw(screen)

  #draw enemy path
  #pg.draw.lines(screen, "grey0", False, world.waypoints)

  #update groups
  enemy_group.update()

  #draw groups
  enemy_group.draw(screen)
  turret_group.draw(screen)


  if placing_turrets == False:
    if turret_button.draw(screen):
      placing_turrets = True
  
  if placing_turrets == True:
    cursort_rect = cursor_turret.get_rect()
    cursor_pos = pg.mouse.get_pos()
    cursort_rect.center = cursor_pos
    screen.blit(cursor_turret, cursort_rect)
    if overlapping_turrets(cursor_pos):
      draw_circ(255,0,0,200)
    else:
      draw_circ(128,128,128,200)
      

    if cancel_button.draw(screen):
      placing_turrets = False

  #event handler
  for event in pg.event.get():
    #quit program
    if event.type == pg.QUIT:
      run = False
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
      mouse_pos = pg.mouse.get_pos()
      if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
        if placing_turrets == True:
          place_turr = create_turret(mouse_pos)
          if place_turr:
            placing_turrets = False
          
    
  #update display
  pg.display.flip()

pg.quit()