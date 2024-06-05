import pygame as pg

class Button():
    def __init__(self,x,y,image, text='', text_x_offset=0, text_y_offset=0, type='', font_size=32):
        self.image = image
        self.rect = self.image.get_rect()
        self.clicked = False
        self.rect.topleft = (x,y)
        self.text = text
        self.font = pg.font.Font("assets/fonts/Amita-Regular.ttf", 18)
        self.alt_font = pg.font.Font("assets/fonts/MedievalSharp-Book.ttf", font_size)
        self.font_color = "grey100"
        self.y_offset = text_y_offset
        self.x_offset = text_x_offset
        self.type = type
        
        #coin and cost
        self.has_coin_cost = False
        self.coin_image = pg.image.load('assets/images/ui_backgrounds/coin.png')
        self.coin_rect = self.rect.copy()
        self.cost_text = 'N/A'
        self.cost_color = "grey100"
        self.cost_text_x = 0
        self.cost_text_y = 0
        self.cost_size = 24
        self.cost_font = pg.font.Font("assets/fonts/Amita-Regular.ttf", self.cost_size)

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
            if self.type == "alt_font":
                self.font = self.alt_font
            elif self.type == "alt_font_with_coin": #adds coin with alt font for side panel buttons
                self.font = self.alt_font
                coin_rect = self.rect.copy()
                coin_rect.y += 30
                coin_rect.x += 55
                surface.blit(self.coin_image, coin_rect)
            text_surface = self.font.render(self.text, True, self.font_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            text_rect.x += self.x_offset #move the text right
            text_rect.y += self.y_offset #move text down
            surface.blit(text_surface, text_rect)
        
        if self.has_coin_cost:
            print("has coin cost!")
            cost_text_surface = self.cost_font.render(self.cost_text, True, self.cost_color)
            cost_text_rect = cost_text_surface.get_rect(center=self.rect.center)
            cost_text_rect.x = self.cost_text_x
            cost_text_rect.y = self.cost_text_y
            surface.blit(cost_text_surface, cost_text_rect)
            surface.blit(self.coin_image, coin_rect)


        #render coin if airstrike
        if self.type == 'airstrike':
            coin_rect = self.rect.copy()
            coin_rect.y += 66
            surface.blit(self.coin_image, coin_rect)
        
        return action
    
    def draw2(self,surface):
        surface.blit(self.image, self.rect)
        if self.text:
            text_surface = self.font.render(self.text, True, self.font_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            text_rect.x += self.x_offset #move the text right
            text_rect.y += self.y_offset #move text down
            surface.blit(text_surface, text_rect)

    def font_red(self):
        self.font_color = "firebrick2"
    
    def font_white(self):
        self.font_color = "grey100"

    def coin_cost(self,coin_x,coin_y, text_x, text_y, cost='', color='grey100', size=24):
        self.has_coin_cost = True
        self.coin_rect.x += coin_x
        self.coin_rect.y += coin_y
        self.cost_text = cost
        self.cost_color = color
        self.cost_text_x = text_x
        self.cost_text_y = text_y
        self.cost_size = size
        