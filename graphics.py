import pygame
import sys
from util import *
from graphic_components import *
from weather_management import weather_management
from settings import *

# handles rendering, pygame, graphical components
# interacts with the weather_management class
class graphics:
    # Sets up Pygame and Screen
    def __init__(self, res:tuple, name:str) -> None:
        # initializing pygame
        pygame.init()

        # window sets caption
        pygame.display.set_caption(name)

        # stores resolution | please keep this constant
        self.res = res

        # opens up a window
        self.screen = pygame.display.set_mode(res)
        
        # sets icon
        icon = pygame.image.load(APP_ICON_PATH).convert_alpha()
        pygame.display.set_icon(icon)

        # background colors
        self.background_colors = BACKGROUND_COLORS
        
        # typing variables
        self.typing_text = ''
        self.typing = False

        # parses weather data    
        self.data = get_current_weather_from_coords()
        self.weather_manager = weather_management(self.data)

        # sets weather data into graphic components 
        self.set_weather_data() 
        
    # grabs and sets the weather_data after its been parsed
    def set_weather_data(self) -> None:
        # gets graphics components
        graphics_components = self.weather_manager.get_graphic_components()
        # transfers components
        self.buttons = graphics_components[0]
        self.texts = graphics_components[1]
        self.images = graphics_components[2]
        # keyboard only exists for readability
        self.keyboard = self.buttons[0] 
        self.keyboard.add_event(self.start_typing)

    # starts the typing process by setting a flag and removing text from keyboard
    def start_typing(self) -> None:
        self.typing = True
        if self.typing_text == '':
            # resets text and sets typing text offset
            self.keyboard.update_text('', text_offset=(10, 20))

    # gets the background by lerping through self.background_colors
    def get_background_color(self) -> tuple:
        # holds color size
        color_size = len(self.background_colors)
        slow_rate = 1000
        # gets time then clamps it then slows it down
        t = (pygame.time.get_ticks() % (slow_rate * color_size)) / slow_rate
        
        # vector3 lerp a to b by t
        def lerp(a:tuple, b:tuple, t:float) -> tuple:
            x = (1 - t) * a[0] + t * b[0]
            y = (1 - t) * a[1] + t * b[1]
            z = (1 - t) * a[2] + t * b[2]
            return (x, y, z)

        # finds correct range for the lerp
        for i in range(0, color_size + 1):
            if t < i:
                # lerps and returns
                return lerp(self.background_colors[i % color_size], self.background_colors[(i + 1) % color_size], t - (i - 1))
        
    # calls the weather api with city name
    # if fails resets keyboard text to tell user
    def find_city(self, city_name:str) -> None:
        data = request_current_weather_from_name(city_name)
        if data == None:
            # tells user place no found
            self.keyboard.update_text('Place doesn\'t exist try again', text_offset=(160, 20))
        else:
            # reinitializes weather_manager
            self.weather_manager.__init__(data)
            # sets up data
            self.set_weather_data()
            

    # game loop
    # manages rendering calls, input, and 
    def run(self) -> None:
        # gets mouse position
        mouse_pos = pygame.mouse.get_pos()

        # iterates through events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # quits everything
                pygame.quit()
                sys.exit()
            
            # keyboard typing logic
            if self.typing:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # send data
                        self.find_city(self.typing_text)

                        # resets typing flags
                        self.typing = False
                        self.typing_text = ''

                        # this break is required because backend can change substantiatly after find_city()
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        # removes last element
                        self.typing_text = self.typing_text[:-1]
                    # if character, space, dash, comma, or single quote | I can't multiline this for some reason
                    elif pygame.K_a <= event.key <= pygame.K_z or event.key == pygame.K_SPACE or event.key == pygame.K_COMMA or event.key == pygame.K_MINUS or event.key == pygame.K_QUOTE:
                        # adds character to text 
                        self.typing_text += event.unicode
                    # updates keyboard text to current input
                    self.keyboard.update_text(self.typing_text)
                    

            #checks if a mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                # click anywhere stops typing
                if self.typing:
                    self.typing = False
                # iterates through buttons for mouse click collisions    
                for button in self.buttons:
                    if button.colliding(mouse_pos):
                        button.clicked()

        # sets background color    
        self.screen.fill(self.get_background_color())

        # renders buttons
        for button in self.buttons:
            button.render(self.screen, mouse_pos)

        # renders images
        for image in self.images:
            image.render(self.screen)

        # renders texts
        for text in self.texts:
            text.render(self.screen)

        # updates the frames of the game
        pygame.display.flip()  
