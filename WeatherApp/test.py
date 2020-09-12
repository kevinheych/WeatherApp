from tkinter import *

root = Tk()

canvas = Canvas(root, width=730, height=600)
canvas.pack(fill="both", expand=True)

bgImg = PhotoImage(file="./img/night-bg.png")

canvas.create_image(370, 330, image=bgImg)

l1 = Label(canvas, text="Hello, world")
e1 = Entry(canvas)
t1 = Text(canvas)

l1.grid(row=0, column=0, sticky="ew", padx=10)
e1.grid(row=1, column=1, sticky="ew")
t1.grid(row=2, column=2, sticky="nsew")

canvas.grid_rowconfigure(2, weight=1)
canvas.grid_columnconfigure(2, weight=1)

root.mainloop()