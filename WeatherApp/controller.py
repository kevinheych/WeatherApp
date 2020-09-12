from view import View
from model import Model

import tkinter as tk
 
from tkinter import ttk
from PIL import Image, ImageTk
import datetime
class Controller:

    location = 0

    def __init__(self, parent):
        
        self.parent = parent
        self.model = Model()
        self.view = View(parent)
        self.view.setup()

    def set_location(self, location):
        self.location = self.model.get_location(location)

    def update_weather(self, location):
        #shorten address
        address = location.address
        split = address.split(",")
        print(split[0], split[2]) 

        #request data 
        weather_json = self.model.get_weather(location)

        #json 
        current = weather_json['current']
        
        #time convert Unix, UTC 
        dt = current['dt']
        current_time = datetime.datetime.fromtimestamp(dt)

        icon_name = current["weather"][0]['icon']
        weather_text = current["weather"][0]['main']
        temp = current['temp']
        feels_like = current['feels_like']
        pressure = current['pressure']
        humidity = current['humidity']
        dew_point = current['dew_point']
        wind_speed = current['wind_speed']
        visibility = current['visibility']

        self.view.open_image(icon_name)

        self.view.location_lbl.configure(text=split[0]+","+split[3])
        self.view.temp_lbl.configure(text=temp)
        self.view.weather_text_lbl.configure(text=weather_text)
        self.view.feels_like_lbl.configure(text="Feels like "+str(feels_like))
        self.view.pressure_lbl.configure(text="Pressure "+str(pressure))
        self.view.humidity_lbl.configure(text="Humidity "+str(humidity))
        self.view.dew_lbl.configure(text="Dew Point "+str(dew_point))
        self.view.wind_lbl.configure(text="Wind speed "+str(wind_speed))
        self.view.visibility_lbl.configure(text="Visibility "+str(visibility))
        self.view.last_updated_lbl.configure(text="Last updated "+ str(current_time))
   




if __name__ == "__main__":
    # Create an instance of Tk. This is popularly called 'root' But let's
    # call it mainwin (the 'main window' of the application. )
    mainwin = tk.Tk()
    WIDTH = 700
    HEIGHT = 700
    mainwin.geometry("%sx%s" % (WIDTH, HEIGHT))
    #mainwin.resizable(0, 0)
    background_label = tk.Label(mainwin)
    mainwin.title("Weather Analysis App")
    
     
    app = Controller(mainwin)
    app.set_location("Preston 3072")
    app.update_weather(app.location)

    # Theme for the respective time the application is used 
 
    mainwin.mainloop()        