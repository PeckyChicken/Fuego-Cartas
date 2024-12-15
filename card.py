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

def draw_hand_space():
    coords = config.get("hand_coords")
    width = config.get("hand_max_width")
    height = config.get("card_height")
    scale = config.get("hand_card_scale")

    x1 = coords[0]-width/2
    y1 = coords[1]-(height/2)*scale
    x2 = coords[0]+width/2
    y2 = coords[1]+(height/2)*scale

    gui.c.create_rectangle(x1,y1,x2,y2,width=5)

draw_hand_space()