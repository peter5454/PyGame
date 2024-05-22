import pygame as pg
import constants as c
import math as math
from turrets_data import TURRET_DATA

class Turret(pg.sprite.Sprite):


    def __init__(self,image,tile_x,tile_y):
        pg.sprite.Sprite.__init__(self)
        self.tile_x = tile_x
        self.tile_y = tile_y

        #calculate center coordinates
        self.x = (self.tile_x + 0.5) * c.TILE_SIZE
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE
        self.original_image = image
        self.image = image

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
        self.upgrade_level = 1
        self.max_level = len(TURRET_DATA)
        self.range = 90
        self.angle = 0
        self.selected = False
        self.target = None
        self.cooldown = TURRET_DATA[self.upgrade_level - 1].get("cooldown")
        self.damage = TURRET_DATA[self.upgrade_level - 1].get("damage")
        self.cost = TURRET_DATA[self.upgrade_level - 1].get("cost")
        self.upgrade_cost = TURRET_DATA[self.upgrade_level - 1].get("upgrade_cost")
        self.last_shot = pg.time.get_ticks()
        self.tower_value = self.cost

    def update (self, enemy_group):
        if pg.time.get_ticks() - self.last_shot >self.cooldown:
            self.pick_target(enemy_group)
            if self.target:
                i = 0 #animation goes here


    def pick_target(self, enemy_group):
        closest_enemy = None
        closest_distance = self.range
        for enemy in enemy_group:
            x_dist = enemy.pos[0] - self.x
            y_dist = enemy.pos[1] - self.y
            dist = (x_dist ** 2 + y_dist ** 2) ** 0.5
            if dist < closest_distance:
                closest_distance = dist
                closest_enemy = enemy
        self.target = closest_enemy

        if self.target:
            x_dist = self.target.pos[0] - self.x
            y_dist = self.target.pos[1] - self.y
            self.angle = math.degrees(math.atan2(-y_dist, x_dist))
            self.rotate_image()
            self.target.health -= self.damage
            self.last_shot = pg.time.get_ticks()

    def rotate_image(self):
        """ Rotate the image to face the target """
        self.image = pg.transform.rotate(self.original_image, self.angle-90)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def upgrade(self):
        self.upgrade_level += 1
        self.cooldown = TURRET_DATA[self.upgrade_level - 1]["cooldown"]
        self.damage = TURRET_DATA[self.upgrade_level - 1]["damage"]
        self.upgrade_cost = TURRET_DATA[self.upgrade_level - 1]["upgrade_cost"]
        self.tower_value += TURRET_DATA[self.upgrade_level - 2]["upgrade_cost"]
    
    def sell(self):
        cost = self.tower_value
        print (cost)
        self.kill()
        return(round(cost*0.8))
            
