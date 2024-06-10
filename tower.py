import pygame as pg
import constants as c
import math as math
from turrets_data import TURRET_DATA

class Tower(pg.sprite.Sprite):


    def __init__(self,tile_x,tile_y,Turret_type,sprite=None):
        pg.sprite.Sprite.__init__(self)
        self.tile_x = tile_x
        self.tile_y = tile_y

        #calculate center coordinates
        self.x = (self.tile_x + 0.5) * c.TILE_SIZE
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE


        #image
        self.image = sprite
        
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        #variables       
        self.selected = False
        self.target = None
        self.type = TURRET_DATA.get(Turret_type, [])
        self.range = self.type[0].get("range")
        self.upgrade_level = 1
        self.turret_type = Turret_type
        self.cost = self.type[0].get("cost")
        self.tower_value = self.cost
        self.type_name = self.type[0].get("type_name")


    def update_king(self, turret_group):
        x_dist = 0
        y_dist = 0
    #check distance to each tower to see if it is in range
        for tower in turret_group:
            #print(tower.type[0]['name'])
            if tower.type[0]['name'] != "KING" and tower.type[0]['name'] != "MARKET":
                x_dist = tower.x - self.x
                y_dist = tower.y - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                #change damage multiplier for towers in range
                if dist < self.range:
                    tower.damage_multiplier = 2
    
    def update_market(self, turret_group):
        x_dist = 0
        y_dist = 0
    #check distance to each tower to see if it is in range
        for tower in turret_group:
            #print(tower.type[0]['name'])
            if tower.type[0]['name'] != "KING" and tower.type[0]['name'] != "MARKET":
                x_dist = tower.x - self.x
                y_dist = tower.y - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                #change reward multiplier for towers in range
                if dist < self.range:
                    tower.reward_multiplier += 1

    def draw(self, surface):
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)
        

    def sell(self):
        cost = self.tower_value
        print (cost)
        self.kill()
        return(round(cost*0.65))

    def sell_price(self):
        return(round(self.tower_value*0.65))
            
