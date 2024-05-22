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
game_over = False
game_outcome = 0 # -1 is loss & 1 is win
level_started = False
last_enemy_spawn = pg.time.get_ticks()
placing_turrets = False
selected_turret = None

#load images
#map
map_image = pg.image.load('assets/images/maps/map_1.png').convert_alpha()

#UI
side_panel = pg.image.load('assets/images/ui_backgrounds/side_panel.png').convert_alpha()
wood_frame_full = pg.image.load('assets/images/ui_backgrounds/wood_frame_full.png').convert_alpha()
health_bar = pg.image.load('assets/images/ui_backgrounds/health_bar.png').convert_alpha()
gold_bar = pg.image.load('assets/images/ui_backgrounds/gold_bar.png').convert_alpha()


#enemies
enemy_images = {
  "enemy_1": pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha(),
  "ice_golem": pg.image.load('assets/images/enemies/ice_golem.png').convert_alpha(),
  "fire_golem": pg.image.load('assets/images/enemies/fire_golem.png').convert_alpha(),
  "earth_golem": pg.image.load('assets/images/enemies/earth_golem.png').convert_alpha(),
  "earth_giant": pg.image.load('assets/images/enemies/earth_giant.png').convert_alpha()
  
}

#turrets
cursor_turret = pg.image.load('assets/images/turrets/cursor_turret.png').convert_alpha()
turret_sheet = pg.image.load('assets/images/turrets/cannon_1.png').convert_alpha()

#buttons
buy_turret_image = pg.image.load('assets/images/buttons/buy_turret.png').convert_alpha()
cancel_image = pg.image.load('assets/images/buttons/cancel.png').convert_alpha()
begin_image = pg.image.load('assets/images/buttons/begin.png').convert_alpha()
restart_image = pg.image.load('assets/images/buttons/restart.png').convert_alpha()
upgrade_image = pg.image.load('assets/images/buttons/upgrade_turret.png').convert_alpha()
sell_image = pg.image.load('assets/images/buttons/sell.png').convert_alpha()

#create groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

#create buttons
turret_button = Button(c.SCREEN_WIDTH - 200 ,300, buy_turret_image)
cancel_button = Button(c.SCREEN_WIDTH - 180 ,500, cancel_image)
begin_button = Button(c.SCREEN_WIDTH - 200 ,700, begin_image)
restart_button = Button(312.5 , 320, restart_image)
upgrade_button = Button(c.SCREEN_WIDTH - 220, 275, upgrade_image)
sell_button = Button(c.SCREEN_WIDTH - 220, 350, sell_image)


#load json data for level
with open('assets/images/maps/map_1.tmj') as file:
  world_data = json.load(file)

#create world
world = World(world_data, map_image)
world.process_data()
world.process_enemies()

#load fonts for displaying text on the screen
text_font = pg.font.SysFont("Consolas", 24, bold = True)
large_font = pg.font.SysFont("Consolas", 36)

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))


def distance(point1, point2):
  return mt.sqrt(((point1[0] - point2[0]) ** 2)+  (point1[1] - point2[1]) **2) #calculate euclidian distance

def draw_circ(R,G,B,Size,location):
  transparent_surface = pg.Surface((c.SCREEN_WIDTH, c.SCREEN_HEIGHT), pg.SRCALPHA)
  transparent_surface.fill((0, 0, 0, 0))
  pg.draw.circle(transparent_surface, (0, 0, 0, 100), location, Size + 2)
  pg.draw.circle(transparent_surface, (R, G, B, 70), location, Size)
  screen.blit(transparent_surface, (0, 0))

def clear_selected():
  for turret in turret_group:
    turret.selected = False

def upgrade_turret(selected_turret):
  if world.money - selected_turret.upgrade_cost >= 0:
    if selected_turret.upgrade_level <  selected_turret.max_level:
      world.money -= selected_turret.upgrade_cost
      selected_turret.upgrade()
      print (selected_turret.upgrade_level)
      print (selected_turret.damage)
    else:
      print("Maximum upgrade level reached.")
  else:
    print ("Out of Money")

def create_turret(mouse_pos):
  #close = False
  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
  #calculate the sequential number of the tile
  mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
  #check if that tile is grass
  if mouse_pos[0] < c.SCREEN_WIDTH - c.SIDE_PANEL: #check if mouse is not on side panel
    if world.tile_map[mouse_tile_num] == 18:
      #check that there isn't already a turret there
      space_is_free = True
      if mouse_pos[0] > (c.SCREEN_WIDTH - c.SIDE_PANEL - 1):
        space_is_free = False
      elif len(turret_group) > 0:
        for turret in turret_group:
          if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            space_is_free = False
      #if it is a free space then create turret
      if space_is_free == True:
        new_turret = Turret(turret_sheet, mouse_tile_x, mouse_tile_y)  
        turret_group.add(new_turret)
        #deduct cost of turret
        world.money -= new_turret.cost
        return True
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

  if world.tile_map[mouse_tile_num] != 18 or mouse_pos[0] > (c.SCREEN_WIDTH - c.SIDE_PANEL - 1):
    return True
  #check if mouse tile is occupied
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
    
def sell_turret(selected_turret):
  sell_value = selected_turret.sell()
  world.money += sell_value

      

  
def select_turret(mouse_pos):
  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
  for turret in turret_group:
    if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
      #print (turret)
      return turret
  
#game loop
run = True
while run:

  clock.tick(c.FPS)

  #####################
  # UPDATING SECTION
  #####################

  if game_over == False:
    #check if player has lost
    if world.health <= 0:
      game_over = True
      game_outcome = -1 #loss
    #check if player has won
    if world.level > c.TOTAL_LEVELS:
      game_over = True
      game_outcome = 1 #win

    #update groups
    enemy_group.update(world)
    turret_group.update(enemy_group)


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
  for turret in turret_group:
    turret.draw(screen)

  #draw side panel
  screen.blit(side_panel, ((c.SCREEN_WIDTH - c.SIDE_PANEL), 0))
  screen.blit(wood_frame_full, (796, 26))
  screen.blit(health_bar, (796, 88))
  screen.blit(gold_bar, (796, 155))


  draw_text("Round", text_font, "grey100", 838, 45)
  draw_text(str(world.level), text_font, "grey100", 925, 45)
  draw_text(str(world.health), text_font, "grey100", 890, 110)
  draw_text(str(world.money), text_font, "grey100", 890, 177)

  if game_over == False:
    #check if the level has been started or not
    if level_started == False:
      if begin_button.draw(screen):
        level_started = True
    else:
      #spawn enemies
      if pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
        if world.spawned_enemies < len(world.enemy_list):
          enemy_type = world.enemy_list[world.spawned_enemies]
          enemy = Enemy(enemy_type, world.waypoints, enemy_images)
          enemy_group.add(enemy)
          world.spawned_enemies += 1
          last_enemy_spawn = pg.time.get_ticks()

    #check if wave is finished
    if world.check_level_complete() == True:
      world.money += c.LEVEL_COMPLETE_REWARD
      world.level += 1
      level_started = False
      last_enemy_spawn = pg.time.get_ticks()
      world.reset_level()
      if world.level <= c.TOTAL_LEVELS:
        world.process_enemies()

    if placing_turrets == False:
        if selected_turret:
          selected_turret.selected = True
          draw_circ(200,200,200,selected_turret.range,(selected_turret.x, selected_turret.y))
          if upgrade_button.draw(screen):
            upgrade_turret(selected_turret)
          if sell_button.draw(screen):
            sell_turret(selected_turret)
            selected_turret = None
          if cancel_button.draw(screen):
            selected_turret = None
    if placing_turrets == False and selected_turret == None:
      if turret_button.draw(screen):
        placing_turrets = True
    
    
    if placing_turrets == True:
      cursort_rect = cursor_turret.get_rect()
      cursor_pos = pg.mouse.get_pos()
      cursort_rect.center = cursor_pos
      screen.blit(cursor_turret, cursort_rect)

      if tile_occupied(cursor_pos):
        draw_circ(255,0,0,90,cursor_pos) #need to change to a varible that matches the turret range rather than a number
      else:
        draw_circ(128,128,128,90,cursor_pos) #need to change to a varible that matches the turret range rather than a number


      if cancel_button.draw(screen):
        placing_turrets = False

  else:
    #game is over
    pg.draw.rect(screen, "dodgerblue", (200, 200, 400, 200), border_radius = 30)
    if game_outcome == -1:
      draw_text("GAME OVER", large_font, "grey0", 310, 230)
    elif game_outcome == 1:
      draw_text("YOU WIN", large_font, "grey0", 315, 230)


    #restart level
    if restart_button.draw(screen):
      game_over = False
      level_started = False
      placing_turrets = False
      selected_turret = None
      last_enemy_spawn = pg.time.get_ticks()
      world = World(world_data, map_image)
      world.process_data()
      world.process_enemies()
      #empty groups
      enemy_group.empty()
      turret_group.empty()


  #event handler
  for event in pg.event.get():
    #quit program
    if event.type == pg.QUIT:
      run = False
    #mouse click
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
      mouse_pos = pg.mouse.get_pos()
      #check if mouse is on the game area
      if mouse_pos[0] < c.SCREEN_WIDTH - c.SIDE_PANEL and mouse_pos[1] < c.SCREEN_HEIGHT:
        selected_turret = None
        clear_selected()
        if placing_turrets == True:
          #check if there is enough money for a turret
          new_turret = Turret(turret_sheet,0,0) # add instance for which turret it is
          if world.money >= new_turret.cost:
            place_turret = create_turret(mouse_pos) #need to pass the turret aswell 
            turret_time = pg.time.get_ticks()
          if place_turret:
            placing_turrets = False
        if pg.time.get_ticks() > turret_time + 10:    
          if placing_turrets == False:
            selected_turret = select_turret(mouse_pos)
          
    
  #update display
  pg.display.flip()

pg.quit()