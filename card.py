from typing import Self

from PIL import Image, ImageTk

import config
import gui
import imaging

BOLD = gui.font.Font(family="Lucida Console", size=config.get("text_size"), weight="bold")
class Card:
    def __init__(self,color:int,value:int,x=300,y=300):
        self._get_image(color, value)

        self._initial_draw(x, y)

        self.highlighted = False
        self.motion = False

    def redraw(self):
        for item in self.id:
            gui.c.delete(item)
        self._photo_image = ImageTk.PhotoImage(self.image)
        self.id[0] = gui.c.create_image(self.x-self.width/2,self.y-self.height/2,image=self._photo_image,anchor="nw")

        self.id[1] = gui.c.create_text(*self.get_text_coords(self.x,self.y),font=BOLD,text=self.hex_code,fill="white")
    
    def get_text_coords(self,x,y):
        text_x, text_y = config.get("TEXT_PLACEMENT")

        text_x *= self.width
        text_y *= self.height
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

        self.width *= scale
        self.height *= scale

        self.bounding_box = (self.x,self.y,self.x+self.width,self.y+self.height)
    
    def move_to(self,x,y):

        self.x = x
        self.y = y
        x -= self.width/2
        y -= self.height/2
        gui.c.moveto(self.id[0],x,y)
        gui.c.moveto(self.id[1],*self.get_text_coords(x,y))

        self.bounding_box = (x,y,x+self.width,y+self.height)

    def smooth_move_to(self,x,y,ms,_frame=0):
        self.motion = True

        dx = x - self.x
        dy = y - self.y
        frames = ms/1000*config.get("fps") - _frame
        move_x = dx/frames
        move_y = dy/frames
        gui.c.move(self.id[0],move_x,move_y)
        gui.c.move(self.id[1],move_x,move_y)

        self.x += move_x
        self.y += move_y
        if frames > _frame:
            gui.window.after(1000//config.get("fps"), lambda: self.smooth_move_to(x,y,ms,_frame+1))
            return
        
        self.motion = False

    
    def highlight(self):
        if self.motion:
            return
        if not self.highlighted:
            x = self.x
            y = self.y - config.get("highlight_movement")
            self.smooth_move_to(x,y,100)
            self.highlighted = True

    def dehighlight(self):
        if self.motion:
            return
        if self.highlighted:
            x = self.x
            y = self.y + config.get("highlight_movement")
            self.smooth_move_to(x,y,100)
            self.highlighted = False

    def _get_image(self, color, value):
        self.tileset_coords = gui.card_tileset.index_to_coords(value)
        self.color = color
        self.value = value
        if value in config.get("wild_cards"):
            self.color = 0
            self.image = gui.card_tileset.get(*self.tileset_coords)
            self.hex_code = ""
        else:
            self.image = imaging.shift(gui.card_tileset.get(*self.tileset_coords),self.color)
            self.hex_code = imaging.rgb_to_hex(*imaging.red_shift(color))

    def _initial_draw(self, x, y):
        self.id = [None,None]
        self.scale_value = 1

        self.width: int = config.get("card_width")
        self.height: int = config.get("card_height")
        
        self.x = x + self.width/2
        self.y = y + self.height/2

        self.bounding_box = (x,y,x+self.width,y+self.height)

        self.redraw()

    def __lt__(self,other:Self):
        if self.value == other.value:
            return self.color < other.color
        return self.value < other.value
    
    def __gt__(self,other:Self):
        if self.value == other.value:
            return self.color > other.color
        return self.value > other.value

    def __eq__(self,other:Self):
        return self.value == other.value and self.color == other.color

    def __ne__(self,other:Self):
        return not(self == other)
    
    def __ge__(self,other:Self):
        if self.value == other.value:
            return self.color >= other.color
        return self.value >= other.value
    
    def __le__(self,other:Self):
        if self.value == other.value:
            return self.color <= other.color
        return self.value <= other.value