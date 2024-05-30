import pygame as pg
import constants as c
import math as math
from tower import Tower
from turrets_data import TURRET_DATA

class Turret(Tower):


    def __init__(self,sprite_sheet,tile_x,tile_y,Turret_type,sprite_upgraded_sheet):
        pg.sprite.Sprite.__init__(self)
        self.tile_x = tile_x
        self.tile_y = tile_y

        #calculate center coordinates
        self.x = (self.tile_x + 0.5) * c.TILE_SIZE
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE


        #animation
        self.sprite_sheet = sprite_sheet
        self.animation_list = self.load_images()
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        #upgraded animation
        self.sprite_upgraded_sheet = sprite_upgraded_sheet

        #image
        self.angle = 90
        self.original_image = self.animation_list[self.frame_index]
        self.image = pg.transform.rotate(self.original_image, self.angle)
        
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        #variables       
        self.upgrade_level = 1
        self.max_level = len(TURRET_DATA)
        self.selected = False
        self.target = None
        self.type = TURRET_DATA.get(Turret_type, [])
        self.range = self.type[self.upgrade_level - 1].get("range")


        self.cooldown = self.type[self.upgrade_level - 1].get("cooldown")
        self.damage = self.type[self.upgrade_level - 1].get("damage")
        self.damage_multiplier = 1
        self.cost = self.type[self.upgrade_level - 1].get("cost")
        self.upgrade_cost = self.type[self.upgrade_level - 1].get("upgrade_cost")
        self.last_shot = pg.time.get_ticks()
        self.tower_value = self.cost
        


    def load_images(self):
        #extract individual images from he sprite sheet
        size = self.sprite_sheet.get_height()
        animation_list = []
        for x in range (c.ANIMATION_STEPS):
            temp_img = self.sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list
    
    def update(self, enemy_group):
        if self.target:
            self.play_animation()
        else:
      #search for new target once turret has cooled down
            if pg.time.get_ticks() - self.last_shot > (self.cooldown):
                self.pick_target(enemy_group)
        #print(self.damage_multiplier)

    def pick_target(self, enemy_group):
        x_dist = 0
        y_dist = 0
    #check distance to each enemy to see if it is in range
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.target = enemy
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
          #damage enemy
                    self.target.health -= self.damage * self.damage_multiplier
                    break

    def play_animation(self):
    #update image
        self.original_image = self.animation_list[self.frame_index]
    #check if enough time has passed since the last update
        if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
      #check if the animation has finished and reset to idle
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
        #record completed time and clear target so cooldown can begin
                self.last_shot = pg.time.get_ticks()
                self.target = None
            


    def draw(self, surface):
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)
        
    def upgrade(self):
        self.upgrade_level += 1
        self.range = self.type[self.upgrade_level - 1].get("range")
        self.cooldown = self.type[self.upgrade_level - 1]["cooldown"]
        self.damage = self.type[self.upgrade_level - 1]["damage"]
        self.upgrade_cost = self.type[self.upgrade_level - 1]["upgrade_cost"]
        self.tower_value += self.type[self.upgrade_level - 2]["upgrade_cost"]
        self.sprite_sheet = self.sprite_upgraded_sheet
        self.animation_list = self.load_images()
        self.original_image = self.animation_list[self.frame_index]

    def sell(self):
        cost = self.tower_value
        print (cost)
        self.kill()
        return(round(cost*0.8))
            
