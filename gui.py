import math
import tkinter as Tk
from typing import Self

from PIL import Image, ImageTk
from PIL.ImageFile import ImageFile

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

class Tileset:
    def __init__(self,image: ImageFile,tile_width,tile_height):
        self.image: ImageFile = image
        self.tile_width: int = tile_width
        self.tile_height: int = tile_height
    
    def get(self,x:int,y:int):
        crop_left = self.tile_width * x
        crop_right = self.tile_width * (x+1)
        crop_upper = self.tile_height * y
        crop_lower = self.tile_height * (y+1)
        print(crop_left,crop_right,crop_upper,crop_lower)

        return self.image.crop((crop_left,crop_upper,crop_right,crop_lower))     

card_tileset = Tileset(Image.open("Assets/cards.png"),config.get("card_width"),config.get("card_height"))


img = ImageTk.PhotoImage(card_tileset.get(0,1))

c.create_image(300,300,image=img)