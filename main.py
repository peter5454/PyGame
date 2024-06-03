import pygame as pg
import json
from enemy import Enemy
from world import World
import constants as c
from buttons import Button
from turrets import Turret
from tower import Tower
from airstrike import airstrike
import math as mt
import csv
from turrets_data import TURRET_DATA

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
turret_equipped = None
place_turret = None
placing_ability = False
turret_time = 0
active_airstrike = None
paused = False
counter = 0
save_error = False

#load images
#map
map_image = pg.image.load('assets/images/maps/map_1.png').convert_alpha()

#UI
side_panel = pg.image.load('assets/images/ui_backgrounds/side_panel.png').convert_alpha()
wood_frame_full = pg.image.load('assets/images/ui_backgrounds/wood_frame_full.png').convert_alpha()
health_bar = pg.image.load('assets/images/ui_backgrounds/health_bar.png').convert_alpha()
gold_bar = pg.image.load('assets/images/ui_backgrounds/gold_bar.png').convert_alpha()
airstrike_banner = pg.image.load('assets/images/ui_backgrounds/airstrike_banner.png').convert_alpha()
airstrike_ability_image = pg.image.load('assets/images/ui_backgrounds/airstrike_ability.png').convert_alpha()



#enemies
enemy_images = {
  "enemy_1": pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha(),
  "ice_golem": pg.image.load('assets/images/enemies/ice_golem.png').convert_alpha(),
  "fire_golem": pg.image.load('assets/images/enemies/fire_golem.png').convert_alpha(),
  "earth_golem": pg.image.load('assets/images/enemies/earth_golem.png').convert_alpha(),
  "ice_giant": pg.image.load('assets/images/enemies/ice_giant.png').convert_alpha(),
  "fire_giant": pg.image.load('assets/images/enemies/fire_giant.png').convert_alpha(),
  "earth_giant": pg.image.load('assets/images/enemies/earth_giant.png').convert_alpha()  
}

#turrets
#cannon
cursor_cannon = pg.image.load('assets/images/turrets/cursor_cannon.png').convert_alpha()
cannon_sheet = pg.image.load('assets/images/turrets/cannon_1.png').convert_alpha()
upgraded_cannon_sheet = pg.image.load('assets/images/turrets/cannon_2.png').convert_alpha()
#ice mage
cursor_ice = pg.image.load('assets/images/turrets/cursor_ice.png').convert_alpha()
ice_sheet = pg.image.load('assets/images/turrets/ice_mage_1.png').convert_alpha()
upgraded_ice_sheet = pg.image.load('assets/images/turrets/turret_2.png').convert_alpha()
#fire archer
cursor_fire = pg.image.load('assets/images/turrets/cursor_fire.png').convert_alpha()
fire_sheet = pg.image.load('assets/images/turrets/fire_archer_1.png').convert_alpha()
upgraded_fire_sheet = pg.image.load('assets/images/turrets/fire_archer_2.png').convert_alpha()
#earth catapult
cursor_earth = pg.image.load('assets/images/turrets/cursor_earth.png').convert_alpha()
earth_sheet = pg.image.load('assets/images/turrets/catapult_1.png').convert_alpha()
upgraded_earth_sheet = pg.image.load('assets/images/turrets/catapult_2.png').convert_alpha()
#king
cursor_king = pg.image.load('assets/images/turrets/cursor_king.png').convert_alpha()
#market
cursor_market = pg.image.load('assets/images/turrets/cursor_market.png').convert_alpha()

#buttons
buy_cannon_image = pg.image.load('assets/images/buttons/cannon_buy_button.png').convert_alpha()
buy_ice_image = pg.image.load('assets/images/buttons/ice_buy_button.png').convert_alpha()
buy_fire_image = pg.image.load('assets/images/buttons/fire_buy_button.png').convert_alpha()
buy_earth_image = pg.image.load('assets/images/buttons/earth_buy_button.png').convert_alpha()
buy_king_image = pg.image.load('assets/images/buttons/king_buy_button.png').convert_alpha()
buy_market_image = pg.image.load('assets/images/buttons/market_buy_button.png').convert_alpha()

cancel_image = pg.image.load('assets/images/buttons/cancel.png').convert_alpha()
begin_image = pg.image.load('assets/images/buttons/begin.png').convert_alpha()
restart_image = pg.image.load('assets/images/buttons/restart.png').convert_alpha()
upgrade_image = pg.image.load('assets/images/buttons/upgrade_turret.png').convert_alpha()
sell_image = pg.image.load('assets/images/buttons/sell.png').convert_alpha()
pause_button_image = pg.image.load('assets/images/buttons/pause_button.png').convert_alpha()
exit_button_image = pg.image.load('assets/images/buttons/exit_button.png').convert_alpha()
load_button_image = pg.image.load('assets/images/buttons/load_button.png').convert_alpha()
save_button_image = pg.image.load('assets/images/buttons/save_button.png').convert_alpha()
menu_button_image = pg.image.load('assets/images/buttons/menu_button.png').convert_alpha()

#create groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

#create buttons
turret_cannon_data = TURRET_DATA["TURRET_CANNON"][0]
cannon_button = Button(c.SCREEN_WIDTH - 245 ,290, buy_cannon_image, str(turret_cannon_data['cost']))
turret_ice_data = TURRET_DATA["TURRET_ICE"][0]
ice_button = Button(c.SCREEN_WIDTH - 122 ,290, buy_ice_image, str(turret_ice_data['cost']))
turret_fire_data = TURRET_DATA["TURRET_FIRE"][0]
fire_button = Button(c.SCREEN_WIDTH - 245 ,360, buy_fire_image, str(turret_fire_data['cost']))
turret_earth_data = TURRET_DATA["TURRET_EARTH"][0]
earth_button = Button(c.SCREEN_WIDTH - 122 ,360, buy_earth_image, str(turret_earth_data['cost']))
king_data = TURRET_DATA["KING"][0]
king_button = Button(c.SCREEN_WIDTH - 245 ,430, buy_king_image, str(king_data['cost']))
market_data = TURRET_DATA["MARKET"][0]
market_button = Button(c.SCREEN_WIDTH - 122 ,430, buy_market_image, str(market_data['cost']))

cancel_button = Button(c.SCREEN_WIDTH - 180 ,500, cancel_image)
begin_button = Button(c.SCREEN_WIDTH - 200 ,700, begin_image)
restart_button = Button(312.5 , 320, restart_image)
upgrade_button = Button(c.SCREEN_WIDTH - 220, 275, upgrade_image)
sell_button = Button(c.SCREEN_WIDTH - 220, 350, sell_image)
airstrike_ability = Button((c.SCREEN_WIDTH-c.SIDE_PANEL)/2 - 175, 0, airstrike_ability_image)
airstrike_ability2 = Button((c.SCREEN_WIDTH-c.SIDE_PANEL)/2 - 75, 0, airstrike_ability_image)
airstrike_ability3 = Button((c.SCREEN_WIDTH-c.SIDE_PANEL)/2 + 25, 0, airstrike_ability_image)
airstrike_ability4 = Button((c.SCREEN_WIDTH-c.SIDE_PANEL)/2 + 125, 0, airstrike_ability_image)
pause_button = Button(5,5, pause_button_image)
exit_button = Button(5,5, exit_button_image)
save_button = Button((c.SCREEN_WIDTH-c.SIDE_PANEL)/2, c.SCREEN_HEIGHT / 2 - 100, save_button_image)
load_button = Button((c.SCREEN_WIDTH-c.SIDE_PANEL)/2, c.SCREEN_HEIGHT / 2, load_button_image)
menu_button = Button((c.SCREEN_WIDTH-c.SIDE_PANEL)/2, c.SCREEN_HEIGHT / 2 - 200, menu_button_image)


#load json data for level
with open('assets/images/maps/map_1.tmj') as file:
  world_data = json.load(file)

#create world
world = World(world_data, map_image)
world.process_data()
world.process_enemies()

#load fonts for displaying text on the screen
text_font = pg.font.Font("assets/fonts/Amita-Regular.ttf", 24)
large_font = pg.font.Font("assets/fonts/Amita-Regular.ttf", 36)
error_font = pg.font.Font("assets/fonts/Aller_Bd.ttf", 24)

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

def create_turret(mouse_pos,turret_name,animation_sheet=None,upgraded_animation_sheet=None,upgrade_level=None,sprite=None):
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
        if turret_name != "KING" and turret_name != "MARKET":
          new_turret = Turret(animation_sheet, mouse_tile_x, mouse_tile_y,turret_name,upgraded_animation_sheet, upgrade_level)
        else:
          new_turret = Tower(mouse_tile_x, mouse_tile_y,turret_name,sprite)
        turret_group.add(new_turret)
        #update support tower effects
        update_supports(turret_group)
        selected_turret = None
        return True
  return False

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
  update_supports(turret_group)

  
def select_turret(mouse_pos):
  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
  for turret in turret_group:
    if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
      #print (turret)
      return turret

def update_supports(turret_group):
  for tower in turret_group:
    if tower.type[0]['name'] != "KING" and tower.type[0]['name'] != "MARKET":
      tower.damage_multiplier = 1
      tower.reward_multiplier = 1
  for tower in turret_group:
    if tower.type[0]['name'] == "KING":
      tower.update_king(turret_group)
    elif tower.type[0]['name'] == "MARKET":
      tower.update_market(turret_group)

    
def save():
  file = open("saves/save1/save1_world.csv", "w")
  file.write('money,health,level' + '\n' + str(world.money) + ','+ str(world.health) + ',' + str(world.level) + ',')
  file.close()

  file = open("saves/save1/save1_turrets.csv", "w")
  file.write('')
  file.close()

  file = open("saves/save1/save1_turrets.csv", "a")
  file.write("x,y,upgrade_level,turret_type")
  for turret in turret_group:
    file.write("\n{},{},{},{}".format(turret.tile_x, turret.tile_y, turret.upgrade_level, turret.turret_type))
  file.close

def load():
  turret_group.empty()

  with open('saves/save1/save1_world.csv', newline='') as constants_file:
    reader = csv.DictReader(constants_file)
    for row in reader:
      world.money = int(row['money'])
      world.health = int(row['health'])
      world.level = int(row['level'])
      world.killed_enemies = 0
      world.missed_enemies = 0 #only works because you cant load and save during rounds

  
  with open('saves/save1/save1_turrets.csv', newline='') as turret_file:
    turret_reader = csv.DictReader(turret_file)
    rows = 0
    x = []
    y = []
    upgrade_level = []
    turret_type = []
    print (turret_reader)
    sprite_sheet = [[] for _ in range(1000)]
    sprite_upgraded_sheet = [[] for _ in range(1000)]
    for row in turret_reader:
      x.append(row['x'])
      y.append(row['y'])
      upgrade_level.append(row['upgrade_level'])
      turret_type.append(row['turret_type'])
      rows += 1
    
    for row in range(rows):
      if turret_type[row] == "TURRET_ICE":
        sprite_sheet[row] = ice_sheet
        sprite_upgraded_sheet[row] = upgraded_ice_sheet
      if turret_type[row] == "TURRET_FIRE":
        sprite_sheet[row] = fire_sheet
        sprite_upgraded_sheet[row] = upgraded_fire_sheet
      if turret_type[row] == "TURRET_EARTH":
        sprite_sheet[row] = earth_sheet
        sprite_upgraded_sheet[row] = upgraded_earth_sheet
      if turret_type[row] == "TURRET_CANNON":
        sprite_sheet[row] = cannon_sheet
        sprite_upgraded_sheet[row] = upgraded_cannon_sheet
    
    if rows > 0:
      for i in range(len(x)):
        create_turret((int(x[i]) * c.TILE_SIZE, int(y[i]) * c.TILE_SIZE), turret_type[i], sprite_sheet[i], sprite_upgraded_sheet[i],int(upgrade_level[i]))
        print (turret_group)

  

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
    turret_group.update(enemy_group, world)

    #update airstrike



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

  #draw airstrike_banner
  screen.blit(airstrike_banner,((c.SCREEN_WIDTH-c.SIDE_PANEL)/2-200,c.SCREEN_HEIGHT-900))

  #draw game stats
  draw_text("Round", text_font, "grey100", 838, 32)
  draw_text(str(world.level), text_font, "grey100", 925, 32)
  draw_text(str(world.health), text_font, "grey100", 890, 97)
  draw_text(str(world.money), text_font, "grey100", 890, 164)

  if game_over == False:
    #check if the level has been started or not
    if level_started == False:
      if begin_button.draw(screen):
        last_enemy_spawn = pg.time.get_ticks()
        world.reset_level()
        if world.level <= c.TOTAL_LEVELS:
          world.process_enemies()
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
      print (world.level)
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

    #buy turrets
    if placing_turrets == False and selected_turret == None:
      #cannon
      if cannon_button.draw(screen):
        turret_equipped = TURRET_DATA.get("TURRET_CANNON", None)
        new_turret = Turret(cannon_sheet,0,0,turret_equipped[0]['name'],upgraded_cannon_sheet,1)
        if world.money >= new_turret.cost:
          placing_turrets = True
        else:
          turret_equipped = None

      #ice mage
      if ice_button.draw(screen):
        turret_equipped = TURRET_DATA.get("TURRET_ICE", None)
        new_turret = Turret(ice_sheet,0,0,turret_equipped[0]['name'],upgraded_ice_sheet,1) 
        if world.money >= new_turret.cost:
          placing_turrets = True
        else:
          turret_equipped = None
      #fire archer
      if fire_button.draw(screen):
        turret_equipped = TURRET_DATA.get("TURRET_FIRE", None)
        new_turret = Turret(fire_sheet,0,0,turret_equipped[0]['name'],upgraded_fire_sheet,1) 
        if world.money >= new_turret.cost:
          placing_turrets = True
        else:
          turret_equipped = None
      #earth catapult
      if earth_button.draw(screen):
        turret_equipped = TURRET_DATA.get("TURRET_EARTH", None)
        new_turret = Turret(earth_sheet,0,0,turret_equipped[0]['name'],upgraded_earth_sheet,1)
        
        if world.money >= new_turret.cost:
          placing_turrets = True
        else:
          turret_equipped = None
      #king
      if king_button.draw(screen):
        turret_equipped = TURRET_DATA.get("KING", None)
        new_turret = Tower(0,0,turret_equipped[0]['name'],cursor_king) 
        if world.money >= new_turret.cost:
          placing_turrets = True
        else:
          turret_equipped = None
      #market
      if market_button.draw(screen):
        turret_equipped = TURRET_DATA.get("MARKET", None)
        new_turret = Tower(0,0,turret_equipped[0]['name'],cursor_market) 
        if world.money >= new_turret.cost:
          placing_turrets = True
        else:
          turret_equipped = None
    
    if placing_turrets and placing_ability:
      placing_turrets = False

    if placing_turrets == True:
      cursort_rect = cursor_cannon.get_rect()
      cursor_pos = pg.mouse.get_pos()
      cursort_rect.center = cursor_pos
      if turret_equipped[0]['name'] == "TURRET_ICE":
        screen.blit(cursor_ice, cursort_rect) 
      elif turret_equipped[0]['name'] == "TURRET_FIRE":
        screen.blit(cursor_fire, cursort_rect)
      elif turret_equipped[0]['name'] == "TURRET_EARTH":
        screen.blit(cursor_earth, cursort_rect)
      elif turret_equipped[0]['name'] == "KING":
        screen.blit(cursor_king, cursort_rect)
      elif turret_equipped[0]['name'] == "MARKET":
        screen.blit(cursor_market, cursort_rect) #create more for different turrets
      else:
        screen.blit(cursor_cannon, cursort_rect) #remove else statement and create more if statments
    


      if tile_occupied(cursor_pos):
        draw_circ(255,0,0,turret_equipped[0]['range'],cursor_pos) #need to change to a varible that matches the turret range rather than a number
      else:
        draw_circ(128,128,128,turret_equipped[0]['range'],cursor_pos) #need to change to a varible that matches the turret range rather than a number


      if cancel_button.draw(screen):
        placing_turrets = False
    if placing_ability == False:
      if airstrike_ability.draw(screen):
        new_aristrike = airstrike("airstrike_1")
        placing_ability = True

      if airstrike_ability2.draw(screen):
        new_aristrike = airstrike("airstrike_2")
        placing_ability = True

      if airstrike_ability3.draw(screen):
        new_aristrike = airstrike("airstrike_3")
        placing_ability = True

      if airstrike_ability4.draw(screen):
        new_aristrike = airstrike("airstrike_4")
        placing_ability = True


    if placing_ability:
      cursor_pos = pg.mouse.get_pos()

      if world.money >= new_aristrike.cost:
        if cancel_button.draw(screen):
          placing_ability = False
        if new_aristrike.airstrike_name == "airstrike_1":
          draw_circ(128, 255, 128, new_aristrike.size, cursor_pos)
        if new_aristrike.airstrike_name == "airstrike_2":
          draw_circ(128, 128, 255, new_aristrike.size, cursor_pos)
        if new_aristrike.airstrike_name == "airstrike_3":
          draw_circ(128, 255, 128, new_aristrike.size, cursor_pos)
        if new_aristrike.airstrike_name == "airstrike_4":
          draw_circ(128, 128, 128, new_aristrike.size, cursor_pos)
        if pg.mouse.get_pressed()[0] and cursor_pos[0] < c.SCREEN_WIDTH - c.SIDE_PANEL and cursor_pos[1] > c.SCREEN_HEIGHT - 700:  # check if left mouse button is clicked
          world.money -= new_aristrike.cost
          new_aristrike.start(cursor_pos)
          active_airstrike = new_aristrike
          placing_ability = False
      else:
        placing_ability = False
    if active_airstrike:
      active_airstrike.place_ability(enemy_group, screen)
      if active_airstrike.shots_fired < active_airstrike.waves:
        draw_circ(123, 255, 123, active_airstrike.size, (active_airstrike.x,active_airstrike.y)) #if more airstrikes get more waves change this to include the different colour circles
      if active_airstrike.shots_fired != counter:
        counter = active_airstrike.shots_fired
        draw_circ(255, 255, 255, active_airstrike.size, (active_airstrike.x,active_airstrike.y)) #flashes white once the timer is finished
      if counter >= active_airstrike.waves:
        counter = 0
        active_airstrike = None
    if pause_button.draw(screen):
        paused = True
        game_over = True

  else:
    #game is over
    if paused == True:
      
      if placing_ability == False:
        airstrike_ability.draw2(screen)
        airstrike_ability2.draw2(screen)
        airstrike_ability3.draw2(screen)
        airstrike_ability4.draw2(screen)

      if selected_turret is not None:
        upgrade_button.draw2(screen)
        sell_button.draw2(screen)

      if not placing_turrets and selected_turret is None:
        cannon_button.draw2(screen)
        ice_button.draw2(screen) 
        fire_button.draw2(screen) 
        earth_button.draw2(screen) 

      if placing_ability or selected_turret or placing_turrets:
        cancel_button.draw2(screen)
      
      if level_started == False:
        begin_button.draw2(screen)
        draw_circ(128,128,128,1000,(c.SCREEN_WIDTH/2,c.SCREEN_HEIGHT/2))
        if load_button.draw(screen):
          load()
          selected_turret = None
          placing_ability = False
          placing_turrets = False
          
        if save_button.draw(screen):
          save()

      if level_started == True:
        if load_button.draw(screen):
            save_error = True
          
        if save_button.draw(screen):
            save_error = True
            
        draw_circ(128,128,128,1000,(c.SCREEN_WIDTH/2,c.SCREEN_HEIGHT/2))
        if save_error == True:
          draw_text("Can't save or load while in a round", error_font, (0, 0, 0), 250, 450)
          draw_text("Wait until the end", error_font, (0, 0, 0), 350, 500)
      if menu_button.draw(screen):
        print (123)

      

      if exit_button.draw(screen):
        save_error == False
        game_over = False
        paused = False
        



      


    
    if paused == False and game_over == True:

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
      if mouse_pos[0] < c.SCREEN_WIDTH - c.SIDE_PANEL and mouse_pos[1] > c.SCREEN_HEIGHT-680:
        selected_turret = None
        clear_selected()
        if placing_turrets == True:
          #check if support tower
          if turret_equipped[0]['name'] == "KING":
            place_turret = create_turret(mouse_pos, turret_equipped[0]['name'],None, None, None, cursor_king)
          elif turret_equipped[0]['name'] == "MARKET":
            place_turret = create_turret(mouse_pos, turret_equipped[0]['name'],None, None, None, cursor_market)
          else: #damage tower
            place_turret = create_turret(mouse_pos,turret_equipped[0]['name'],new_turret.sprite_sheet,new_turret.sprite_upgraded_sheet,1)
          turret_time = pg.time.get_ticks()
        if place_turret:
          world.money -= new_turret.cost
          placing_turrets = False
          place_turret = None
        if pg.time.get_ticks() > turret_time + 10:    
          if placing_turrets == False:
            selected_turret = select_turret(mouse_pos)


          
    
  #update display
  pg.display.flip()

pg.quit()