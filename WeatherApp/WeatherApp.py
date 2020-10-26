
from controller import Controller

import tkinter as tk



if __name__ == "__main__":
    # Create an instance of Tk. This is popularly called 'root' But let's
    # call it mainwin (the 'main window' of the application. )
    mainwin = tk.Tk()
    WIDTH = 1000
    HEIGHT = 700
    mainwin.geometry("%sx%s" % (WIDTH, HEIGHT))
  
    mainwin.title("Weather Analysis App")
    
    mainwin.attributes('-alpha', 0.0)    
    app = Controller(mainwin)
    mainwin.after(0, mainwin.attributes, "-alpha", 1.0)
  
    mainwin.mainloop()        