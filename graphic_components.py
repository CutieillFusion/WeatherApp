import pygame
from settings import*

# these are all different classes because the abstraction creates complication
# its sadly not a zero cost abstraction since each subcomponent can be treated completely differently

# button class
# uses colored rects and texts with collision to create a button
# read more about text in text class
class button:
    def __init__(self, position:tuple, size:tuple, button_light:tuple, button_dark:tuple, 
                 text:str=None, font_name:str=DEFAULT_FONT, font_size:int=25, font_color:tuple=DEFAULT_FONT_COLOR, text_offset:tuple=(0, 0)) -> None:
        # ui control
        self.position = position
        self.size = size

        # visuals
        self.button_light = button_light
        self.button_dark = button_dark

        # button event
        self.event = None

        # text init
        self.update_text(text, font_name, font_size, font_color, text_offset)

    # adds function pointer to create button events
    def add_event(self, event:any=None) -> None:
        self.event = event

    # allows the user to redefine the text on the button
    def update_text(self, text:str=None, font_name:str=None, font_size:int=None, font_color:tuple=None, text_offset:tuple=None) -> None:
        # turns on or off text
        self.text_active = text != None
        # fine tuning position
        if text_offset != None:
            self.text_offset = text_offset 
        # font data
        if font_name != None and font_size != None:
            self.font = pygame.font.SysFont(font_name, font_size)
        if font_color != None:
            self.font_color = font_color
        # creates text object
        if text != None:
            self.text = self.font.render(text, True, self.font_color)

    # renders button, first the rect then text
    def render(self, screen:pygame.Surface, mouse_pos:tuple) -> None:
        # AABB collision
        if self.colliding(mouse_pos):
            pygame.draw.rect(screen, self.button_light, [self.position[0], self.position[1], self.size[0], self.size[1]])
        else:
            pygame.draw.rect(screen, self.button_dark, [self.position[0], self.position[1], self.size[0], self.size[1]])
        # has to be after button draw so text can appear infront
        if self.text_active:
            screen.blit(self.text, (self.position[0] + self.text_offset[0], self.position[1] + + self.text_offset[1]))

    # checks to see if the button is colliding
    def colliding(self, mouse_pos:tuple) -> bool:
        # AABB collision if button is clicked
        return self.position[0] <= mouse_pos[0] <= self.position[0] + self.size[0] and self.position[1] <= mouse_pos[1] <= self.position[1] + self.size[1]          
            

    # runs events if set by add_event
    def clicked(self) -> None:
        if self.event != None:
            self.event()

# image class
# blits a surface to the screen based off position
class image:
    # size will resize the surface if they don't match
    def __init__(self, position:tuple, size:tuple, surface:pygame.surface) -> None:
        # ui
        self.position = position
        
        # visuals
        self.surface = surface
        
        # scale
        if surface.get_size() != size:
            self.surface =  pygame.transform.scale(self.surface, size)
        self.size = size

    # renders image to the screen
    def render(self, screen:pygame.Surface) -> None:
        screen.blit(self.surface, self.position)

# text class
# displays text to the screen
class text:
    def __init__(self, position:tuple, text:str, font_name:str=DEFAULT_FONT, font_size:int=25, 
                 font_color:tuple=DEFAULT_FONT_COLOR, text_offset:tuple=(0, 0)) -> None:
        # ui 
        self.position = position

        # text init
        self.update_text(text, font_name, font_size, font_color, text_offset)

    # allows the user to redefine the text on the button 
    def update_text(self, text:str=None, font_name:str=None, font_size:int=None, font_color:tuple=None, text_offset:tuple=None) -> None:
        # fine tuning position
        if text_offset != None:
            self.text_offset = text_offset 
        # font data
        if font_name != None and font_size != None:
            self.font = pygame.font.SysFont(font_name, font_size)
        if font_color != None:
            self.font_color = font_color
        # creates text object
        if text != None:
            self.text = self.font.render(text, True, self.font_color)

    # blits image to screen based off position and text_offset
    def render(self, screen:pygame.Surface) -> None:
        screen.blit(self.text, (self.position[0] + self.text_offset[0], self.position[1] + self.text_offset[1]))