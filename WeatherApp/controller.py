from view import View
from model import Model

import tkinter as tk
 
from tkinter import ttk
from PIL import Image, ImageTk
import datetime

 
class Controller:

    location = 0

    def __init__(self, parent):
       
        self.model = Model()
        self.view = View(parent)
        
        self.location = self.model.get_currentLoc()
        self.update_weather_c(self.location)
        self.view.location = self.location
        
        self.view.setup()
        self.update_views(self.current)

        #attach button commands 
        self.view.search_btn.config(command = self.get_location)
        self.view.refresh_btn.config(command = self.refresh_ui)
        self.view.c_button.config(command = self.change_metric)

   

    def refresh_ui(self):
        self.update_weather_c(self.location)
        self.update_views(self.current)
  
    def get_location(self):
        location = self.view.search_box.get()
        self.view.search_box.delete(0, 'end')
        self.set_location(location)
        self.view.location = self.location
        self.view.map_RadioBtnSelected()
        self.update_weather_c(self.location)
        self.update_views(self.current)
   

    def change_metric(self):
        
        btn_text = self.view.c_button['text']
        if btn_text == 'C':
            self.update_weather_f(self.location)
            #
            self.update_views(self.current)
            self.view.c_button.config(text = "F")
        elif btn_text == 'F':
            self.update_weather_c(self.location)
         
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
       
        #reattach button commands 
        self.view.c_button.config(command = self.change_metric)
        self.view.refresh_btn.config(command = self.refresh_ui)
        self.view.search_btn.config(command = self.get_location)
        #update overview 
        self.view.open_image(icon_name)
        self.view.overview_canvas.itemconfig(self.view.location_text, text=split[0]+","+split[1])
        self.view.overview_canvas.itemconfig(self.view.temp_lbl, text= str(temp)+"°")
        self.view.overview_canvas.itemconfig(self.view.weather_text_lbl, text= weather_text)
        self.view.overview_canvas.itemconfig(self.view.overview_info_text, text= overview_text)
        self.view.overview_canvas.itemconfig(self.view.last_updated_lbl, text= "Last updated "+ str(current_time.strftime("%I:%M %p, %a %d ")))

        #remove and recreate 48hrs, daily, dailydetails
        self.view.hourly_frame.destroy()
        self.view.daily_scroll_frame.destroy()
        self.view.daily_detail_frame.destroy()

        self.view.next_48hrs()
        self.view.daily_section()
        self.view.load_daily_detail()




        #update map
        self.view.loc_label.config(text=split[0]+","+split[1])




         
        
  
 


if __name__ == "__main__":
 
    mainwin = tk.Tk()
    WIDTH = 1000
    HEIGHT = 700
    mainwin.geometry("%sx%s" % (WIDTH, HEIGHT))
  
    mainwin.title("Weather Analysis App")
    
    mainwin.attributes('-alpha', 0.0) 
    

   
    app = Controller(mainwin)
    mainwin.after(0, mainwin.attributes, "-alpha", 1.0)
  
    mainwin.mainloop()        