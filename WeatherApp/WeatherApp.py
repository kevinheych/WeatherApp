import tkinter as tk
from tkinter import ttk

WIDTH = 700
HEIGHT = 700
PADDING = 3
bg_color = 'white'

root = tk.Tk()
root.title("Weather Analysis App")
style = ttk.Style(root)
style.configure('lefttab.TNotebook', tabposition='wn')

#The tab bar
notebook = ttk.Notebook(root, style='lefttab.TNotebook', width = WIDTH, height = HEIGHT)
notebook.pack(fill = tk.BOTH, expand = True)



#Make Forecast Tab
forecast_tab = tk.Frame(notebook, bg='red')

#sections
overview_frame = tk.Frame(forecast_tab, bg='white', width = 200, height = 200)
overview_frame.pack(padx=PADDING, pady=PADDING)



location_lbl = tk.Label(overview_frame, text = "Location", font=(None, 15))
location_lbl.grid(row = 0, sticky="ew", padx=PADDING, pady=PADDING)

overview_middle = tk.Frame(overview_frame)
overview_middle.grid(row = 1, padx=PADDING, pady=PADDING)
overview_middle.grid_columnconfigure((0, 4), weight=1)


weather_icon_lbl    = tk.Label(overview_middle, bg='black', width = 5 )
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




 

 
daily_frame = ttk.Labelframe(forecast_tab, text='Daily',height=150)
daily_frame.pack(fill= tk.BOTH, padx=PADDING, pady=PADDING)
daily_frame.pack_propagate(False) 

#daily item 1
daily_item1 = tk.Frame(daily_frame, bg='yellow')
daily_item1.pack(side = tk.LEFT, padx=PADDING, pady=PADDING)

label_a = tk.Label(daily_item1, text= 'Item1')
label_a.pack()
label_b = tk.Label(daily_item1, text= 'Item2')
label_b.pack()

#daily item 1
daily_item2 = tk.Frame(daily_frame, bg='blue')
daily_item2.pack(side = tk.LEFT,fill= tk.Y, padx=PADDING, pady=PADDING)

label_a = tk.Label(daily_item2, text= 'Item1')
label_a.pack()
label_b = tk.Label(daily_item2, text= 'Item2')
label_b.pack()

hourly_frame = ttk.Labelframe(forecast_tab, text='Hourly', height=150)
hourly_frame.pack(fill= tk.X,padx=PADDING, pady=PADDING)
hourly_frame.pack_propagate(False) 

 
#Make Map Tab
map_tab = tk.Frame(notebook, bg='blue')





notebook.add(forecast_tab, text='Forecast')
notebook.add(map_tab, text='Map')


root.mainloop()