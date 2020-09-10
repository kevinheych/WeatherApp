import tkinter as tk
import requests
import json

from tkinter import ttk
from PIL import Image, ImageTk

WIDTH = 700
HEIGHT = 700
PADDING = 3
bg_color = 'white'

# https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={YOUR API KEY}



def open_image(icon):
     
    img_large = ImageTk.PhotoImage(Image.open('./img/'+icon+'.png').resize((50, 50)))
    weather_icon_lbl.delete("all")
    weather_icon_lbl.create_image(0,0, anchor='nw', image=img_large)
    weather_icon_lbl.image = img_large

    img_small = ImageTk.PhotoImage(Image.open('./img/'+icon+'.png').resize((35, 35)))
    daily_weather_icon.delete("all")
    daily_weather_icon.create_image(0,0, anchor='nw', image=img_small)
    daily_weather_icon.image = img_small




root = tk.Tk()
root.title("Weather Analysis App")
style = ttk.Style(root)
style.configure('lefttab.TNotebook', tabposition='wn')



#The tab bar
notebook = ttk.Notebook(root, style='lefttab.TNotebook', width = WIDTH, height = HEIGHT)
notebook.pack(fill = tk.BOTH, expand = True)



#Make Forecast Tab
forecast_tab = tk.Frame(notebook, bg=bg_color)

#sections
overview_frame = tk.Frame(forecast_tab, bg='white', width = 200, height = 200)
overview_frame.pack(padx=PADDING, pady=PADDING)



location_lbl = tk.Label(overview_frame, text = "Location", font=(None, 15))
location_lbl.grid(row = 0, sticky="ew", padx=PADDING, pady=PADDING)

overview_middle = tk.Frame(overview_frame)
overview_middle.grid(row = 1, padx=PADDING, pady=PADDING)
overview_middle.grid_columnconfigure((0, 4), weight=1)


weather_icon_lbl    = tk.Canvas(overview_middle, width = 50, height = 50 )
temp_lbl            = tk.Label(overview_middle, text = "11°", font=(None, 50))
c_button            = tk.Button(overview_middle, text = "C",font=(None, 15) )

weather_icon_lbl.grid(row = 0, column=1)
temp_lbl.grid(row = 0, column=2)
c_button.grid(row = 0, column = 3)


weather_text_lbl = tk.Label(overview_frame, text = "Clouds", font=(None, 15))
weather_text_lbl.grid(row = 2, padx=PADDING, pady=PADDING)

overview_bottom = tk.Frame(overview_frame)
overview_bottom.grid(row=3, padx=PADDING, pady=PADDING)

feels_like_lbl = tk.Label(overview_bottom, text = "Feels like 7°")
pressure_lbl = tk.Label(overview_bottom, text = "Pressure 1021")
humidity_lbl = tk.Label(overview_bottom, text = "Humidity 68%")
dew_lbl = tk.Label(overview_bottom, text = "Dew Point 13.2")
wind_lbl = tk.Label(overview_bottom, text = "Wind: 7.7km/h ")
visibility_lbl = tk.Label(overview_bottom, text = "Visibility 100%")

feels_like_lbl.grid(row =0, column = 0)
pressure_lbl.grid(row =0, column = 1)
humidity_lbl.grid(row =0, column = 2)
dew_lbl.grid(row =1, column = 0)
wind_lbl.grid(row =1, column = 1)
visibility_lbl.grid(row =1, column = 2)

last_updated_lbl = tk.Label(overview_frame, text = "Last updated: 10:10AM",font=(None, 8) )
last_updated_lbl.grid(row=4, padx=PADDING, pady=PADDING)




 

#daily section
daily_frame = ttk.Labelframe(forecast_tab, text='Daily')
daily_frame.pack(fill= tk.BOTH, padx=PADDING, pady=PADDING)


#daily item 1
daily_item = tk.Frame(daily_frame, bg='yellow')
daily_item.pack(side = tk.LEFT, padx=PADDING, pady=PADDING)

daily_date_lbl = tk.Label(daily_item, text= 'Wed 9th', font=30)
daily_weather_icon = tk.Canvas(daily_item, width=35, height = 35 )
daily_temp_fr = tk.Frame(daily_item)
daily_temp_high = tk.Label(daily_temp_fr, text="14°", font=(None,25))
daily_temp_low = tk.Label(daily_temp_fr, text="7°")
daily_weather_text = tk.Label(daily_item, text = "Cloudy")


daily_date_lbl.pack(anchor = "w")
daily_weather_icon.pack(anchor = "w")
daily_temp_fr.pack(anchor = "w")
daily_temp_high.pack(side= tk.LEFT, anchor = "sw")
daily_temp_low.pack(side= tk.LEFT, anchor = "se", padx=PADDING, pady=PADDING)
daily_weather_text.pack(side = tk.TOP,anchor = "w")

#hourly section

hourly_frame = ttk.Labelframe(forecast_tab, text='Hourly', height=150)
hourly_frame.pack(fill= tk.X,padx=PADDING, pady=PADDING)
hourly_frame.pack_propagate(False) 

 
#Make Map Tab
map_tab = tk.Frame(notebook, bg='blue')





notebook.add(forecast_tab, text='Forecast')
notebook.add(map_tab, text='Map')

open_image('04d')
root.mainloop()