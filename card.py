import gui
import imaging
from PIL import Image,ImageTk

class Card:
    def __init__(self,color:int,value:int):
        gui.c.create_rectangle(300,300,502,603,width=5)

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
