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

#game variables
last_enemy_spawn = pg.time.get_ticks()
placing_turrets = False


#load images
#map
map_image = pg.image.load('assets/images/maps/map_1.png').convert_alpha()
#enemies
enemy_images = {
  "enemy_1": pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha(),
  "ice_golem": pg.image.load('assets/images/enemies/ice_golem.png').convert_alpha(),
  "fire_golem": pg.image.load('assets/images/enemies/fire_golem.png').convert_alpha()
}

#load json data for level
with open('assets/images/maps/map_1.tmj') as file:
  world_data = json.load(file)

#create world
world = World(world_data, map_image)
world.process_data()
world.process_enemies()

#turret
cursor_turret = pg.image.load('assets/images/turrets/cursor_turret.png').convert_alpha()

buy_turret_image = pg.image.load('assets/images/buttons/buy_turret.png').convert_alpha()
cancel_image = pg.image.load('assets/images/buttons/cancel.png').convert_alpha()

#create groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

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
  #close = False
  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
  #calculate the sequential number of the tile
  mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
  #check if that tile is grass
  if world.tile_map[mouse_tile_num] == 18:
    #check that there isn't already a turret there
    space_is_free = True
    for turret in turret_group:
      if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
        space_is_free = False
      #if it is a free space then create turret
    if space_is_free == True:
      new_turret = Turret(cursor_turret, mouse_tile_x, mouse_tile_y)  
      turret_group.add(new_turret)
      """
      close = overlapping_turrets(mouse_pos)
      if close == False:
        turret_group.add(new_turret)
        return True
      else:
        return False
      """

def tile_occupied(mouse_pos):
  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
  #calculate the sequential number of the tile
  mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
  #check if that tile is grass
  if world.tile_map[mouse_tile_num] != 18:
    return True
  #chek if mouse tile is occupied
  for turret in turret_group:
    if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
      return True
  return False
  """
  if 10 > mouse_pos[0] or mouse_pos[0] > c.SCREEN_WIDTH - 10:
    return True
  if 10 > mouse_pos[1] or mouse_pos[1] > c.SCREEN_HEIGHT - 10:
    return True
  for i in turret_group:
      dist = distance(mouse_pos, i.rect.center)
      if dist < mt.sqrt((mt.pi * 10)**2 ): #create circle around the point of radius 10
        return True
  return False
  """
    

#game loop
run = True
while run:

  clock.tick(c.FPS)

  #####################
  # UPDATING SECTION
  #####################

  #update groups
  enemy_group.update()


  #####################
  # DRAWING SECTION
  #####################

  screen.fill("grey100")

  #draw level
  world.draw(screen)

  #draw enemy path
  #pg.draw.lines(screen, "grey0", False, world.waypoints)

  #draw groups
  enemy_group.draw(screen)
  turret_group.draw(screen)

  #spawn enemies
  if pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
    if world.spawned_enemies < len(world.enemy_list):
      enemy_type = world.enemy_list[world.spawned_enemies]
      enemy = Enemy(enemy_type, world.waypoints, enemy_images)
      enemy_group.add(enemy)
      world.spawned_enemies += 1
      last_enemy_spawn = pg.time.get_ticks()

  if placing_turrets == False:
    if turret_button.draw(screen):
      placing_turrets = True
  
  if placing_turrets == True:
    cursort_rect = cursor_turret.get_rect()
    cursor_pos = pg.mouse.get_pos()
    cursort_rect.center = cursor_pos
    screen.blit(cursor_turret, cursort_rect)

    if tile_occupied(cursor_pos):
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
    #mouse click
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
      mouse_pos = pg.mouse.get_pos()
      #check if mouse is on the game area
      if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:

        if placing_turrets == True:
          place_turret = create_turret(mouse_pos)
          if place_turret:
            placing_turrets = False
          
    
  #update display
  pg.display.flip()

pg.quit()