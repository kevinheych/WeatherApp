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
        
        self.set_location("Preston 3072")
        self.update_weather_c(self.location)
        
        self.view.setup()
        self.update_views(self.current)

        self.view.search_btn.config(command = self.get_location)
        self.view.c_button.config(command = self.change_metric)

  
    def get_location(self):
        location = self.view.search_box.get()
        self.set_location(location)
        self.update_weather_c(self.location)
        self.update_views(self.current)

    def change_metric(self):
        
        btn_text = self.view.c_button['text']
        if btn_text == 'C':
            self.update_weather_f(self.location)
            self.view.setup()
            self.update_views(self.current)
            self.view.c_button.config(text = "F")
        elif btn_text == 'F':
            self.update_weather_c(self.location)
            self.view.setup()
            self.update_views(self.current)
            self.view.c_button.config(text = "C")
        
        

    def set_location(self, location):
        self.location = self.model.get_location(location)

    def update_weather_c(self, location):
        #request data 
        weather_json = self.model.get_weather_c(self.location)
        self.view.weather_json = weather_json
        #json 
        self.current = weather_json['current']

    def update_weather_f(self, location):
        #request data 
        weather_json = self.model.get_weather_f(self.location)
        self.view.weather_json = weather_json
        #json 
        self.current = weather_json['current']

        

    def update_views(self, current):
        #shorten address to Suburb, Postcode
        address = self.location.address
        split = address.split(",")
        print(split) 
        #time convert Unix, UTC 
        dt = current['dt']
        current_time = datetime.datetime.fromtimestamp(dt)
        icon_name = current["weather"][0]['icon']
        weather_text = current["weather"][0]['main']
        temp = round(current['temp'],1)
        feels_like = current['feels_like']
        pressure = current['pressure']
        humidity = current['humidity']
        dew_point = current['dew_point']
        wind_speed = current['wind_speed']
        visibility = current['visibility']

        overview_text = "Feels like "+ str(feels_like) + "    Pressure "+str(pressure) + "    Humidity "+str(humidity) + "\nDew Point "+ str(dew_point) + "    Wind speed "+str(wind_speed) + "    Visibility "+str(visibility)
       
         
        self.view.c_button.config(command = self.change_metric)
        self.view.search_btn.config(command = self.get_location)
        #update overview 
        self.view.open_image(icon_name)
        self.view.overview_canvas.itemconfig(self.view.location_text, text=split[0]+","+split[1])
        self.view.overview_canvas.itemconfig(self.view.temp_lbl, text= str(temp)+"°")
        self.view.overview_canvas.itemconfig(self.view.weather_text_lbl, text= weather_text)
        self.view.overview_canvas.itemconfig(self.view.overview_info_text, text= overview_text)
        self.view.overview_canvas.itemconfig(self.view.last_updated_lbl, text= "Last updated "+ str(current_time.strftime("%I:%M %p, %a %d ")))



         
        
  
 


if __name__ == "__main__":
    # Create an instance of Tk. This is popularly called 'root' But let's
    # call it mainwin (the 'main window' of the application. )
    mainwin = tk.Tk()
    WIDTH = 700
    HEIGHT = 1000
    mainwin.geometry("%sx%s" % (WIDTH, HEIGHT))
    #mainwin.resizable(0, 0)
    background_label = tk.Label(mainwin)
    mainwin.title("Weather Analysis App")
    
     
    app = Controller(mainwin)
    
 
    mainwin.mainloop()        