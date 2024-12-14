import gui
import colors
from PIL import Image,ImageTk

class Card:
    def __init__(self,color:int,value:int):
        tileset_coords = gui.card_tileset.index_to_coords(value)
        print(gui.card_tileset.get(*tileset_coords))
        self.img = ImageTk.PhotoImage(colors.shift(gui.card_tileset.get(*tileset_coords),color))
        gui.c.create_rectangle(300,300,502,603,width=5)
        self.id = gui.c.create_image(300,300,image=self.img)
        print(tileset_coords,self.img,self.id)

img = ImageTk.PhotoImage(colors.shift(gui.card_tileset.get(0,0),48))
id1 = gui.c.create_image(200,200,image=img)
