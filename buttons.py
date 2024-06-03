import pygame as pg

class Button():
    def __init__(self,x,y,image, text='', x_offset=0, y_offset=0, type=''):
        self.image = image
        self.rect = self.image.get_rect()
        self.clicked = False
        self.rect.topleft = (x,y)
        self.text = text
        self.font = pg.font.Font("assets/fonts/Amita-Regular.ttf", 18)
        self.alt_font = pg.font.Font("assets/fonts/MedievalSharp-Book.ttf", 32)
        self.y_offset = y_offset
        self.x_offset = x_offset
        self.coin_image = pg.image.load('assets/images/ui_backgrounds/coin.png')
        self.type = type


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
        
        #render text
        if self.text:
            if self.text == "START ROUND":
                self.font = self.alt_font
            text_surface = self.font.render(self.text, True, "grey100")
            text_rect = text_surface.get_rect(center=self.rect.center)
            text_rect.x += self.x_offset #move the text right
            text_rect.y += self.y_offset #move text down
            surface.blit(text_surface, text_rect)
        
        #render coin if airstrike
        if self.type == 'airstrike':
            coin_rect = self.rect.copy()
            coin_rect.y += 66
            surface.blit(self.coin_image, coin_rect)
        
        return action
    def draw2(self,surface):
        surface.blit(self.image, self.rect)
        if self.text:
            text_surface = self.font.render(self.text, True, "grey100")
            text_rect = text_surface.get_rect(center=self.rect.center)
            text_rect.x += self.x_offset #move the text right
            text_rect.y += self.y_offset #move text down
            surface.blit(text_surface, text_rect)


        