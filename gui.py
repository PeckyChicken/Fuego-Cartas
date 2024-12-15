import math
import tkinter as Tk
from typing import Self

from PIL import Image, ImageTk
from PIL.ImageFile import ImageFile

import config
import imaging

window = Tk.Tk()
window.geometry(f"{config.get("window_width")}x{config.get("window_height")}")
window.title("Hexo")
window.attributes('-fullscreen',config.get("fullscreen"))

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
        pixel_width, pixel_height = image.size
        self.width = pixel_width/tile_width
        self.height = pixel_height/tile_height

    def get(self,x:int,y:int):
        if not (0 <= x < self.width) or not(0 <= y < self.height):
            raise IndexError(f"{x=}, {y=} is out of range of Tileset.")
            return None
        
        crop_left = self.tile_width * x
        crop_right = self.tile_width * (x+1)
        crop_upper = self.tile_height * y
        crop_lower = self.tile_height * (y+1)

        return self.image.crop((crop_left,crop_upper,crop_right,crop_lower))

    def index_to_coords(self,index):
        y,x = divmod(index,self.width)
        return x,y

card_tileset = Tileset(Image.open("Assets/cards.png"),config.get("card_width"),config.get("card_height"))

window.bind("<Escape>",lambda _: window.destroy())