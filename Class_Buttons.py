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

    def spoof_text(self, previous_lenght):
        for i in range(len(self.text) - previous_lenght):
            self.text_spoof += "*"

class Messages:
    def __init__(self, coords, size, font, text = [], color = "black", set_timeout = False, activable = False):
        self.coords = coords
        self.size = size

        self.text = text
        self.font = font
        self.color = color

        self.active = False
        self.activable = activable
        
        self.set_timeout = set_timeout
        self.timeout = 0
        self.previous_text = ''
        

    def draw(self, app, row_id = []):
        line_offset = 0
        # Make message disappear after set frames
        if not self.text or self.text != self.previous_text:
            self.timeout = 200
            self.previous_text = self.text
        if self.timeout == 0:
            self.text = ''

        if self.timeout > 0:
            self.line_objs = [] 
            i = 0
            line_id = []
            for line in self.text:
                if row_id:
                    line_id = row_id[i]
                self.line_objs.append(Line_obj((self.coords[0], self.coords[1]+line_offset), (self.size[0], self.size[1]), line,self.font, self.color, self.activable, line_id))
                self.line_objs[-1].draw(app)
                line_offset += 20
                i += 1
                
            if self.set_timeout:
                self.timeout -= 1

class Line_obj:
    def __init__(self, coords, size, text, font, color, activable, line_id = None):
        self.text = text

        self.active = False
        self.activable = activable

        self.font = font
        self.color = color

        self.COLOR_ACTIVE= 'lightblue'
        self.COLOR_INACTIVE = color

        self.rect = pygame.Rect(coords[0], coords[1], size[0], size[1])

        self.line_id = line_id

    def draw(self, app):
        if self.active and self.activable:
            self.color = self.COLOR_ACTIVE
        else:
            self.color = self.COLOR_INACTIVE

        text_render = self.font.render(self.text, True, self.color)
        app.screen.blit(text_render, self.rect)