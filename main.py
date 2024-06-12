import pygame as pg
import json
from enemy import Enemy
from health_bars import HealthBar
from world import World
import constants as c
from buttons import Button
from turrets import Turret
from tower import Tower
from airstrike import airstrike
import math as mt
import csv
from turrets_data import TURRET_DATA
from airstrike_data import AIRSTRIKE_DATA


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
menu_counter = 0
muted = False
buy_round_song = False

#load images
#map
map_image = pg.image.load('assets/images/maps/map_1.png').convert_alpha()

#UI
side_panel = pg.image.load('assets/images/ui_backgrounds/side_panel.png').convert_alpha()
wood_frame_full = pg.image.load('assets/images/ui_backgrounds/wood_frame_full.png').convert_alpha()
health_bar_side_panel = pg.image.load('assets/images/ui_backgrounds/health_bar.png').convert_alpha()
gold_bar = pg.image.load('assets/images/ui_backgrounds/gold_bar.png').convert_alpha()
airstrike_banner = pg.image.load('assets/images/ui_backgrounds/airstrike_banner.png').convert_alpha()
arrow_strike_ability_image = pg.image.load('assets/images/buttons/arrow_strike_button.png').convert_alpha()
ice_strike_ability_image = pg.image.load('assets/images/buttons/ice_strike_button.png').convert_alpha()
fire_strike_ability_image = pg.image.load('assets/images/buttons/fire_strike_button.png').convert_alpha()
earth_strike_ability_image = pg.image.load('assets/images/buttons/earth_strike_button.png').convert_alpha()
menu_background = pg.image.load('assets/images/ui_backgrounds/MenuBG.png').convert_alpha()
medieval = pg.image.load('assets/images/ui_backgrounds/Medieval.png').convert_alpha()
meltdown = pg.image.load('assets/images/ui_backgrounds/Meltdown.png').convert_alpha()



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
upgraded_ice_sheet = pg.image.load('assets/images/turrets/ice_mage_2.png').convert_alpha()
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
#tower_king = pg.image.load('assets/images/turrets/tower_king.png').convert_alpha()
#market
cursor_market = pg.image.load('assets/images/turrets/cursor_market.png').convert_alpha()
#tower_market = pg.image.load('assets/images/turrets/tower_market.png').convert_alpha()

#buttons
buy_cannon_image = pg.image.load('assets/images/buttons/cannon_buy_button.png').convert_alpha()
buy_ice_image = pg.image.load('assets/images/buttons/ice_buy_button.png').convert_alpha()
buy_fire_image = pg.image.load('assets/images/buttons/fire_buy_button.png').convert_alpha()
buy_earth_image = pg.image.load('assets/images/buttons/earth_buy_button.png').convert_alpha()
buy_king_image = pg.image.load('assets/images/buttons/king_buy_button.png').convert_alpha()
buy_market_image = pg.image.load('assets/images/buttons/market_buy_button.png').convert_alpha()

cancel_image = pg.image.load('assets/images/buttons/cancel.png').convert_alpha()
start_image = pg.image.load('assets/images/buttons/start_button.png').convert_alpha()
restart_image = pg.image.load('assets/images/buttons/restart.png').convert_alpha()
upgrade_image = pg.image.load('assets/images/buttons/upgrade_turret.png').convert_alpha()
sell_image = pg.image.load('assets/images/buttons/sell_button.png').convert_alpha()
pause_button_image = pg.image.load('assets/images/buttons/pause_button.png').convert_alpha()
exit_button_image = pg.image.load('assets/images/buttons/exit_button.png').convert_alpha()
load_button_image = pg.image.load('assets/images/buttons/load_button1.png').convert_alpha()
save_button_image = pg.image.load('assets/images/buttons/save_button.png').convert_alpha()
menu_button_image = pg.image.load('assets/images/buttons/menu_button.png').convert_alpha()
menu_base_button_image = pg.image.load('assets/images/buttons/Menu_base_button.png').convert_alpha()

mute_button_image = pg.image.load('assets/images/buttons/mute_button.png').convert_alpha()
mute_button_pressed_image = pg.image.load('assets/images/buttons/mute_button_pressed.png').convert_alpha()

#create groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()
health_bars = []

#create buttons
#buy buttons
cannon_button = Button(c.SCREEN_WIDTH - 245 ,290, buy_cannon_image)
cannon_button.cost(33,-2,str(TURRET_DATA["TURRET_CANNON"][0].get('cost')), 18)
ice_button = Button(c.SCREEN_WIDTH - 122 ,290, buy_ice_image)
ice_button.cost(33,-2,str(TURRET_DATA["TURRET_ICE"][0].get('cost')), 18)
fire_button = Button(c.SCREEN_WIDTH - 245 ,360, buy_fire_image)
fire_button.cost(33,-2,str(TURRET_DATA["TURRET_FIRE"][0].get('cost')), 18)
earth_button = Button(c.SCREEN_WIDTH - 122 ,360, buy_earth_image)
earth_button.cost(33,-2,str(TURRET_DATA["TURRET_EARTH"][0].get('cost')), 18)
king_button = Button(c.SCREEN_WIDTH - 245 ,430, buy_king_image)
king_button.cost(33,-2,str(TURRET_DATA["KING"][0].get('cost')), 18)
market_button = Button(c.SCREEN_WIDTH - 122 ,430, buy_market_image)
market_button.cost(33,-2,str(TURRET_DATA["MARKET"][0].get('cost')), 18)

#selected tower
cancel_button = Button(c.SCREEN_WIDTH - 190 ,450, cancel_image, "CANCEL",0,0,"alt_font",24)
begin_button = Button(c.SCREEN_WIDTH - 242 ,670, start_image, "START ROUND",0,-2,"alt_font",30)
restart_button = Button(312.5 , 320, restart_image)
upgrade_button = Button(c.SCREEN_WIDTH - 210, 290, upgrade_image,"UPGRADE",0,-13, "alt_font",22)
sell_button = Button(c.SCREEN_WIDTH - 210, 360, sell_image, "SELL",0,-13,"alt_font",22)

#airstrike buttons
airstrike_ability = Button((c.SCREEN_WIDTH-c.SIDE_PANEL)/2 - 164, 5, arrow_strike_ability_image)
airstrike_ability.coin_cost(-22,44,8,45,str(AIRSTRIKE_DATA["airstrike_1"].get("cost")),18)
airstrike_ability2 = Button((c.SCREEN_WIDTH-c.SIDE_PANEL)/2 - 76, 5, ice_strike_ability_image)
airstrike_ability2.coin_cost(-22,44,8,45,str(AIRSTRIKE_DATA["airstrike_2"].get("cost")),18)
airstrike_ability3 = Button((c.SCREEN_WIDTH-c.SIDE_PANEL)/2 + 12, 5, fire_strike_ability_image)
airstrike_ability3.coin_cost(-22,44,8,45,str(AIRSTRIKE_DATA["airstrike_3"].get("cost")),18)
airstrike_ability4 = Button((c.SCREEN_WIDTH-c.SIDE_PANEL)/2 + 100, 5, earth_strike_ability_image)
airstrike_ability4.coin_cost(-22,44,8,45,str(AIRSTRIKE_DATA["airstrike_4"].get("cost")),18)
airstrike_cancel_button = Button((c.SCREEN_WIDTH-c.SIDE_PANEL)/2 - 60 ,25, cancel_image, "CANCEL",0,0,"alt_font",24)

#pause menu
pause_button = Button(5,5, pause_button_image)
exit_button = Button(5,5, exit_button_image)
resume_button = Button((c.SCREEN_WIDTH)/2 - 110, c.SCREEN_HEIGHT / 2 - 120, menu_base_button_image, "RESUME",0,0,'alt_font',30)
save_button = Button((c.SCREEN_WIDTH)/2 - 110, c.SCREEN_HEIGHT / 2 - 30, menu_base_button_image, "SAVE",0,0,'alt_font',30)
load_button = Button((c.SCREEN_WIDTH)/2 - 110, c.SCREEN_HEIGHT / 2 + 60, menu_base_button_image, "LOAD",0,0,'alt_font',30)
menu_button = Button((c.SCREEN_WIDTH)/2 - 110, c.SCREEN_HEIGHT / 2 + 150, menu_base_button_image, "MENU",0,0,'alt_font',30)
play_button = Button((c.SCREEN_WIDTH)/2 - 110, c.SCREEN_HEIGHT / 2, menu_base_button_image, "PLAY",0,0,'alt_font',30)
menu_load_button = Button((c.SCREEN_WIDTH)/2 - 110, c.SCREEN_HEIGHT / 2 + 100, menu_base_button_image, "LOAD",0,0,'alt_font',30)
quit_button = Button((c.SCREEN_WIDTH)/2 - 110, c.SCREEN_HEIGHT / 2 + 200, menu_base_button_image, "EXIT",0,0,'alt_font',30)
mute_button = Button(55,5,mute_button_image)
pressed_mute_button = Button(55,5, mute_button_pressed_image)

#sounds
cannon_shot = pg.mixer.Sound('assets/audio/cannon_Sound.mp3')
cannon_shot.set_volume(0.6)
archer_shot = pg.mixer.Sound('assets/audio/fire_archer_sound.mp3')
archer_shot.set_volume(0.3)
mage_shot = pg.mixer.Sound('assets/audio/mage_sound.mp3')
mage_shot.set_volume(0.7)
catapult_shot = pg.mixer.Sound('assets/audio/catapult_sound.mp3')
catapult_shot.set_volume(0.8)
place_turret_sound = pg.mixer.Sound('assets/audio/place_sound.mp3')

#music
Main_menu_song = pg.mixer.Sound('assets/audio/main_theme.mp3')
Buy_song = pg.mixer.Sound('assets/audio/buy_theme.mp3')
Battle_song = pg.mixer.Sound('assets/audio/battle_theme.mp3')

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
extra_large_font = pg.font.Font("assets/fonts/Amita-Regular.ttf", 48)
alt_text_font = pg.font.Font("assets/fonts/MedievalSharp-Book.ttf", 36)
error_font = pg.font.Font("assets/fonts/Aller_Bd.ttf", 24)
small_font = pg.font.Font("assets/fonts/Amita-Regular.ttf", 18)

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y, centered=False):
    img = font.render(text, True, text_col)
    text_rect = img.get_rect()
    
    if centered:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    
    screen.blit(img, text_rect)


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

def create_turret(mouse_pos,turret_name,animation_sheet=None,upgraded_animation_sheet=None,upgrade_level=None,sprite=None, sound= None, load = None):
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
          new_turret = Turret(animation_sheet, mouse_tile_x, mouse_tile_y,turret_name,upgraded_animation_sheet, upgrade_level,sound)
        else:
          new_turret = Tower(mouse_tile_x, mouse_tile_y,turret_name,sprite)
        if not load:
          place_turret_sound.play()
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
    sprite_sound = [[] for _ in range(1000)]
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
        sprite_sound[row] = mage_shot
      elif turret_type[row] == "TURRET_FIRE":
        sprite_sheet[row] = fire_sheet
        sprite_upgraded_sheet[row] = upgraded_fire_sheet
        sprite_sound[row] = archer_shot
      elif turret_type[row] == "TURRET_EARTH":
        sprite_sheet[row] = earth_sheet
        sprite_sound[row] = catapult_shot
        sprite_upgraded_sheet[row] = upgraded_earth_sheet
      elif turret_type[row] == "TURRET_CANNON":
        sprite_sheet[row] = cannon_sheet
        sprite_sound[row] = cannon_shot
        sprite_upgraded_sheet[row] = upgraded_cannon_sheet
    
    if rows > 0:
      for i in range(len(x)):
        if turret_type[i] == "KING":
          create_turret((int(x[i]) * c.TILE_SIZE, int(y[i]) * c.TILE_SIZE), turret_type[i], None, None,int(upgrade_level[i]), cursor_king, load = True)
        elif turret_type[i] == "MARKET":
          create_turret((int(x[i]) * c.TILE_SIZE, int(y[i]) * c.TILE_SIZE), turret_type[i], None, None,int(upgrade_level[i]), cursor_market,load = True)
        else:
          create_turret((int(x[i]) * c.TILE_SIZE, int(y[i]) * c.TILE_SIZE), turret_type[i], sprite_sheet[i], sprite_upgraded_sheet[i],int(upgrade_level[i]),sound=sprite_sound[i],load=True)
        print (turret_group)

  
def main_menu():
  Main_menu_song.play()
  global buy_round_song
  buy_round_song = False
  Buy_song.stop()
  Battle_song.stop()

  run2 = True
  menu_bg = pg.transform.scale(menu_background,(1024,768))
  while run2:
    screen.blit(menu_bg, (0,0))
    screen.blit(medieval, (c.SCREEN_WIDTH/2 - 200,100))
    screen.blit(meltdown, (c.SCREEN_WIDTH/2 - 220,210))
    if play_button.draw(screen):
      Main_menu_song.fadeout(5)
      return(1)
    if menu_load_button.draw(screen):
      load()
      Main_menu_song.fadeout(5)
      return(1)
    if quit_button.draw(screen):
      pg.quit()
    pg.display.flip()
    pg.time.delay(10)
    for event in pg.event.get():
    #quit program
      if event.type == pg.QUIT:
        pg.quit()

def reset_game():
  global game_over
  game_over = False
  global level_started
  level_started = False
  global placing_turrets
  placing_turrets = False
  global selected_turret
  selected_turret = None
  global last_enemy_spawn
  last_enemy_spawn = pg.time.get_ticks()
  global world
  world = World(world_data, map_image)
  world.process_data()
  world.process_enemies()
  #empty groups
  enemy_group.empty()
  turret_group.empty()


def muteGame():
  mage_shot.set_volume(0)
  archer_shot.set_volume(0)
  cannon_shot.set_volume(0)
  catapult_shot.set_volume(0)
  place_turret_sound.set_volume(0)
  Buy_song.set_volume(0)
  Battle_song.set_volume(0)

def unmuteGame():
  mage_shot.set_volume(0.7)
  archer_shot.set_volume(0.3)
  cannon_shot.set_volume(0.6)
  catapult_shot.set_volume(0.8)
  place_turret_sound.set_volume(1)
  Buy_song.set_volume(1)
  Battle_song.set_volume(1)

def buttons_draw2():
  if placing_ability == False:
    airstrike_ability.draw2(screen)
    airstrike_ability2.draw2(screen)
    airstrike_ability3.draw2(screen)
    airstrike_ability4.draw2(screen)

  if selected_turret is not None:
    #sidepanel with tower selected
    draw_text(str(selected_turret.type_name),alt_text_font, "grey100", 900, 260,centered=True) #draw name of tower type
    upgrade_button.draw2(screen)
    sell_button.draw2(screen)

  if not placing_turrets and selected_turret is None:
    #sidepanel default
    draw_text("BUY",alt_text_font,"grey100",900,260,centered=True)
    cannon_button.draw2(screen)
    ice_button.draw2(screen) 
    fire_button.draw2(screen) 
    earth_button.draw2(screen) 
    king_button.draw2(screen)
    market_button.draw2(screen)
  
  if not muted:
    mute_button.draw2(screen)
  else:
    pressed_mute_button.draw2(screen)



#game loop
run = True
while run:
  if menu_counter == 0 :
    menu_counter  = main_menu()

  if buy_round_song == False:
    Buy_song.play(20)
    buy_round_song = True
  
  

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
  screen.blit(health_bar_side_panel, (796, 88))
  screen.blit(gold_bar, (796, 155))

  #draw airstrike_banner
  screen.blit(airstrike_banner,((c.SCREEN_WIDTH-c.SIDE_PANEL)/2-200,c.SCREEN_HEIGHT-815))

  #draw game stats
  draw_text("Round", text_font, "grey100", 846, 32)
  draw_text(str(world.level), text_font, "grey100", 930, 32)
  draw_text(str(world.health), text_font, "grey100", 910, 119, centered=True)
  draw_text(str(world.money), text_font, "grey100", 910, 187, centered=True)

  index = len(health_bars) - 1
  while index >= 0:
    if health_bars[index].update(screen):
        health_bars.pop(index)
    index -= 1


  if game_over == False:
    #check if the level has been started or not
    if level_started == False:
      Battle_song.fadeout(5)
      if begin_button.draw(screen):
        last_enemy_spawn = pg.time.get_ticks()   
        Battle_song.play(20)
        Buy_song.fadeout(5)
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
          health_bars.append(HealthBar(enemy))
          enemy_group.add(enemy)
          world.spawned_enemies += 1
          last_enemy_spawn = pg.time.get_ticks()

    #check if wave is finished
    if world.check_level_complete() == True:
      buy_round_song = False
      world.money += c.LEVEL_COMPLETE_REWARD
      world.level += 1
      print (world.level)
      level_started = False
      last_enemy_spawn = pg.time.get_ticks()
      world.reset_level()
      if world.level <= c.TOTAL_LEVELS:
        world.process_enemies()

    #selected turret
    if placing_turrets == False:
        if selected_turret:
          selected_turret.selected = True
          draw_circ(200,200,200,selected_turret.range,(selected_turret.x, selected_turret.y)) #draw range circle
          draw_text(str(selected_turret.type_name),alt_text_font, "grey100", 900, 260,centered=True) #draw name of tower type

          #UPGRADE BUTTON
          #check if turret is upgradable
          if selected_turret.turret_type != "KING" and selected_turret.turret_type != "MARKET" and selected_turret.upgrade_level < 2:
            upgrade_button.coin_cost(-20,8,10,10,str(selected_turret.upgrade_cost), 20) #add coin & cost to button
            #set cost color based on available money
            if world.money < selected_turret.upgrade_cost:
              upgrade_button.change_cost_color("firebrick2")
            else:
              upgrade_button.change_cost_color("grey100")
            if upgrade_button.draw(screen):
              upgrade_turret(selected_turret)
          
          #SELL BUTTON
          sell_button.coin_cost(-20,8,10,10,"+"+str(selected_turret.sell_price()), 20) #add coin & sell price to button
          sell_button.change_cost_color("green1")
          if sell_button.draw(screen):
            sell_turret(selected_turret)
            selected_turret = None

          #CANCEL BUTTON
          if cancel_button.draw(screen):
            selected_turret = None

    #buy turrets
    if placing_turrets == False and selected_turret == None:
      #buy text
      draw_text("BUY",alt_text_font,"grey100",900,260,centered=True)
      #cannon
      if world.money < TURRET_DATA["TURRET_CANNON"][0]["cost"]:
        cannon_button.change_cost_color("firebrick2")
      else:
        cannon_button.change_cost_color("grey100")
      
      if cannon_button.Hovered():
        draw_text("Cannon Tower",alt_text_font,(255,255,255), 900,520, True)
        draw_text("This is a normal Tower",small_font,(255,255,255), 900,560, True)
        draw_text("It does small damage",small_font,(255,255,255), 900,590, True)
        draw_text("To every Type",small_font,(255,255,255), 900,620, True)

      if cannon_button.draw(screen):
        turret_equipped = TURRET_DATA.get("TURRET_CANNON", None)
        new_turret = Turret(cannon_sheet,0,0,turret_equipped[0]['name'],upgraded_cannon_sheet,1,cannon_shot)
        if world.money >= new_turret.cost:
          placing_turrets = True
        else:
          turret_equipped = None

      #ice mage
      if world.money < TURRET_DATA["TURRET_ICE"][0]["cost"]:
        ice_button.change_cost_color("firebrick2")
      else:
        ice_button.change_cost_color("grey100")

      if ice_button.Hovered():
        draw_text("Ice Mage",alt_text_font,(255,255,255), 900,520, True)
        draw_text("Deals more damage to Earth",small_font,(255,255,255), 900,560, True)
        draw_text("But deals less damage to Fire",small_font,(255,255,255), 900,590, True)

      if ice_button.draw(screen):
        turret_equipped = TURRET_DATA.get("TURRET_ICE", None)
        new_turret = Turret(ice_sheet,0,0,turret_equipped[0]['name'],upgraded_ice_sheet,1,mage_shot) 
        if world.money >= new_turret.cost:
          placing_turrets = True
        else:
          turret_equipped = None
      
      #fire archer
      if world.money < TURRET_DATA["TURRET_FIRE"][0]["cost"]:
        fire_button.change_cost_color("firebrick2")
      else:
        fire_button.change_cost_color("grey100")

      if fire_button.Hovered():
        draw_text("Fire Archer",alt_text_font,(255,255,255), 900,520, True)
        draw_text("Deals more damage to Ice",small_font,(255,255,255), 900,560, True)
        draw_text("But deals less damage to Earth",small_font,(255,255,255), 900,590, True)

      if fire_button.draw(screen):
        turret_equipped = TURRET_DATA.get("TURRET_FIRE", None)
        new_turret = Turret(fire_sheet,0,0,turret_equipped[0]['name'],upgraded_fire_sheet,1,archer_shot) 
        if world.money >= new_turret.cost:
          placing_turrets = True
        else:
          turret_equipped = None
      
      #earth catapult
      if world.money < TURRET_DATA["TURRET_EARTH"][0]["cost"]:
        earth_button.change_cost_color("firebrick2")
      else:
        earth_button.change_cost_color("grey100")

      if earth_button.Hovered():
        draw_text("Earth Catapult",alt_text_font,(255,255,255), 900,520, True)
        draw_text("Deals more damage to fire",small_font,(255,255,255), 900,560, True)
        draw_text("But deals less damage to Ice",small_font,(255,255,255), 900,590, True)

      if earth_button.draw(screen):
        turret_equipped = TURRET_DATA.get("TURRET_EARTH", None)
        new_turret = Turret(earth_sheet,0,0,turret_equipped[0]['name'],upgraded_earth_sheet,1, catapult_shot)
        
        if world.money >= new_turret.cost:
          placing_turrets = True
        else:
          turret_equipped = None
      
      #king
      if world.money < TURRET_DATA["KING"][0]["cost"]:
        king_button.change_cost_color("firebrick2")
      else:
        king_button.change_cost_color("grey100")

      if king_button.Hovered():
        draw_text("King",alt_text_font,(255,255,255), 900,520, True)
        draw_text("Towers placed within its range",small_font,(255,255,255), 900,560, True)
        draw_text("deal 2x the damage to enemies",small_font,(255,255,255), 900,590, True)

      if king_button.draw(screen):
        turret_equipped = TURRET_DATA.get("KING", None)
        new_turret = Tower(0,0,turret_equipped[0]['name'],cursor_king) 
        if world.money >= new_turret.cost:
          placing_turrets = True
        else:
          turret_equipped = None

      
      #market
      if world.money < TURRET_DATA["MARKET"][0]["cost"]:
        market_button.change_cost_color("firebrick2")
      else:
        market_button.change_cost_color("grey100")

      if market_button.Hovered():
        draw_text("Market",alt_text_font,(255,255,255), 900,520, True)
        draw_text("Towers placed within its range",small_font,(255,255,255), 900,560, True)
        draw_text("get twice the gold on kill",small_font,(255,255,255), 900,590, True)
      
      if market_button.draw(screen):
        turret_equipped = TURRET_DATA.get("MARKET", None)
        new_turret = Tower(0,0,turret_equipped[0]['name'],cursor_market) 
        if world.money >= new_turret.cost:
          placing_turrets = True
        else:
          turret_equipped = None
    
    if placing_turrets and placing_ability:
      placing_turrets = False

    #cursor blit
    if placing_turrets == True:
      cursort_rect = cursor_cannon.get_rect()
      cursor_pos = pg.mouse.get_pos()
      cursort_rect.center = cursor_pos
      if turret_equipped[0]['name'] == "TURRET_CANNON":
        screen.blit(cursor_cannon, cursort_rect)
      elif turret_equipped[0]['name'] == "TURRET_ICE":
        screen.blit(cursor_ice, cursort_rect) 
      elif turret_equipped[0]['name'] == "TURRET_FIRE":
        screen.blit(cursor_fire, cursort_rect)
      elif turret_equipped[0]['name'] == "TURRET_EARTH":
        screen.blit(cursor_earth, cursort_rect)
      elif turret_equipped[0]['name'] == "KING":
        screen.blit(cursor_king, cursort_rect)
      elif turret_equipped[0]['name'] == "MARKET":
        screen.blit(cursor_market, cursort_rect)
    


      if tile_occupied(cursor_pos):
        draw_circ(255,0,0,turret_equipped[0]['range'],cursor_pos) #draw turret range in red
      else:
        draw_circ(128,128,128,turret_equipped[0]['range'],cursor_pos) #draw turret range in white


      if cancel_button.draw(screen):
        placing_turrets = False

    #airstrikes
    if placing_ability == False:

      #airstrike 1
      if world.money < AIRSTRIKE_DATA["airstrike_1"]["cost"]:
        airstrike_ability.change_cost_color("firebrick2")
      else:
        airstrike_ability.change_cost_color("grey100")

      if airstrike_ability.Hovered():
        draw_text("Arrow Strike",alt_text_font,(255,255,255), 375,125, True)
  
      if airstrike_ability.draw(screen):
        new_aristrike = airstrike("airstrike_1")
        placing_ability = True

      #airstrike 2
      if world.money < AIRSTRIKE_DATA["airstrike_2"]["cost"]:
        airstrike_ability2.change_cost_color("firebrick2")
      else:
        airstrike_ability2.change_cost_color("grey100")
    
      if airstrike_ability2.Hovered():
        draw_text("Avalanche",alt_text_font,(255,255,255), 375,125, True)

      if airstrike_ability2.draw(screen):
        new_aristrike = airstrike("airstrike_2")
        placing_ability = True

      #airstrike 3
      if world.money < AIRSTRIKE_DATA["airstrike_3"]["cost"]:
        airstrike_ability3.change_cost_color("firebrick2")
      else:
        airstrike_ability3.change_cost_color("grey100")

      if airstrike_ability3.Hovered():
        draw_text("Fire Nova",alt_text_font,(255,255,255), 375,125, True)

      if airstrike_ability3.draw(screen):
        new_aristrike = airstrike("airstrike_3")
        placing_ability = True

      #airstrike 4
      if world.money < AIRSTRIKE_DATA["airstrike_4"]["cost"]:
        airstrike_ability4.change_cost_color("firebrick2")
      else:
        airstrike_ability4.change_cost_color("grey100")

      if airstrike_ability4.Hovered():
        draw_text("Rockfall",alt_text_font,(255,255,255), 375,125, True)
      if airstrike_ability4.draw(screen):
        new_aristrike = airstrike("airstrike_4")
        placing_ability = True


    if placing_ability:
      cursor_pos = pg.mouse.get_pos()

      if world.money >= new_aristrike.cost:
        if airstrike_cancel_button.draw(screen):
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
    
    if muted == True:
      if pressed_mute_button.draw(screen):
        muted = False
        unmuteGame()
    else:
      if mute_button.draw(screen):
        muted = True
        muteGame()


  else:
    #game is over
    if paused == True:
  
      buttons_draw2()


      if placing_ability or selected_turret or placing_turrets:
        cancel_button.draw2(screen)
      
      if level_started == False:
        begin_button.draw2(screen)
        draw_circ(0,0,0,1000,(c.SCREEN_WIDTH/2,c.SCREEN_HEIGHT/2))

        #load button
        if load_button.font_color != "grey100":
          load_button.change_text_color("grey100")
        if load_button.draw(screen):
          load()
          selected_turret = None
          placing_ability = False
          placing_turrets = False
        
        #save button
        if save_button.font_color != "grey100":
          save_button.change_text_color("grey100")
        if save_button.draw(screen):
          save()

      draw_text("Paused",extra_large_font, "grey100", (c.SCREEN_WIDTH/2), 180, centered=True)#draw "PAUSED" text
      
      if level_started == True:
        draw_circ(0,0,0,1000,(c.SCREEN_WIDTH/2,c.SCREEN_HEIGHT/2))
        
        #load button
        if load_button.font_color != "grey60":
          load_button.change_text_color("grey60")
        if load_button.draw2(screen):
            save_error = True

        #save button
        if save_button.font_color != "grey60":
          save_button.change_text_color("grey60")
        if save_button.draw2(screen):
            save_error = True
            
        if save_error == True:
          draw_text("Can't save or load while in a round", error_font, (0, 0, 0), 250, 450)
          draw_text("Wait until the end", error_font, (0, 0, 0), 350, 500)

      if resume_button.draw(screen):
          save_error = False
          paused = False
          game_over = False

      if menu_button.draw(screen):
        reset_game()
        paused = False
        main_menu()

      

      exit_button.draw2(screen)

    
    if paused == False and game_over == True:
      Battle_song.stop()
      Buy_song.stop()

      buttons_draw2()
      draw_circ(0,0,0,1000,(c.SCREEN_WIDTH/2,c.SCREEN_HEIGHT/2))
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
        buy_round_song = False
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
        if not paused and not game_over:
          selected_turret = None
          clear_selected()
          if placing_turrets == True:
            #check if support tower
            if turret_equipped[0]['name'] == "KING":
              place_turret = create_turret(mouse_pos, turret_equipped[0]['name'],None, None, None, cursor_king)
            elif turret_equipped[0]['name'] == "MARKET":
              place_turret = create_turret(mouse_pos, turret_equipped[0]['name'],None, None, None, cursor_market)
            else: #damage tower
              place_turret = create_turret(mouse_pos,turret_equipped[0]['name'],new_turret.sprite_sheet,new_turret.sprite_upgraded_sheet,1, sound = new_turret.sound)
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