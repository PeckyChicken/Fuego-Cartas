import math
import tkinter as Tk
from typing import Self

from PIL import Image, ImageTk

import config

window = Tk.Tk()
window.geometry(f"{config.get("window_width")}x{config.get("window_height")}")
window.title("Hexo")

c = Tk.Canvas(window,width=config.get("window_width"),height=config.get("window_height"),bg="#77DD77")
c.pack(padx=0,pady=0)

class Point:
    def __init__(self,x: int,y: int):
        self.set_coords(x,y)

    def set_coords(self,x: int,y: int):
        self.x = x
        self.y = y
        self.coords = (x,y)

    def distance_to(self,point:Self):
        dx = abs(self.x-point.x)
        dy = abs(self.y-point.y)
        distance = math.sqrt(dx**2+dy**2)
        return distance

card_tileset = Image.open("Assets/cards.png")
img = ImageTk.PhotoImage(card_tileset)

c.create_image(50,50,image=img)