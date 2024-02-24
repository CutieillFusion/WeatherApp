from graphics import graphics

# main entry point
def main() -> None:
    # screen resolution
    res = (600,900) # just dont touch this variable please
    name = 'Weather App'

    # initializes graphics
    app = graphics(res, name)

    # infinity loop till forced close
    while True:
        app.run()

# python safety net
if __name__ == "__main__":
    main()

# For anyone reading this code
# - the resolution is FIXED, DONT TOUCH, nothing breaks but visually it stops working correctly
# - buttons could be swapped to work with images but wasn't needed
# - please don't fall into the trap abstracting graphic_component logic. Keep it seperate for sake of quick customization
# - I have my a private key in here so don't upload to github with it
# - the UI could look better but its the best programmer art I could obtain
# - graphical components are stored in arrays. they are being modified based on index in update_temperature(), update_speed(), and set_weather_data()
# - API calls tend to freeze the app for a second. I don't think adding multithreading is worth but its possible
# - if the times are off by a couple of minutes its because of the API, if its more than that its because of me
# - if the color changing background is annoying, set color_size to 1 inside graphics.get_background_color()
# - settings.py contains 90% of magic numbers and paths, modify anything easily from that file
# - parsed_cities.json is required for this function correctly. if lost download current.city.list.json from OpenWeatherAPI and run parse_cities
# - changing font ruins everything. fixing this issue seems very impossible
# - all components are hardcoded in weather_management. Could be stored in a json file but that tends to make modifiying more frustrating from my experience
    
# pip install
# - requests
# - pygame
# - pil