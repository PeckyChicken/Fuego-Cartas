from PIL import Image, ImageTk

import config
import gui
import imaging

BOLD = gui.font.Font(family="Cascadia Mono SemiBold", size=config.get("text_size"), weight="bold")
class Card:
    def __init__(self,color:int,value:int,x=300,y=300):
        self.tileset_coords = gui.card_tileset.index_to_coords(value)
        self.color = color
        if value in config.get("wild_cards"):
            self.color = 0
            self.image = gui.card_tileset.get(*self.tileset_coords)
            self.hex_code = ""
        else:
            self.image = imaging.shift(gui.card_tileset.get(*self.tileset_coords),self.color)
            self.hex_code = imaging.rgb_to_hex(*imaging.red_shift(color))

        self.id = [None,None]
        self.scale_value = 1
        self.x = x
        self.y = y
        self.redraw()

    def redraw(self):
        for item in self.id:
            gui.c.delete(item)
        self._photo_image = ImageTk.PhotoImage(self.image)
        self.id[0] = gui.c.create_image(self.x,self.y,image=self._photo_image,anchor="nw")


        self.id[1] = gui.c.create_text(*self.get_text_coords(self.x,self.y),font=BOLD,text=self.hex_code,fill="white")

    def findXCenter(self, canvas, item):
        coords = canvas.bbox(item)
        xOffset = (self.windowWidth / 2) - ((coords[2] - coords[0]) / 2)
        return xOffset
    
    def get_text_coords(self,x,y):
        text_x, text_y = config.get("TEXT_PLACEMENT")

        text_x *= self.size()[0]
        text_y *= self.size()[1]
        text_x += x
        text_y += y

        x_offset = config.get("text_size")*len(self.hex_code)/2
        text_x -= x_offset

        return text_x, text_y
    
    def size(self):
        return self.image.size

    def scale(self,scale):
        self.image = imaging.scale(self.image,scale)
        self.redraw()
        self.scale_value = scale
    
    def move_to(self,x,y):
        width,height = self.size()
        x -= width/2
        y -= height/2
        self.x = x
        self.y = y
        gui.c.moveto(self.id[0],x,y)
        
        gui.c.moveto(self.id[1],*self.get_text_coords(x,y))
