import tkinter as tk
from model import Model
from map import Map
 
import json
from tkinter import ttk
from PIL import Image, ImageTk
import datetime
import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 

from scipy import interpolate
class ScrollableFrame(tk.Frame):
    def __init__(self, parent):

        self.parent = parent
        

        tk.Frame.__init__(self, self.parent)
         

        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        #self.scrollbar.pack( side = tk.RIGHT, fill = tk.Y)
        #self.canvas.pack(  fill = tk.BOTH, expand=True)

        self.canvas.grid(row=0, column=0, sticky="ns")
        self.scrollbar.grid(row=0, column=1, sticky = "ns")
        
        

        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw",
                                                                tags="scroll_fr")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

         
        self.scrollable_frame.bind(
            "<Configure>",
            self.handle_canvas_resize
        )
         

    def handle_canvas_resize(self,event):
     
        width = event.width
        self.canvas.config( width=width)
        
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
         

     
class View:
    background_image = 0

    def __init__(self,parent):
      
 
        self.i = tk.IntVar()
        self.i.set(0)
        self.layer_i = tk.StringVar()
        self.layer_i.set("temp_new")
        

        self.container = parent

        #class variables
        self.WIDTH = parent.winfo_width()
        self.HEIGHT = parent.winfo_height()
        self.PADDING = 3
        self.bg_color = 'white'

        self.map = Map()
        
        
         
        

    def setup(self):
        

        #gui navigation
        self.header_bar()
        self.tab_bar()

        #Forecast sections
        self.overview_section()
        self.next_48hrs()
        self.daily_section()
        self.load_daily_detail()

        #Map section
        self.load_map_section()


 
## GUI 


    def tab_bar(self):  

        #The tab bar
        noteStyler = ttk.Style( )
        noteStyler.theme_use('winnative')
        noteStyler.configure('lefttab.TNotebook', tabposition='wn' , tabmargins=[2, 5, 2, 0],background='navajo white')
        noteStyler.map('lefttab.TNotebook.Tab',background=[('selected', 'goldenrod'), ('active', 'goldenrod')])
        noteStyler.configure('lefttab.TNotebook.Tab', padding=[12, 12], font =(None, 12))

        self.notebook = ttk.Notebook(self.container, style='lefttab.TNotebook')
        self.notebook.pack(side = tk.BOTTOM,fill=tk.BOTH, expand = True)
         
        #Make Tabs
        self.forecast_frame = tk.Frame(self.notebook)
        self.testScroll = ScrollableFrame(self.forecast_frame)
        self.testScroll.pack(side=tk.BOTTOM,fill=tk.BOTH, expand=True)
        self.forecast_tab = tk.Frame(self.testScroll.scrollable_frame, bg='white')
        self.forecast_tab.pack( fill=tk.BOTH, expand=True)
        
        self.map_tab = tk.Frame(self.notebook, bg= 'white')


        self.notebook.add(self.forecast_frame, text="Forecast".ljust(8)[:8])
        self.notebook.add(self.map_tab,  text="     Map   ".ljust(8))


    def load_map_section(self):
        

        #change layers
        #add radiobutton
        LAYERS = [
            ("Temperature","temp_new"),
            ("Clouds","clouds_new"),
            ("Precipitation","precipitation_new"),
            ("Sea level pressure","pressure_new"),
            ("Wind speed","wind_new"),
            
        ]

        self.layer_btn_frame = tk.Frame(self.map_tab, bg= 'white')

        self.layer_btn_frame.pack(side=tk.BOTTOM, padx = 20, pady = 10)
        for text, layer in LAYERS:
            self.btn = tk.Radiobutton(self.layer_btn_frame, text= text, variable=self.layer_i,value=layer, command = self.map_RadioBtnSelected, bg= 'white') 
            self.btn.pack(side=tk.LEFT)
     
        #map fig
        self.load_mapfig(self.location)
        self.loc_label = tk.Label(self.map_tab, text = self.location.address,bg= 'white',
                                font=(None, 15), 
                                anchor=tk.CENTER, padx = 10,pady=10)
        self.loc_label.pack()


    def load_mapfig(self,location):
        #map container
        self.map_canvas = tk.Canvas(self.map_tab, bg= 'white')
        self.map_canvas.pack( expand = True)

        #matlab figure
        self.map_fig = plt.Figure()

        latitude = self.location.latitude 
        longitude = self.location.longitude
        print("lat",latitude)
        print("lon",longitude)
        self.map_ax = self.map.map(self.map_fig, self.layer_i.get(),longitude,latitude )
        self.map_ax.set_title("Radar")
        self.map_widget  = FigureCanvasTkAgg(self.map_fig, self.map_canvas)
        self.map_widget.get_tk_widget().pack(fill = tk.X)
        self.map_widget.draw()
        
    def header_bar(self):
        # button picture icons
        img_search = Image.open("./img/search_icon.png")
        img_search = img_search.resize((25,25), Image.ANTIALIAS)

        img_refresh = Image.open("./img/refresh_icon.png")
        img_refresh = img_refresh.resize((25,25), Image.ANTIALIAS)

        self.search_icon = ImageTk.PhotoImage(img_search)
        self.btn_refresh_icon = ImageTk.PhotoImage(img_refresh)

        #frame container
        self.header_frame = tk.Frame(self.container, bg= 'white')

        self.refresh_btn = tk.Button(self.header_frame, image = self.btn_refresh_icon)
        self.search_box = tk.Entry(self.header_frame, font=(None, 15))
        self.search_btn = tk.Button(self.header_frame, image = self.search_icon, bg= 'white',command=self.clear_text)

        
        self.header_frame.pack(side=tk.TOP,fill = tk.X)
        self.search_btn.pack(side = tk.RIGHT)
        self.search_box.pack(side = tk.RIGHT)
        self.refresh_btn.pack(side = tk.RIGHT, padx=20)
        
    def overview_section(self):
        #overview section
        canvas_height = 250
        canvas_width = self.WIDTH
        current = self.weather_json['current'] 
        self.overview_canvas = tk.Canvas(self.forecast_tab,  height = canvas_height, bg = 'white',highlightthickness=0)
        self.overview_canvas.pack(fill = tk.X)
        self.notebook.update() 

        self.overview_bg = self.overview_canvas.create_image(canvas_width/2,canvas_height/2, image = self.load_bg())

        self.location_text = self.overview_canvas.create_text(
                                canvas_width//2, canvas_height*0.12, 
                                text='', 
                                fill = 'white', 
                                font=(None, 15), 
                                anchor=tk.CENTER)

        self.weather_icon_pic =  self.overview_canvas.create_image(canvas_width//2-150, canvas_height*0.25, anchor='nw')
        self.temp_lbl =  self.overview_canvas.create_text(
                            canvas_width//2, canvas_height*0.35, 
                            text='', fill = 'white', 
                            font=(None, 55), 
                            anchor=tk.CENTER)
                            
        self.c_button  = tk.Button(self.overview_canvas, text = "C",font=(None, 15) )
        self.c_button_window = self.overview_canvas.create_window(
                            canvas_width//2+100, canvas_height*0.25, 
                            anchor='nw', 
                            window= self.c_button)
        
        self.weather_text_lbl = self.overview_canvas.create_text(
                            canvas_width//2, canvas_height*0.6, 
                            text='', 
                            fill= 'white', font=(None, 15), 
                            anchor=tk.CENTER)

        overview_text = "Feels like 7°  Pressure 1021   Humidity 68% \nDew Point 13.2   Wind: 7.8km/h   Visibility 100%"
        self.overview_info_text = self.overview_canvas.create_text(
                            canvas_width//2, canvas_height*0.75, 
                            text=overview_text, 
                            fill = 'white', 
                            anchor=tk.CENTER)

        self.last_updated_lbl = self.overview_canvas.create_text(
                            canvas_width//2, canvas_height*0.9, 
                            text='Last updated: 10:10AM', 
                            fill = 'green', font=(None, 8), 
                            anchor=tk.CENTER)

        self.overview_canvas.bind("<Configure>", self.resize_window)
        self.overview_canvas.addtag_all("all")


    def next_48hrs(self):
        
        self.hourly_frame = tk.Frame(self.forecast_tab, bg = 'white')
        self.hourly_frame.pack()

        #gather data
        graphData = self.weather_json['hourly']
        hours = [i['dt'] for i in graphData]
        x_hours = pd.to_datetime(hours, unit = 's').strftime("%I%p %a")
       
        x_incre = list(range(0, 48))

        y_temp = [i['temp'] for i in graphData]
        y_precipitation = [i['pop']*100 for i in graphData]
        y_windspeed = [i['wind_speed'] for i in graphData]
    

        

        #create figure area
        self.f = plt.Figure( figsize=(10,3), tight_layout=True)
        self.ax = self.f.add_subplot(111)
        # draw subplot
        self.line_fig  = FigureCanvasTkAgg(self.f, self.hourly_frame)
        self.line_fig.draw()  
        self.line_fig.get_tk_widget().pack()
        self.line_fig.mpl_connect('pick_event', self.legend_pick)
        
        #add subplot
        
        self.ax.set_facecolor('skyblue')
        self.ax.set_xlabel('Time (hr)')
        self.ax.set_ylabel('Temp', color='darkorange')
        self.ax.set_title('Next 48 hours')

        self.ax.tick_params(  labelsize=7, color='moccasin')

        #add data to plot
        self.line1, = self.ax.plot(x_hours,y_temp,color='moccasin', zorder = 3, label="Temp")
        
        
        self.ax2 = self.ax.twinx()
        self.ax3 = self.ax.twinx()
        self.ax3.spines["right"].set_position(("axes", 1.15))
       
        self.ax3.spines["right"].set_visible(True)

        self.ax2.set_ylabel('Rain Chance (%)', color='royalblue')
        self.line2, = self.ax2.plot(x_hours, y_precipitation, color='royalblue', zorder=1, label="Rain")
        self.ax2.tick_params(  labelsize=7, color='royalblue')
        self.ax2.fill_between(x_hours,y_precipitation, color='cornflowerblue')
        self.ax2.set_ylim( 0,100)

        self.ax3.set_ylabel('Wind speed (m/s)', color='lightslategrey')
        self.line3, = self.ax3.plot(x_hours, y_windspeed, color='lightslategrey', zorder=2, label="Wind")
        self.ax3.tick_params(  labelsize=7, color='lightslategrey')
        self.ax3.set_ylim( 0,30)

        self.ax.set_xticklabels(x_hours)
        self.ax.set_ylim( 0,max(y_temp)+3)
        self.ax.set_xlim(0,48)
        self.ax.grid(True)

        #legend
        leg = self.f.legend(loc='upper center', bbox_to_anchor=(0.45, 0.9),
          ncol=3, fancybox=True, shadow=True, fontsize=10)
        leg.get_frame().set_alpha(0.4)
         
        for label in self.ax.get_xticklabels()[::2]:
            label.set_visible(False)
        
        plt.setp(self.ax.get_xticklabels(), rotation=-50, horizontalalignment='left',rotation_mode="anchor")
        self.f.subplots_adjust(bottom=0.2)
        

        
        # we will set up a dict mapping legend line to orig line, and enable
        # picking on the legend line
        self.lined = dict()
        axes = [ self.line1, self.ax2, self.ax3]
        
        for legline, origline in zip(leg.get_lines(), axes):
            legline.set_picker(10)  # 10 pts tolerance
           
            self.lined[legline] = origline
    
    def legend_pick(self, event):
        # on the pick event, find the orig line corresponding to the
        # legend proxy line, and toggle the visibility
        
        legline = event.artist
        origline = self.lined[legline]
        vis = not origline.get_visible()
        origline.set_visible(vis)
        
        # Change the alpha on the line in the legend so we can see what lines
        # have been toggled
        if vis:
            legline.set_alpha(1.0)
        else:
            legline.set_alpha(0.2)

        self.f.canvas.draw()
        self.f.canvas.flush_events()
      
    def daily_section(self):
        
        #daily item header for 8 day forecast. Implement horizontal scroll for overflow 

        #parent container for scroll view inside the tab
        self.daily_scroll_frame = tk.Frame(self.forecast_tab,bg='white')
        self.daily_scroll_frame.pack()

        #only canvas are scrollable
        self.scroll_canvas = tk.Canvas(self.daily_scroll_frame, height= 135, width = 900, bg= 'white')
        self.scrollbar_daily = tk.Scrollbar(self.daily_scroll_frame, orient = 'horizontal', command=self.scroll_canvas.xview, bg= 'white')
        self.scrollbar_daily.pack(fill=tk.X, side=tk.BOTTOM)

        #create the frame that will be put inside the canavs
        self.daily_frame = tk.Frame(self.scroll_canvas, bg= 'white')
        self.load_daily_items()

        self.scroll_canvas.create_window(0, 0, anchor='nw', window=self.daily_frame)
        self.scroll_canvas.update_idletasks()
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox('all'), xscrollcommand=self.scrollbar_daily.set)
        self.scroll_canvas.pack( padx=self.PADDING, pady=self.PADDING)

        #daily detail 
              
  
    def load_daily_items(self):
         #daily item 
        daily=  self.weather_json['daily']
        for index, day in enumerate(daily):
            
            date = datetime.datetime.fromtimestamp(day['dt'])
            temp = day['temp']
            #create daily item
            self.daily_item = tk.Frame(self.daily_frame, bg = 'white')
 
            self.daily_date_lbl = tk.Label(self.daily_item, 
                                text= date.strftime("%a %d"), 
                                font=30, width = 10, bg= 'white')
            self.daily_weather_icon = tk.Canvas(self.daily_item, width=35, height = 40 , bg= 'white')
            self.daily_temp_fr = tk.Frame(self.daily_item,bg= 'white')
            self.daily_temp_high = tk.Label(self.daily_temp_fr, text=str(round(temp['max']))+"°", font=(None,20), bg= 'white')
            self.daily_temp_low = tk.Label(self.daily_temp_fr, text=str(round(temp['min']))+"°",font=(None,16), foreground ='grey', bg= 'white')
            self.daily_weather_text = tk.Label(self.daily_item, text = day['weather'][0]['main'] , bg= 'white')
            
            #load daily item widgets
            self.daily_item.pack(side = tk.LEFT)
            self.daily_date_lbl.pack(anchor = "w")
            self.daily_weather_icon.pack(fill = tk.BOTH)
            self.daily_temp_fr.pack(anchor = "w")
            self.daily_temp_high.pack(side= tk.LEFT, anchor = "s", padx=self.PADDING+4)
            self.daily_temp_low.pack(side= tk.LEFT, anchor = "sw",padx=self.PADDING, pady=self.PADDING)
            #self.daily_weather_text.pack(side = tk.LEFT , padx=self.PADDING+4,pady=self.PADDING)
            #load icon
            self.img_small = ImageTk.PhotoImage(Image.open('./img/'+day["weather"][0]['icon']+'.png').resize((50, 50)))
            self.daily_weather_icon.delete("all")
            self.daily_weather_icon.create_image(30,0, anchor="nw", image=self.img_small)
            self.daily_weather_icon.image = self.img_small

            #radio button
            self.radiobutton = tk.Radiobutton(self.daily_item, value =index, variable = self.i, command=self.Daily_RadioBtnSelected, bg= 'white')
            self.radiobutton.pack()
            self.i.set(0)
    
    def load_daily_detail(self):


        #detail frame
        self.daily_detail_frame = tk.Frame(self.forecast_tab, bg = 'white')
         
        self.daily_detail_frame.pack(side = tk.TOP )
        
        # set data for plot
        graphData = self.weather_json['daily'][self.i.get()]['temp']
        x = [0,1,2,3]
        y = [graphData['morn'],graphData['day'],graphData['eve'],graphData['night']]
        
        xnew = np.linspace(0, 4, 20) 
        bspline = interpolate.make_interp_spline(x, y)
        y_smoothed = bspline(xnew)
                

        # the figure that will contain the plot 
        self.hourly_fig = plt.Figure(figsize=(4,2), dpi=100, constrained_layout=True)

        # adding the subplot 
        self.ax = self.hourly_fig.add_subplot(111)

        # plotting the graph 
        self.ax.set_title('Day Details')
        self.line, = self.ax.plot(xnew,y_smoothed,'black') 
        self.ax.set_ylim( 0,45)
        self.fill_day = self.ax.fill_between(xnew,y_smoothed, color='moccasin')

        self.line_fig  = FigureCanvasTkAgg(self.hourly_fig, self.daily_detail_frame)
        self.line_fig.get_tk_widget().pack(fill = tk.X)
        self.line_fig.draw()

        #data
        #sunrise, sunset, temp(day,night,evening,morning,min,max), feels like, pressure, humidity, dew,wind,weather, clouds,pop,uvi
        #fetch data
        daily_data = self.weather_json['daily'][self.i.get()]

        sunrise = daily_data['sunrise']
        sunrise_time = datetime.datetime.fromtimestamp(sunrise)
        sunrise_string = str(sunrise_time.strftime("%I:%M %p"))

        sunset = daily_data['sunset']
        sunset_time = datetime.datetime.fromtimestamp(sunset)
        sunset_string = str(sunset_time.strftime("%I:%M %p"))

        temp = daily_data['temp']
        temp_max = temp['max']
        temp_min = temp['min']
        
        feels_like = daily_data['feels_like']
        clouds_percent = daily_data['clouds']
        rain_prob = daily_data['pop']*100
         
       
        humidity = daily_data['humidity']
        wind_speed = daily_data['wind_speed']
        uvi = daily_data['uvi']
        pressure = daily_data['pressure']
        dew_point = daily_data['dew_point']
      

        #strings
        weather_string = "Day Description: " + daily_data['weather'][0]['description']
        sun_rise_set = "Sunrise at " + str(sunrise_string) + "\nSunset at " + str(sunset_string)  
        temp_string = "Max Temperature: " + str(temp_max)+"°" + " feels like  " + str(feels_like['day']) +"°"+ "\nMin Temperature: " + str(temp_min) +"°"+ " feels like  " + str(feels_like['night'])+"°"
         
        group_info1 = "Rain chance: " + str(rain_prob) +"%" + "\nHumidity: " +str(humidity)+"%" +"\tUV Index: " + str(uvi) 
        group_info2 = "Wind speed: " + str(rain_prob) + "km/s" + "\tClouds: "+ str(clouds_percent) + "%"
        group_info3 = "Atmospheric Conditions: \nPressure: "+ str(pressure)+"hPa" + "\nDew Point: "+ str(dew_point)+"°"



      
        self.daily_detail_frame_bottom = tk.Frame(self.daily_detail_frame, bg= 'red')
        self.daily_detail_frame_bottom.pack(fill = tk.BOTH, expand = True )

        self.top_detail = tk.Frame(self.daily_detail_frame_bottom)
        self.top_detail.pack(fill=tk.BOTH, expand= True)
        self.lab1 = tk.Label(self.top_detail, text = weather_string, font = 30, bg= 'white', padx=8, pady=8)
        self.lab2 = tk.Label(self.top_detail, text = sun_rise_set, font = 30, padx=8, pady=8)

        self.mid_detail = tk.Frame(self.daily_detail_frame_bottom)
        self.mid_detail.pack(fill=tk.BOTH, expand= True)
        self.lab3 = tk.Label(self.mid_detail, text = temp_string, font = 30, padx=8, pady=8)
        self.lab4 = tk.Label(self.mid_detail, text = group_info1, font = 30,bg= 'white', padx=8, pady=8)

        self.bot_detail = tk.Frame(self.daily_detail_frame_bottom)
        self.bot_detail.pack(fill=tk.BOTH, expand= True)
        self.lab5 = tk.Label(self.bot_detail, text = group_info2, font = 30,bg= 'white', padx=8, pady=8)
        self.lab6 = tk.Label(self.bot_detail, text = group_info3, font = 30 , padx=8, pady=8)

      
        self.lab1.pack(side= tk.LEFT,fill=tk.BOTH, expand= True)
        self.lab2.pack(side= tk.LEFT,fill=tk.BOTH, expand= True)
        self.lab3.pack(side= tk.LEFT,fill=tk.BOTH, expand= True)
        self.lab4.pack(side= tk.LEFT,fill=tk.BOTH, expand= True)
        self.lab5.pack(side= tk.LEFT,fill=tk.BOTH, expand= True)
        self.lab6.pack(side= tk.LEFT,fill=tk.BOTH, expand= True)
     
    def update_daily_detail(self):
       
        
         
        graphData = self.weather_json['daily'][self.i.get()]['temp']
       
        x = [0,1,2,3]
        y = [graphData['morn'],graphData['day'],graphData['eve'],graphData['night']]
        
        xnew = np.linspace(0, 4, 20) 
        bspline = interpolate.make_interp_spline(x, y)
        y_smoothed = bspline(xnew)
        #update data
        self.line.set_ydata(y_smoothed)
        self.ax.set_ylim( 0,45)
        self.fill_day.remove()
         
        self.fill_day = self.ax.fill_between(xnew,y_smoothed, color='moccasin')
        #refresh ui
        self.hourly_fig.canvas.draw()
        self.hourly_fig.canvas.flush_events()

         
        #fetch data
        daily_data = self.weather_json['daily'][self.i.get()]

        sunrise = daily_data['sunrise']
        sunrise_time = datetime.datetime.fromtimestamp(sunrise)
        sunrise_string = str(sunrise_time.strftime("%I:%M %p"))

        sunset = daily_data['sunset']
        sunset_time = datetime.datetime.fromtimestamp(sunset)
        sunset_string = str(sunset_time.strftime("%I:%M %p"))

        temp = daily_data['temp']
        temp_max = temp['max']
        temp_min = temp['min']

        feels_like = daily_data['feels_like']
        clouds_percent = daily_data['clouds']
        rain_prob = daily_data['pop']*100
         
       
        humidity = daily_data['humidity']
        wind_speed = daily_data['wind_speed']
        uvi = daily_data['uvi']
        pressure = daily_data['pressure']
        dew_point = daily_data['dew_point']
      

       #strings
        weather_string = "Day Description: " + daily_data['weather'][0]['description']
        sun_rise_set = "Sunrise at " + str(sunrise_string) + "\nSunset at " + str(sunset_string)  
        temp_string = "Max Temperature: " + str(temp_max)+"°" + " feels like  " + str(feels_like['day']) +"°"+ "\nMin Temperature: " + str(temp_min) +"°"+ " feels like  " + str(feels_like['night'])+"°"
         
        group_info1 = "Rain chance: " + str(rain_prob) +"%" + "\nHumidity: " +str(humidity)+"%" +"\tUV Index: " + str(uvi) 
        group_info2 = "Wind speed: " + str(rain_prob) + "km/s" + "\tClouds: "+ str(clouds_percent) + "%"
        group_info3 = "Atmospheric Conditions: \nPressure: "+ str(pressure)+"hPa" + "\nDew Point: "+ str(dew_point)+"°"





        self.lab1.config(text = weather_string)
        self.lab2.config(text = sun_rise_set)
        self.lab3.config(text = temp_string)
        self.lab4.config(text = group_info1)
        self.lab5.config(text = group_info2)
        self.lab6.config(text = group_info3)
         


         
        
        

        

## Misc Functions

    def resize_window(self, event):
        self.WIDTH = event.width
        self.HEIGHT = event.height
        print("resize window call")
        
        self.overview_canvas.coords(self.overview_bg, self.WIDTH/2,self.HEIGHT/2)
        self.overview_canvas.coords(self.location_text, self.WIDTH//2,self.HEIGHT *0.12)
        self.overview_canvas.coords(self.weather_icon_pic, self.WIDTH//2-150,self.HEIGHT*0.25)
        self.overview_canvas.coords(self.temp_lbl, self.WIDTH//2,self.HEIGHT*0.35)
        self.overview_canvas.coords(self.c_button_window, self.WIDTH//2+100,self.HEIGHT*0.25)
        self.overview_canvas.coords(self.weather_text_lbl, self.WIDTH//2,self.HEIGHT*0.6)
        self.overview_canvas.coords(self.overview_info_text, self.WIDTH//2,self.HEIGHT*0.75)
        self.overview_canvas.coords(self.last_updated_lbl, self.WIDTH//2,self.HEIGHT*0.9)

    def Daily_RadioBtnSelected(self):
        print(json.dumps(self.i.get()))
        self.update_daily_detail()



    def load_bg(self):
        img_height = 300
        now = datetime.datetime.now() 
         
        
        if int((now.strftime('%H'))) >= 18 or int((now.strftime('%H'))) <= 6: 
            img_file = Image.open('./img/night-bg.png')
            if img_file.size != (self.WIDTH, img_height):
                img_file = img_file.resize((2000, img_height+50), Image.ANTIALIAS)
            self.background_image = ImageTk.PhotoImage(img_file)
            print("night", img_file.size)
            
            return self.background_image
        else: 
            img_file = Image.open('./img/day-bg.png')
            if img_file.size != (self.WIDTH, img_height):
                img_file = img_file.resize((2000, img_height+150), Image.ANTIALIAS)
            self.background_image = ImageTk.PhotoImage(img_file)
            print("day")
            return self.background_image
     
    def open_image(self, icon):
    
        self.img_large = ImageTk.PhotoImage(Image.open('./img/'+icon+'.png').resize((70, 70)))
        self.overview_canvas.delete(self.weather_icon_pic)
        self.weather_icon_pic = self.overview_canvas.create_image(self.WIDTH//2-150, 250*0.25, anchor='nw',image=self.img_large)
   
    def clear_text(self):
             self.search_box.delete(0, 'end')

    def map_RadioBtnSelected(self):
        self.map_canvas.destroy()
        self.load_mapfig(self.location)

 

  
        

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Weather Analysis App")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
     

    WIDTH = 1000
    HEIGHT = 700
    root.geometry("%sx%s" % (WIDTH, HEIGHT))
    

    model = Model()
    view = View(root)
    view.weather_json = model.get_weathertest()
    view.location = model.get_location("Melbourne")
    view.setup()

     
    root.mainloop()
 

