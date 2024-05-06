import pygame as pg

class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self, surface):
        pos = pg.mouse.get_pos()
        
        #check colission for button and mouse pressed
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1:
                pass
        #draw button on top
        surface.blit(self.image, self.rect)

        