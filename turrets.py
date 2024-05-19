import pygame as pg

class Turret(pg.sprite.Sprite):
    def __init__(self,image,pos):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.range = 90
        self.selected = False

    #def pick_target(self, enemy_group):
