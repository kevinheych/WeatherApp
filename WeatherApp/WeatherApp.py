import tkinter as tk
from tkinter import ttk

WIDTH = 700
HEIGHT = 700


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
overview_frame = tk.Frame(forecast_tab, bg='white', width=300, height=300)
overview_frame.pack(padx=5, pady=5)
overview_frame.pack_propagate(False) 

lbl_location = tk.Label(overview_frame, text = "Location", font=(None, 15))
lbl_location.pack()





 
daily_frame = ttk.Labelframe(forecast_tab, text='Daily',height=150)
daily_frame.pack(fill= tk.BOTH, padx=5, pady=5)
daily_frame.pack_propagate(False) 

#daily item 1
daily_item1 = tk.Frame(daily_frame, bg='yellow')
daily_item1.pack(side = tk.LEFT, padx=5, pady=5)

label_a = tk.Label(daily_item1, text= 'Item1')
label_a.pack()
label_b = tk.Label(daily_item1, text= 'Item2')
label_b.pack()

#daily item 1
daily_item2 = tk.Frame(daily_frame, bg='blue')
daily_item2.pack(side = tk.LEFT,fill= tk.Y, padx=5, pady=5)

label_a = tk.Label(daily_item2, text= 'Item1')
label_a.pack()
label_b = tk.Label(daily_item2, text= 'Item2')
label_b.pack()

hourly_frame = ttk.Labelframe(forecast_tab, text='Hourly', height=150)
hourly_frame.pack(fill= tk.X,padx=5, pady=5)
hourly_frame.pack_propagate(False) 

 
#Make Map Tab
map_tab = tk.Frame(notebook, bg='blue')





notebook.add(forecast_tab, text='Forecast')
notebook.add(map_tab, text='Map')


root.mainloop()