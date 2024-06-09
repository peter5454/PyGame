import pygame as pg



class HealthBar():
    def __init__(self,enemy):
        self.enemy = enemy
        self.x = 0
        self.y = 0
        self.hp = enemy.health
        self.max_hp = enemy.max_health
        self.w = 40
        self.h = 5
    

    def draw(self, surface):
        #calculate health ratio
        ratio = self.hp / self.max_hp
        pg.draw.rect(surface, "red", (self.x-20, self.y-30, self.w, self.h))
        pg.draw.rect(surface, "green", (self.x-20, self.y-30, self.w * ratio, self.h))

    def update(self,surface):
        self.x,self.y = self.enemy.get_coords()
        self.hp = self.enemy.health
        print (self.enemy)
        if self.enemy.health <=0 or self.enemy.finished == True or not self.enemy.groups():
            return True
        self.draw(surface)
        return False