import pygame as pg
import constants as c
import math as math
from airstrike_data import AIRSTRIKE_DATA

class airstrike ():
    def __init__(self,airstrike_name):
        self.type = AIRSTRIKE_DATA.get(airstrike_name, [])
        self.damage = self.type.get("damage")
        self.size = self.type.get("size")
        self.cooldown = self.type.get("cooldown")
        self.cost = self.type.get("cost")
        self.waves = self.type.get("waves")
        self.last_shot = 0
        self.shots_fired = 0
        self.running = False
        self.next_shot_time = 0

    def wait(self,wait_time, start_time):
        return pg.time.get_ticks() >= start_time + wait_time

    def draw_circ(self,R,G,B,Size,location,screen,):
        transparent_surface = pg.Surface((c.SCREEN_WIDTH, c.SCREEN_HEIGHT), pg.SRCALPHA)
        transparent_surface.fill((0, 0, 0, 0))
        pg.draw.circle(transparent_surface, (0, 0, 0, 100), location, Size + 2)
        pg.draw.circle(transparent_surface, (R, G, B, 70), location, Size)
        screen.blit(transparent_surface, (0, 0))
        

        
    def place_ability(self, enemy_group, screen):
        current_time = pg.time.get_ticks()
        
        if self.running and self.wait(self.cooldown, self.next_shot_time):
            cursor_pos = pg.mouse.get_pos()
            for enemy in enemy_group:
                if enemy.health > 0:
                    x_dist = enemy.pos[0] - cursor_pos[0]
                    y_dist = enemy.pos[1] - cursor_pos[1]
                    dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                    if dist < self.size:
                        enemy.health -= self.damage
            self.draw_circ(123, 123, 123, self.size, cursor_pos, screen)
            self.last_shot = current_time
            self.shots_fired += 1
            if self.shots_fired >= self.waves:
                self.running = False
            else:
                self.next_shot_time = current_time


    def start(self):
        self.running = True
        self.shots_fired = 0
        self.next_shot_time = pg.time.get_ticks()




    

 



