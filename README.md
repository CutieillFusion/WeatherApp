# WeatherApp
 KATA problem for DirectSupply

# Required Libraries

    Pygame
    Requests
    PIL
    

# Documentation
main.py:

    This code is the main entry point for a weather application. It initializes a graphics object with a specified screen resolution and application name. Then, it enters an infinite loop where it continuously runs the run method of the graphics object, allowing the application to render and respond to events until it is closed by the user.

graphics.py:

    This code defines the class graphics responsible for managing the rendering, user input, and graphical components in a Pygame-based application. Here's a breakdown of its functionality:

    Initialization (__init__ method):
        Initializes Pygame and sets up the window with the specified resolution and name.
        Sets the window icon.
        Initializes variables for background colors, typing text, and typing flag.
        Retrieves weather data using coordinates and initializes a weather_management object to manage the weather data.
    Set Weather Data (set_weather_data method):
        Retrieves the graphical components (buttons, texts, images) from the weather_management object and stores them for rendering.
    Start Typing (start_typing method):
        Sets the typing flag to True and clears the typing text if it's empty.
    Get Background Color (get_background_color method):
        Calculates and returns the background color by interpolating between predefined background colors based on time.
    Find City (find_city method):
        Calls the weather API with a city name.
        If the city is found, reinitializes the weather_management object with the new data.
        If the city is not found, updates the keyboard text to notify the user.
    Game Loop (run method):
        Manages user input events, including quitting the application, keyboard typing, and mouse clicks.
        Renders the background color, buttons, images, and texts on the screen.
        Updates the display by flipping the display buffer.

graphic_components.py:

    This code defines three classes (Button, Image, and Text) for creating graphical user interface (GUI) components using the Pygame library. Here's a breakdown of each class:

    button Class:
        Represents an interactive button with optional text.
        The button has properties such as position, size, colors for normal and hover states, and an optional text label.
        You can associate a function with the button to be executed when the button is clicked.
        The render method draws the button on a Pygame surface, taking into account the current mouse position to change the button's appearance when hovered.
        The colliding method checks if the mouse cursor is over the button.
        The clicked method executes the associated function if there is one.
    image Class:
        Represents an image that can be displayed on the screen.
        The image has properties such as position, size, and the Pygame surface containing the image.
        If the size provided during initialization doesn't match the surface size, the surface is scaled accordingly.
        The render method blits the image onto a Pygame surface.
    text Class:
        Represents text that can be displayed on the screen.
        The text has properties such as position, font information, and color.
        The update_text method allows for the modification of the text, font, and color.
        The render method blits the text onto a Pygame surface, considering the text offset.
        Note: The code assumes the existence of a settings module with the DEFAULT_FONT and DEFAULT_FONT_COLOR constants, which are used as default values for font-related properties.

weather_management.py:

    This defines the weather_management class which manages the interaction between weather data and graphical components, converting data into variables and initializing various text, button, and image components for display.

    Initialization:
        Upon initialization, it takes weather data as input and parses it to extract relevant information.
        It initializes variables for font, font color, and units for temperature and speed.
    Data Parsing:
        It converts temperature from Kelvin to Celsius and Fahrenheit.
        It extracts location, weather description, sunrise, sunset, day of the week, current hour, wind speed,  humidity, and cloudiness from the data.
    Component Initialization:
        It initializes text components for displaying various weather-related information.
        It initializes button components, including buttons for toggling between temperature units and speed units.
        It initializes image components, including weather icons and other visual elements.
    Update Methods:
        update_temperature(): 
            Toggles between Kelvin, Celsius, and Fahrenheit for temperature units and updates relevant text components accordingly.
        update_speed(): 
            Toggles between meters per second and miles per hour for speed units and updates relevant text components accordingly.
    Utility Methods:
        get_graphic_components(): 
            Returns the initialized graphical components (buttons, texts, images) as a tuple.

util.py:

    This code is a collection of functions related to fetching weather data from the OpenWeatherMap API, handling image downloads, and converting timestamps.

    request_current_weather_from_name_redundant(city_name:str) -> dict:
        Sends a request to the OpenWeatherMap API to get current weather data based on the provided city name.
        Returns the weather data in a JSON-style dictionary.
    find_city_id_from_name(name:str) -> int:
        Finds the city ID corresponding to the given city name by searching through a JSON file containing city data.
        Returns the city ID.
    request_current_weather_from_name(name:str) -> dict:
        Requests current weather data from the OpenWeatherMap API using either the city name or city ID.
        Returns the weather data in a JSON-style dictionary.
    get_current_weather_from_coords(position:tuple=DEFAULT_COORDS) -> dict:
        Requests weather data based on latitude and longitude coordinates.
        Returns the weather data in a JSON-style dictionary.
    download_image(url:str) -> Image:
        Downloads an image from the provided URL.
        Returns a Pillow image object.
    convert_pillow_to_pygame_surface(pillow_image:Image) -> pygame.image:
        Converts a Pillow image to a Pygame surface.
        Returns the Pygame surface.
    get_weather_icon(data:dict) -> pygame.image:
        Retrieves the weather icon corresponding to the current weather conditions from OpenWeatherMap.
        Returns the weather icon as a Pygame image.
    unix_to_utc(unix_timestamp:int, local_time:int=0) -> datetime.datetime:
        Converts a Unix timestamp to a UTC datetime object.
        Returns the UTC datetime object.
    unix_to_hour_minute(unix_timestamp:int, local_time:int=0) -> str:
        Converts a Unix timestamp to local time and returns the hour and minute portion as a string.
    unix_to_day_of_week(unix_timestamp:int, local_time:int=0) -> str:
        Converts a Unix timestamp to local time and returns the day of the week as a string.

settings.py:

    This code defines several constants and paths used in a weather application.

    OPEN_WEATHER_API_KEY: 
        Private key for accessing the OpenWeather API. It is used to authenticate API requests.
    DEFAULT_COORDS: 
        Default coordinates representing a location (Zocca, Italy) used when retrieving weather data if no specific coordinates are provided.
    DEFAULT_FONT: 
        Default font used for rendering text in the application.
    DEFAULT_FONT_COLOR: 
        Default font color (white) used for rendering text.
    BACKGROUND_COLORS: 
        List of background colors used in the application. These colors are used to create a dynamic background that changes over time.
    Paths to icon images used in the application:
        SUNRISE_ICON_PATH: Path to the image representing a sunrise icon.
        SUNSET_ICON_PATH: Path to the image representing a sunset icon.
        WIND_ICON_PATH: Path to the image representing a wind icon.
        HUMIDITY_ICON_PATH: Path to the image representing a humidity icon.
        CLOUDS_ICON_PATH: Path to the image representing a clouds icon.
        APP_ICON_PATH: Path to the application icon.
        PARSED_CITIES_PATH: Path to a JSON file containing parsed city data. This file likely includes information such as city names and their corresponding IDs.

parse_cities.py:

    This code reads city data from one JSON file, extracts relevant information (city name converted to lowercase and ID), sorts it based on city IDs, and then writes the processed data to another JSON file.