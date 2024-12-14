import gui
import imaging
from PIL import Image,ImageTk

class Card:
    def __init__(self,color:int,value:int):
        gui.c.create_rectangle(300,300,502,603,width=5)

        tileset_coords = gui.card_tileset.index_to_coords(value)
        print(gui.card_tileset.get(*tileset_coords))
        self.img = imaging.shift(gui.card_tileset.get(*tileset_coords),color)
        self.id = gui.c.create_image(300,300,image=ImageTk.PhotoImage(self.img),anchor="nw")
        print(tileset_coords,self.img,self.id)

