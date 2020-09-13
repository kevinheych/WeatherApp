import tkinter as tk
 
from tkinter import ttk
from PIL import Image, ImageTk
import datetime
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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

        self.container = parent
        self.WIDTH = 700
        self.HEIGHT = 700
        self.PADDING = 3
        self.bg_color = 'white'
        return

    def setup(self):
        self.create_widgets()
        self.setup_layout()

 
    def open_image(self, icon):
    
        self.img_large = ImageTk.PhotoImage(Image.open('./img/'+icon+'.png').resize((70, 70)))
        self.overview_canvas.delete(self.weather_icon_pic)
        self.weather_icon_pic = self.overview_canvas.create_image(self.WIDTH//2-150, 250*0.25, anchor='nw',image=self.img_large)
        
        #self.img_small = ImageTk.PhotoImage(Image.open('./img/'+icon+'.png').resize((35, 35)))
        #self.daily_weather_icon.delete("all")
        #self.daily_weather_icon.create_image(0,0, anchor=tk.CENTER, image=self.img_small)
        #self.daily_weather_icon.image = self.img_small

    def create_widgets(self):
        #The tab bar
        self.notebook = ttk.Notebook(self.container, style='lefttab.TNotebook', width = self.WIDTH, height = self.HEIGHT)
        self.notebook.place(x=0, y=0, relwidth=1, relheight=1)
        #Make Tabs
        self.forecast_tab = tk.Frame(self.notebook)
        self.map_tab = tk.Frame(self.notebook)

        self.notebook.add(self.forecast_tab, text='Forecast')
        self.notebook.add(self.map_tab, text='Map')

        #overview section
        canvas_height = 250
        canvas_width = self.WIDTH
        self.overview_canvas = ResizingCanvas(self.forecast_tab,  height = canvas_height, bg = 'white',highlightthickness=0)
        self.overview_canvas.pack(fill = tk.X  )
        self.notebook.update() 

        self.overview_bg = self.overview_canvas.create_image(0,0, image = self.load_bg(), anchor='nw')

        self.location_text = self.overview_canvas.create_text(
                                canvas_width//2, canvas_height*0.12, 
                                text='Location', 
                                fill = 'white', 
                                font=(None, 15), 
                                anchor=tk.CENTER)

        self.weather_icon_pic =  self.overview_canvas.create_image(canvas_width//2-150, canvas_height*0.25, anchor='nw')
        self.temp_lbl =  self.overview_canvas.create_text(
                            canvas_width//2, canvas_height*0.35, 
                            text='11°', fill = 'white', 
                            font=(None, 55), 
                            anchor=tk.CENTER)
                            
        self.c_button  = tk.Button(self.overview_canvas, text = "C",font=(None, 15) )
        self.c_button_window = self.overview_canvas.create_window(
                            canvas_width//2+100, canvas_height*0.25, 
                            anchor='nw', 
                            window= self.c_button)
        
        self.weather_text_lbl = self.overview_canvas.create_text(
                            canvas_width//2, canvas_height*0.6, 
                            text='Clouds', 
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


        
    
        #daily section
        self.scroll_canvas = tk.Canvas(self.forecast_tab, height= 130)
        

        self.scrollbar_daily = tk.Scrollbar(self.forecast_tab, orient = 'horizontal', command=self.scroll_canvas.xview)
        
        self.daily_frame = tk.Frame(self.scroll_canvas, bg = 'green')
        #daily item 
        for x in range(8):
            self.daily_item = tk.Frame(self.daily_frame)
            self.daily_date_lbl = tk.Label(self.daily_item, 
                                text= 'Wed '+ str(x+1) +'th', 
                                font=30, width = 10)
            self.daily_weather_icon = tk.Canvas(self.daily_item, width=35, height = 35 )
            self.daily_temp_fr = tk.Frame(self.daily_item)
            self.daily_temp_high = tk.Label(self.daily_temp_fr, text="14°", font=(None,25))
            self.daily_temp_low = tk.Label(self.daily_temp_fr, text="7°")
            self.daily_weather_text = tk.Label(self.daily_item, text = "Cloudy")

            
            self.daily_item.pack(side = tk.LEFT, padx=self.PADDING, pady=self.PADDING)
            self.daily_date_lbl.pack(anchor = "w")
            self.daily_weather_icon.pack(anchor = "w")
            self.daily_temp_fr.pack(anchor = "w")
            self.daily_temp_high.pack(side= tk.LEFT, anchor = "sw")
            self.daily_temp_low.pack(side= tk.LEFT, anchor = "se", padx=self.PADDING, pady=self.PADDING)
            self.daily_weather_text.pack(side = tk.TOP,anchor = "w")

        self.scroll_canvas.create_window(0, 0, anchor='nw', window=self.daily_frame)
        self.scroll_canvas.update_idletasks()
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox('all'), xscrollcommand=self.scrollbar_daily.set)

        self.scroll_canvas.pack(fill= tk.X, padx=self.PADDING, pady=self.PADDING)
        self.scrollbar_daily.pack(fill=tk.X, side=tk.TOP)


        #hourly section

        self.hourly_canvas = tk.Canvas(self.forecast_tab)
        

         
    def setup_layout(self):
        return

        
    def resize_window(self, event):
        self.WIDTH = event.width
        self.HEIGHT = event.height
         
        self.overview_canvas.itemconfig(self.overview_bg, image=self.load_bg())
        self.overview_canvas.coords(self.location_text, self.WIDTH//2,self.HEIGHT *0.12)
        self.overview_canvas.coords(self.weather_icon_pic, self.WIDTH//2-150,self.HEIGHT*0.25)
        self.overview_canvas.coords(self.temp_lbl, self.WIDTH//2,self.HEIGHT*0.35)
        self.overview_canvas.coords(self.c_button_window, self.WIDTH//2+100,self.HEIGHT*0.25)
        self.overview_canvas.coords(self.weather_text_lbl, self.WIDTH//2,self.HEIGHT*0.6)
        self.overview_canvas.coords(self.overview_info_text, self.WIDTH//2,self.HEIGHT*0.75)
        self.overview_canvas.coords(self.last_updated_lbl, self.WIDTH//2,self.HEIGHT*0.9)
    
        print("resize update")

    def load_bg(self):
        img_height = 300
        now = datetime.datetime.now() 
        print(now.strftime('%H'))
        if int((now.strftime('%H'))) >= 18 or int((now.strftime('%H'))) <= 6: 
            img_file = Image.open('./img/night-bg.png')
            if img_file.size != (self.WIDTH, img_height):
                img_file = img_file.resize((self.WIDTH, img_height), Image.ANTIALIAS)
            self.background_image = ImageTk.PhotoImage(img_file)
            print("night", img_file.size)
            
            return self.background_image
        else: 
            img_file = Image.open('./img/day-bg.png')
            if img_file.size != (self.WIDTH, img_height):
                img_file = img_file.resize((self.WIDTH, img_height), Image.ANTIALIAS)
            self.background_image = ImageTk.PhotoImage(img_file)
            print("day")
            return self.background_image
     

  
        

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Weather Analysis App")
    WIDTH = 700
    HEIGHT = 700
    root.geometry("%sx%s" % (WIDTH, HEIGHT))


    view = View(root)
    view.setup()
   
    root.mainloop()
 

