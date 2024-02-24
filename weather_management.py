from graphics import *
from graphic_components import *
from settings import *

# manages the datas interaction with the graphics class and converts data into variables
# all variables are stored as strings internally for easy of output
class weather_management:
    def __init__(self, data:dict) -> None:
        #parses data
        self.data = data
        self.parse_data(data)
        
        # main font
        self.main_font = DEFAULT_FONT

        # white color
        self.font_color = DEFAULT_FONT_COLOR

        # starting units
        self.tempature_unit = 'F°'
        self.speed_unit = 'mph'

        # creates graphical components
        self.create_buttons()
        self.create_texts()
        self.create_images()

    # parses data into variables stored as strings 
    def parse_data(self, data:dict) -> None:
        # inner functions used for conversion
        kelvin_to_celsius_constant = 273.15
        def kelvin_to_celsius(kelvin) -> float:
            return round(kelvin - kelvin_to_celsius_constant)
        def kelvin_to_fahrenheit(kelvin) -> float:
            return round((kelvin - kelvin_to_celsius_constant) * 9 / 5 + 32)
        meters_to_miles_constant = 2.23694
        def meters_per_second_to_miles_per_hour(meters_per_second) -> float:
            # rounded to 2 decimals of precision
            return round(meters_per_second * meters_to_miles_constant, 2)
        
        # temperature
        self.temp = {
            'K°' : str(round(data['main']['temp'])), 
            'C°' : str(kelvin_to_celsius(data['main']['temp'])),
            'F°' : str(kelvin_to_fahrenheit(data['main']['temp']))
            }
        self.max_temp = {
            'K°' : str(round(data['main']['temp_max'])), 
            'C°' : str(kelvin_to_celsius(data['main']['temp_max'])),
            'F°' : str(kelvin_to_fahrenheit(data['main']['temp_max']))
        }
        self.min_temp = {
            'K°' : str(round(data['main']['temp_min'])), 
            'C°' : str(kelvin_to_celsius(data['main']['temp_min'])),
            'F°' : str(kelvin_to_fahrenheit(data['main']['temp_min']))
        }
        self.feels_temp = {
            'K°' : str(round(data['main']['feels_like'])), 
            'C°' : str(kelvin_to_celsius(data['main']['feels_like'])),
            'F°' : str(kelvin_to_fahrenheit(data['main']['feels_like']))
        }
        
        # location
        self.name = str(self.data['name'])
        # some places don't return a country
        try:
            self.country = str(self.data['sys']['country'])
        except:
            self.country = None

        # weather description
        self.description = str(self.data['weather'][0]['description'])

        # sunrise and sunset
        self.sunrise = unix_to_hour_minute(self.data['sys']['sunrise'], self.data['timezone'])
        self.sunset = unix_to_hour_minute(self.data['sys']['sunset'], self.data['timezone'])

        # day of the week and local hour and minute
        self.day_of_week = unix_to_day_of_week(self.data['dt'], self.data['timezone'])
        self.current_hour_minute = unix_to_hour_minute(self.data['dt'], self.data['timezone'])

        # misc weather
        self.wind_speed = {
            'm/s' : str(data['wind']['speed']),
            'mph' : str(meters_per_second_to_miles_per_hour(data['wind']['speed']))
        }
        self.humidity = str(self.data['main']['humidity'])
        self.cloudiness = str(self.data['clouds']['all'])

    # creates and initializes text components 
    def create_texts(self) -> None:
        self.texts = [
            # temperature toggle
            text((54, 125), self.tempature_unit, self.main_font, 30, self.font_color),
            text((13, 165), 'Click to Toggle', self.main_font, 16, self.font_color),
            # mileage toggle
            text((141, 125), self.speed_unit, self.main_font, 30, self.font_color),
            text((123, 165), 'Click to Toggle', self.main_font, 16, self.font_color),
            # time
            text((305, 260), 'Local Time is ' + self.day_of_week + ', ' + self.current_hour_minute, self.main_font, 25, self.font_color),
            # weather description
            text((342, 205), self.description, self.main_font, 30, self.font_color),
            # temperature data
            text((12, 192), self.temp[self.tempature_unit] + ' ' + self.tempature_unit, self.main_font, 50),
            text((12, 270), 'Max '+ self.max_temp[self.tempature_unit] + ' ' + self.tempature_unit + 
                        ' / Min ' + self.min_temp[self.tempature_unit] + ' ' + self.tempature_unit, self.main_font, 25),
            text((342, 232), 'Feels like ' + self.feels_temp[self.tempature_unit] + ' ' + self.tempature_unit, self.main_font, 30),
            # location | ternary operator to ease creation
            text((12, 235), self.name + ', ' + self.country if self.country != None else self.name, self.main_font, 35),
            # sunrise and sunset
            text((115, 550), 'Sunrise', self.main_font, 22),
            text((418, 550), 'Sunset', self.main_font, 22),
            text((97, 503), self.sunrise, self.main_font, 48),
            text((395, 503), self.sunset, self.main_font, 48),
            # wind
            text((72, 775), 'Wind', self.main_font, 35),
            text((47, 840), self.wind_speed[self.speed_unit] + ' ' + self.speed_unit, self.main_font, 35),
            # humidity
            text((235, 775), 'Humidity', self.main_font, 35),
            text((280, 840), self.humidity + '%', self.main_font, 35),
            # cloudiness
            text((437, 775), 'Cloudiness', self.main_font, 35),
            text((472, 840), self.cloudiness + '%', self.main_font, 35)
            ]

    # creates and initializes button components
    def create_buttons(self) -> None:
        # button colors
        button_light = (115,215,255)
        button_dark = (85,206,255)

        self.buttons = [ 
            # input
            button((10, 10), (580, 70), button_light, button_dark, 'Enter a City\'s Name', self.main_font, 25, self.font_color, (192, 23)),
            # temperature toggle
            button((10, 90), (100, 100), button_light, button_dark, 'Tempature', self.main_font, 16, self.font_color, (17, 7)),
            # speed toggle
            button((120, 90), (100, 100), button_light, button_dark, 'Speed', self.main_font, 16, self.font_color, (30, 7)),
            ]
        self.buttons[1].add_event(self.update_temperature)
        self.buttons[2].add_event(self.update_speed)

    # creates the images
    def create_images(self) -> None:
        self.images = [
            image((425, 35), (200, 200), get_weather_icon(self.data)),
            image((0, 308), (300, 300), pygame.image.load(SUNRISE_ICON_PATH).convert_alpha()),
            image((300, 320), (300, 300), pygame.image.load(SUNSET_ICON_PATH).convert_alpha()),
            image((25, 620), (170, 150), pygame.image.load(WIND_ICON_PATH).convert_alpha()),
            image((210, 580), (180, 180), pygame.image.load(HUMIDITY_ICON_PATH).convert_alpha()),
            image((410, 580), (180, 180), pygame.image.load(CLOUDS_ICON_PATH).convert_alpha())
            ]

    # sends the graphics components
    def get_graphic_components(self) -> tuple:
        return (self.buttons, self.texts, self.images)

    # updates the text that is dependent on the temperature unit 
    def update_temperature(self) -> None:
        # swaps between kelvin, celsius, and fahrenheit
        if(self.tempature_unit == 'K°'):
            self.tempature_unit = 'C°'
        elif(self.tempature_unit == 'C°'):
            self.tempature_unit = 'F°'
        elif(self.tempature_unit == 'F°'):
            self.tempature_unit = 'K°'

        # updates temperature related components
        self.texts[0].update_text(self.tempature_unit)
        self.texts[6].update_text(self.temp[self.tempature_unit] + ' ' + self.tempature_unit)
        self.texts[7].update_text('Max '+ self.max_temp[self.tempature_unit] + ' ' + self.tempature_unit + 
                              ' / Min ' + self.min_temp[self.tempature_unit] + ' ' + self.tempature_unit)
        self.texts[8].update_text('Feels like ' + self.feels_temp[self.tempature_unit] + ' ' + self.tempature_unit)

    # updates text that is dependent on the wind speed
    def update_speed(self) -> None:
        # swaps between m/s and mph
        if(self.speed_unit == 'm/s'):
            self.speed_unit = 'mph'
        else:
            self.speed_unit = 'm/s'

        # changes wind related components
        self.texts[2].update_text(self.speed_unit, self.main_font)
        self.texts[15].update_text(self.wind_speed[self.speed_unit] + ' ' + self.speed_unit)