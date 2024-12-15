from PIL import Image, ImageTk

import config
import gui
import imaging


class Card:
    def __init__(self,color:int,value:int):
        self.tileset_coords = gui.card_tileset.index_to_coords(value)
        self.color = color

        self.image = imaging.shift(gui.card_tileset.get(*self.tileset_coords),color)

        self.id = [None]
        self.redraw()

    def redraw(self):
        if self.id[0]:
            gui.c.delete(self.id[0])
        self._photo_image = ImageTk.PhotoImage(self.image)
        self.id[0] = gui.c.create_image(300,300,image=self._photo_image,anchor="nw")   

    def scale(self,scale):
        self.image = imaging.scale(self.image,scale)
        self.redraw()
    
    def move_to(self,x,y):
        width,height = self.image.size
        x -= width/2
        y -= height/2
        gui.c.moveto(self.id,x,y)
