import pygame as pg

class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.clicked = False
        self.rect.topleft = (x,y)

    def draw(self, surface):
        action = False
        pos = pg.mouse.get_pos()
        button_state = pg.mouse.get_pressed()[0] == 1
        #check colission for button and mouse pressed
        if self.rect.collidepoint(pos):
            if button_state and not self.prev_button_state: #if button is not the same as previous state
                self.clicked = True
            elif not button_state and self.clicked: #if button isn't clicked and mouse not pressed down
                action = True
                self.clicked = False
        
        self.prev_button_state = button_state #gets previous state of button

        if self.clicked:
            scaled_image = pg.transform.scale(self.image, (self.rect.width - 5, self.rect.height - 5))
            surface.blit(scaled_image, self.rect)
        else:
            surface.blit(self.image, self.rect)
        
        return action


        