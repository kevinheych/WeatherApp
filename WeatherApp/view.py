import tkinter as tk
 
from tkinter import ttk
from PIL import Image, ImageTk

class View:


    def __init__(self,parent):
        self.container = parent
        self.WIDTH = 700
        self.HEIGHT = 700
        self.PADDING = 3
        self.bg_color = 'white'
        return

    def setup(self):
        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):
        """Create various widgets in the tkinter main window"""
        #The tab bar
        self.notebook = ttk.Notebook(self.container, style='lefttab.TNotebook', width = self.WIDTH, height = self.HEIGHT)

        #Make Forecast Tab
        self.forecast_tab = tk.Frame(self.notebook, bg=self.bg_color)

        #sections
        self.overview_frame      = tk.Frame(self.forecast_tab, bg='white', width = 200, height = 200)
        self.location_lbl        = tk.Label(self.overview_frame, text = "Location", font=(None, 15))
        self.overview_middle     = tk.Frame(self.overview_frame)
        self.weather_icon_lbl    = tk.Canvas(self.overview_middle, width = 50, height = 50 )
        self.temp_lbl            = tk.Label(self.overview_middle, text = "11°", font=(None, 50))
        self.c_button            = tk.Button(self.overview_middle, text = "C",font=(None, 15) )
        self.weather_text_lbl    = tk.Label(self.overview_frame, text = "Clouds", font=(None, 15))
        self.overview_bottom     = tk.Frame(self.overview_frame)
        self.feels_like_lbl      = tk.Label(self.overview_bottom, text = "Feels like 7°")
        self.pressure_lbl        = tk.Label(self.overview_bottom, text = "Pressure 1021")
        self.humidity_lbl        = tk.Label(self.overview_bottom, text = "Humidity 68%")
        self.dew_lbl = tk.Label(self.overview_bottom, text = "Dew Point 13.2")
        self.wind_lbl = tk.Label(self.overview_bottom, text = "Wind: 7.7km/h ")
        self.visibility_lbl = tk.Label(self.overview_bottom, text = "Visibility 100%")
        self.last_updated_lbl = tk.Label(self.overview_frame, text = "Last updated: 10:10AM",font=(None, 8) )

        #daily section
        self.daily_frame = ttk.Labelframe(self.forecast_tab, text='Daily')

        #daily item 1
        self.daily_item = tk.Frame(self.daily_frame, bg='yellow')
        

        self.daily_date_lbl = tk.Label(self.daily_item, text= 'Wed 9th', font=30)
        self.daily_weather_icon = tk.Canvas(self.daily_item, width=35, height = 35 )
        self.daily_temp_fr = tk.Frame(self.daily_item)
        self.daily_temp_high = tk.Label(self.daily_temp_fr, text="14°", font=(None,25))
        self.daily_temp_low = tk.Label(self.daily_temp_fr, text="7°")
        self.daily_weather_text = tk.Label(self.daily_item, text = "Cloudy")

        #hourly section
        self.hourly_frame = ttk.Labelframe(self.forecast_tab, text='Hourly', height=150)


        
        #Make Map Tab
        self.map_tab = tk.Frame(self.notebook, bg='blue')





        self.notebook.add(self.forecast_tab, text='Forecast')
        self.notebook.add(self.map_tab, text='Map')

    def setup_layout(self):
        self.notebook.pack(fill = tk.BOTH, expand = True)

        self.overview_frame.pack(padx=self.PADDING, pady=self.PADDING)
        self.location_lbl.grid(row = 0, sticky="ew", padx=self.PADDING, pady=self.PADDING)

        self.overview_middle.grid(row = 1, padx=self.PADDING, pady=self.PADDING)
        self.overview_middle.grid_columnconfigure((0, 4), weight=1)

        self.weather_icon_lbl.grid(row = 0, column=1)
        self.temp_lbl.grid(row = 0, column=2)
        self.c_button.grid(row = 0, column = 3)
        self.weather_text_lbl.grid(row = 2, padx=self.PADDING, pady=self.PADDING)
        self.overview_bottom.grid(row=3, padx=self.PADDING, pady=self.PADDING)
        self.feels_like_lbl.grid(row =0, column = 0)
        self.pressure_lbl.grid(row =0, column = 1)
        self.humidity_lbl.grid(row =0, column = 2)
        self.dew_lbl.grid(row =1, column = 0)
        self.wind_lbl.grid(row =1, column = 1)
        self.visibility_lbl.grid(row =1, column = 2)
        self.last_updated_lbl.grid(row=4, padx=self.PADDING, pady=self.PADDING)
        self.daily_frame.pack(fill= tk.BOTH, padx=self.PADDING, pady=self.PADDING)
        self.daily_item.pack(side = tk.LEFT, padx=self.PADDING, pady=self.PADDING)
        self.daily_date_lbl.pack(anchor = "w")
        self.daily_weather_icon.pack(anchor = "w")
        self.daily_temp_fr.pack(anchor = "w")
        self.daily_temp_high.pack(side= tk.LEFT, anchor = "sw")
        self.daily_temp_low.pack(side= tk.LEFT, anchor = "se", padx=self.PADDING, pady=self.PADDING)
        self.daily_weather_text.pack(side = tk.TOP,anchor = "w")
        self.hourly_frame.pack(fill= tk.X,padx=self.PADDING, pady=self.PADDING)
        self.hourly_frame.pack_propagate(False) 



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Weather Analysis App")
    style = ttk.Style(root)
    style.configure('lefttab.TNotebook', tabposition='wn')

    view = View(root)
    view.setup()

    root.mainloop()
 