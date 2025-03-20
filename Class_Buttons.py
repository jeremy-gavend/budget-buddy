import pygame

class Buttons:
    def __init__(self, coords, size, text, text_font, text_color = 'black', link_to = ''):
        self.coords = coords
        self.size = size
        self.text = text
        self.link_to = link_to

        self.rect = pygame.Rect(coords[0], coords[1], size[0], size[1])
        self.text_render = text_font.render(self.text, True, text_color)

    def draw(self, app):
        app.screen.blit(self.text_render, self.rect)
    
    # TODO put them in a dict with label as index, not in a list
    # size, position, draw method + text if any,  

class Textbox:
    def __init__(self, coords, size, text_font, text_color = 'black', label = '', label_font = '', label_color = 'black', tab_to = '' ):
        self.coords = coords
        self.size = size
        
        self.label = label
        self.label_font = label_font
        self.label_color = label_color
        self.label_rect = pygame.Rect(coords[0], coords[1]-50, size[0], size[1])

        self.rect = pygame.Rect(coords[0], coords[1], size[0], size[1])

        self.text = ''
        self.text_spoof = ''
        self.text_font = text_font
        self.text_color = text_color
        self.color = 'lightgray'

        self.active = False
        self.tab_to = tab_to

        self.COLOR_ACTIVE= 'lightblue'
        self.COLOR_INACTIVE = 'lightgray'

    def draw(self, app, index):
        if self.active:
            self.color = self.COLOR_ACTIVE
        else:
            self.color = self.COLOR_INACTIVE

        pygame.draw.rect(app.screen, self.color, self.rect)
        if index == 'password' or index == 'confirm_password':
            text_render = self.text_font.render(self.text_spoof, True, self.text_color)
        else:
            text_render = self.text_font.render(self.text, True, self.text_color)
        app.screen.blit(text_render, self.rect)
        
        if self.label:
            label_render = self.label_font.render(self.label, True, self.label_color)
            app.screen.blit(label_render, self.label_rect)

    def activate(self):
        pass #event

    def spoof_text(self):
        pass #event


# self.active, need to change color when active