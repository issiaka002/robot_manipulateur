import tkinter as tk
from PIL import Image, ImageTk
from random import choice

fen = tk.Tk()
fen.geometry('700x440')

def enter(event):
    tof = ['ferrari1.jpg', 'ferrari2.jpg', 'ferrari3.jpg', 'ferrari4.jpeg', 'ferrari5.jpg','ferrari6.jpg']
    load = Image.open(f"{choice(tof)}")
    photo = ImageTk.PhotoImage(load)
    label_image.config(image=photo)
    label_image.image=photo

def out(event):
    tof = ['ferrari1.jpg', 'ferrari2.jpg', 'ferrari3.jpg', 'ferrari4.jpeg', 'ferrari5.jpg','ferrari6.jpg']
    load = Image.open(f"{choice(tof)}")
    photo = ImageTk.PhotoImage(load)
    label_image.config(image=photo)
    label_image.image=photo

load = Image.open("ferrari1.jpg")
#load.show()
photo = ImageTk.PhotoImage(load)
label_image=tk.Label(fen, image=photo)
label_image.place(x=0,y=0)
label_image.bind("<Enter>", enter)
label_image.bind("<Leave>", out)

fen.mainloop()