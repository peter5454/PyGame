import pygame as pg



class HealthBar():
    def __init__(self,enemy):
        self.enemy = enemy
        self.x = 0
        self.y = 0
        self.hp = enemy.health
        self.max_hp = enemy.max_health
        self.w = 50
        self.h = 10
    

    def draw(self, surface):
        #calculate health ratio
        ratio = self.hp / self.max_hp
        pg.draw.rect(surface, "red", (self.x, self.y-20, self.w, self.h))
        pg.draw.rect(surface, "green", (self.x, self.y-20, self.w * ratio, self.h))

    def update(self,surface):
        self.x,self.y = self.enemy.get_coords()
        self.hp = self.enemy.health
        if self.enemy.health <=0 or self.enemy.finished == True:
            return True
        self.draw(surface)
        return False