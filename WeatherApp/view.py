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


class ResizingCanvas(tk.Canvas):
    def __init__(self,parent,**kwargs):
        tk.Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)
        

class View:
    background_image = 0

    def __init__(self,parent):
        style = ttk.Style(parent)
        style.configure('lefttab.TNotebook', tabposition='wn')

        #data test
        self.model = Model()
        self.weather_json = self.model.get_weathertest()
        self.i = tk.IntVar()
        self.i.set(0)
        self.layer_i = tk.StringVar()
        self.layer_i.set("temp_new")
        

        self.container = parent
        self.WIDTH = 700
        self.HEIGHT = 1000
        self.PADDING = 3
        self.bg_color = 'white'
        

    def setup(self):
        self.tab_bar()

        #Forecast sections
        self.header_bar()

        self.overview_section()
        self.next_48hrs()
        self.daily_section()
        self.load_daily_detail()

        #Map section
        self.load_map_section()


         

 
 
## GUI 

    def tab_bar(self):  
        #The tab bar
        self.notebook = ttk.Notebook(self.container, style='lefttab.TNotebook', width = self.WIDTH, height = self.HEIGHT)
        self.notebook.place(x=0, y=0, relwidth=1, relheight=1)
        #Make Tabs
        self.forecast_tab = tk.Frame(self.notebook)
        self.map_tab = tk.Frame(self.notebook)

        self.notebook.add(self.forecast_tab, text='Forecast')
        self.notebook.add(self.map_tab, text='Map')


    def load_map_section(self):
        self.map = Map()

        #change layers
        #add radiobutton
        LAYERS = [
            ("Clouds","clouds_new"),
            ("Precipitation","precipitation_new"),
            ("Sea level pressure","pressure_new"),
            ("Wind speed","wind_new"),
            ("Temperature","temp_new"),
        ]

        self.layer_btn_frame = tk.Frame(self.map_tab)
        self.layer_btn_frame.pack(side=tk.BOTTOM)
        for text, layer in LAYERS:
            self.btn = tk.Radiobutton(self.layer_btn_frame, text= text, variable=self.layer_i,value=layer, command = self.map_RadioBtnSelected) 
            self.btn.pack(side=tk.LEFT)
        
        #map fig
        self.load_mapfig()


    def load_mapfig(self):
        self.map_canvas = tk.Canvas(self.map_tab, bg= 'blue')
        self.map_canvas.pack(side=tk.BOTTOM, expand = True)
        self.map_fig = plt.Figure()
        self.map_ax = self.map.map(self.map_fig, self.layer_i.get())
        self.map_widget  = FigureCanvasTkAgg(self.map_fig, self.map_canvas)
        self.map_widget.get_tk_widget().pack(fill = tk.X)
        self.map_widget.draw()

    def map_RadioBtnSelected(self):
        self.map_canvas.destroy()
        self.load_mapfig()


    def header_bar(self):
        img = Image.open("./img/search_icon.png")
        img = img.resize((20,20), Image.ANTIALIAS)

        self.btn_icon = ImageTk.PhotoImage(img)
        #self.img_small = ImageTk.PhotoImage(Image.open('./img/'+day["weather"][0]['icon']+'.png').resize((50, 50)))

        self.header_frame = tk.Frame(self.forecast_tab)

        self.search_box = tk.Entry(self.header_frame)
        self.search_btn = tk.Button(self.header_frame, image = self.btn_icon)

        self.header_frame.pack(fill = tk.X)
        self.search_btn.pack(side = tk.RIGHT)
        self.search_box.pack(side = tk.RIGHT)
        
    def overview_section(self):
        #overview section
        canvas_height = 250
        canvas_width = self.WIDTH
        current = self.weather_json['current'] 
        self.overview_canvas = ResizingCanvas(self.forecast_tab,  height = canvas_height, bg = 'white',highlightthickness=0)
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

    def daily_section(self):
        
         #daily section
        self.scroll_canvas = tk.Canvas(self.forecast_tab, height= 135, width = 900)
        self.scrollbar_daily = tk.Scrollbar(self.forecast_tab, orient = 'horizontal', command=self.scroll_canvas.xview)
        
        self.daily_frame = tk.Frame(self.scroll_canvas)

       
        self.load_daily_items()

        self.scroll_canvas.create_window(0, 0, anchor='nw', window=self.daily_frame)
        self.scroll_canvas.update_idletasks()
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox('all'), xscrollcommand=self.scrollbar_daily.set)
        self.scrollbar_daily.pack(fill=tk.X, side=tk.TOP)
        self.scroll_canvas.pack( padx=self.PADDING, pady=self.PADDING)

        #daily detail 

        self.daily_detail_frame = tk.Frame(self.forecast_tab, width= self.WIDTH+200,height = 200)
        self.daily_detail_frame.pack_propagate(False)
        self.daily_detail_frame.pack(side = tk.TOP)
        print(self.weather_json['daily'][0])
        
    def load_daily_items(self):
         #daily item 
        daily=  self.weather_json['daily']
        for index, day in enumerate(daily):
            
            date = datetime.datetime.fromtimestamp(day['dt'])
            temp = day['temp']
            #create daily item
            self.daily_item = tk.Frame(self.daily_frame)
 
            self.daily_date_lbl = tk.Label(self.daily_item, 
                                text= date.strftime("%a %d"), 
                                font=30, width = 10)
            self.daily_weather_icon = tk.Canvas(self.daily_item, width=35, height = 40 )
            self.daily_temp_fr = tk.Frame(self.daily_item)
            self.daily_temp_high = tk.Label(self.daily_temp_fr, text=str(round(temp['max']))+"°", font=(None,20))
            self.daily_temp_low = tk.Label(self.daily_temp_fr, text=str(round(temp['min']))+"°",font=(None,16), foreground ='grey')
            self.daily_weather_text = tk.Label(self.daily_item, text = day['weather'][0]['main'] )
            
            #load daily item widgets
            self.daily_item.pack(side = tk.LEFT, padx=self.PADDING, pady=self.PADDING)
            self.daily_date_lbl.pack(anchor = "w")
            self.daily_weather_icon.pack(fill = tk.X)
            self.daily_temp_fr.pack(anchor = "w")
            self.daily_temp_high.pack(side= tk.LEFT, anchor = "s", padx=self.PADDING+4)
            self.daily_temp_low.pack(side= tk.LEFT, anchor = "sw",padx=self.PADDING, pady=self.PADDING)
            self.daily_weather_text.pack(side = tk.LEFT , padx=self.PADDING+4,pady=self.PADDING)
            #load icon
            self.img_small = ImageTk.PhotoImage(Image.open('./img/'+day["weather"][0]['icon']+'.png').resize((50, 50)))
            self.daily_weather_icon.delete("all")
            self.daily_weather_icon.create_image(30,0, anchor="nw", image=self.img_small)
            self.daily_weather_icon.image = self.img_small

            #radio button
            self.radiobutton = tk.Radiobutton(self.daily_item, value =index, variable = self.i, command=self.Daily_RadioBtnSelected)
            self.radiobutton.pack()
            self.i.set(0)
    
    def next_48hrs(self):
        
        self.hourly_frame = tk.Frame(self.forecast_tab)
        self.hourly_frame.pack()


        graphData = self.weather_json['hourly']
        hours = [i['dt'] for i in graphData]
        x_hours = pd.to_datetime(hours, unit = 's').strftime("%I%p %a")
        print(x_hours)
        x_incre = list(range(0, 48))

        y_temp = [i['temp'] for i in graphData]
        y_precipitation = [i['pop'] for i in graphData]
        y_windspeed = [i['wind_speed'] for i in graphData]
        print(y_temp)
        self.hourly_fig = plt.Figure( figsize=(20,3))
        
        

        self.ax = self.hourly_fig.add_subplot(111)
       
        
        self.ax.set_title('Next 48 hours')
        self.ax.tick_params(  labelsize=7)
        self.line, = self.ax.plot(x_hours,y_temp,'b-') 
        #self.ax.set_xticklabels(x_hours)
        loc = plticker.MultipleLocator(base=1)
        self.ax.xaxis.set_major_locator(loc)

        self.ax.set_ylim( min(y_temp)-3,max(y_temp)+3)
        self.ax.set_xlim(0,48)
        
        plt.setp(self.ax.get_xticklabels(), rotation=-50, horizontalalignment='left',rotation_mode="anchor")
        self.hourly_fig.subplots_adjust(bottom=0.2)
        self.line_fig  = FigureCanvasTkAgg(self.hourly_fig, self.hourly_frame)
        self.line_fig.get_tk_widget().pack()
        self.line_fig.draw()    
    
    def load_daily_detail(self):
        
        # set data for plot
        graphData = self.weather_json['daily'][self.i.get()]['temp']
        x = ['Morning','Day','Evening','Night']
        y = [graphData['morn'],graphData['day'],graphData['eve'],graphData['night']]

        # the figure that will contain the plot 
        self.hourly_fig = plt.Figure(figsize=(6,5), dpi=100, constrained_layout=True)

        # adding the subplot 
        self.ax = self.hourly_fig.add_subplot(111)

        # plotting the graph 
        self.ax.set_title('Day')
        self.line, = self.ax.plot(x,y,'black') 
        self.ax.set_ylim( min(y)-3,max(y)+3)

        self.line_fig  = FigureCanvasTkAgg(self.hourly_fig, self.daily_detail_frame)
        self.line_fig.get_tk_widget().pack(fill = tk.X)
        self.line_fig.draw()

    def update_daily_detail(self):
       
        print(self.weather_json['daily'][self.i.get()])
        graphData = self.weather_json['daily'][self.i.get()]['temp']
        y = [graphData['morn'],graphData['day'],graphData['eve'],graphData['night']]

        #update data
        self.line.set_ydata(y)
        self.ax.set_ylim( min(y)-3,max(y)+3)

        #refresh ui
        self.hourly_fig.canvas.draw()
        self.hourly_fig.canvas.flush_events()

        ###TO DO: add the rest of the info 
        

## Misc Functions

    def resize_window(self, event):
        self.WIDTH = event.width
        self.HEIGHT = event.height
         
        
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
         
        print(now.strftime('%H'))
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
   
    def get_location(self):
        self.location = self.search_box.get()
        self.search_box.delete(0,'end')
        print(self.location)
  
        

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Weather Analysis App")
    WIDTH = 700
    HEIGHT = 700
    root.geometry("%sx%s" % (WIDTH, HEIGHT))
    


    view = View(root)
    view.setup()
   
    root.mainloop()
 

