from turtle import width
from typing import TYPE_CHECKING, Optional, Self

from PIL import Image, ImageTk

import config
import gui
import imaging
import sounds

#Importing hand normally would cause circular imports.
#So I only import it for type checking.
if TYPE_CHECKING:
    from hand import Hand
class Card:
    HIGHLIGHTS: list[Self] = []
    MOTION = False
    
    def __init__(self,color:int,value:int,x=300,y=300,hand:Optional["Hand"]=None):
        self.font_size = config.get("text_size")
        self.font = gui.font.Font(family="Lucida Console", size=config.get("text_size"), weight="bold")

        self.face_up = True

        self._get_image(color, value)

        self._initial_render(x, y)

        self.highlighted = False
        self.motion = False
        self.hand = hand
        


    def redraw(self):
        for item in self.id:
            gui.c.delete(item)
        self._photo_image = ImageTk.PhotoImage(self.image)
        self.id[0] = gui.c.create_image(self.x-self.width/2,self.y-self.height/2,image=self._photo_image,anchor="nw")

        if self.face_up:
            self.id[1] = gui.c.create_text(*self.get_text_coords(self.x,self.y),font=self.font,text=self.hex_code,fill="white")
    
    def get_text_coords(self,x,y):
        text_x, text_y = config.get("TEXT_PLACEMENT")

        text_x *= self.width
        text_y *= self.height
        text_x += x
        text_y += y

        x_offset = self.font_size*len(self.hex_code)/2
        text_x -= x_offset

        return text_x, text_y
    
    def size(self):
        return self.image.size

    def scale(self,scale):
        '''Scales the card down or up in size by a relative value.'''
        self.image = imaging.scale(self.image,scale)
        self.font_size *= scale
        self.font.configure(size=round(self.font_size))

        self.redraw()
        self.scale_value *= scale

        self.width *= scale
        self.height *= scale

        self.bounding_box = (self.x,self.y,self.x+self.width,self.y+self.height)

    def rescale(self,scale):
        '''Unlike Card.scale, this function scales to an absolute value rather than a relative value.'''

        scale = scale/self.scale_value
        self.scale(scale)

    def fix_image(self):
        '''Constant rescaling of an image can cause it to become blurry. This function resets the image to its original size and then rescales it from there.'''

        self._get_image(self.color,self.value)
        self.image = imaging.scale(self.image,self.scale_value)

    def move_to(self,x,y,update_bounding_box=True):

        self.x = x
        self.y = y
        x -= self.width/2
        y -= self.height/2
        gui.c.moveto(self.id[0],x,y)
        gui.c.moveto(self.id[1],*self.get_text_coords(x,y))

        if update_bounding_box:
            self.bounding_box = (x,y,x+self.width,y+self.height)

    def smooth_move_to(self, dest_x, dest_y, ms, easing=1, update_bounding_box=False, _frame=0, _original_x=None, _original_y=None):
        self.motion = True
        self.MOTION = True
        _original_x = _original_x or self.x
        _original_y = _original_y or self.y

        frames = (ms / 1000) * config.get("fps")
        ratio_complete = (_frame / frames) ** easing

        x = _original_x + (dest_x - _original_x) * ratio_complete
        y = _original_y + (dest_y - _original_y) * ratio_complete

        self.move_to(x, y, update_bounding_box)

        if frames > _frame:
            gui.window.after(1000 // config.get("fps"), lambda: self.smooth_move_to(dest_x, dest_y, ms, easing, update_bounding_box, _frame + 1, _original_x, _original_y))
            return
        self.motion = False
        self.MOTION = False
        self.move_to(dest_x, dest_y, update_bounding_box)

    
    def highlight(self):
        if self.motion:
            return
        if not self.highlighted:
            sounds.play_sound(sounds.hover_sound)
            if self not in self.HIGHLIGHTS:
                self.HIGHLIGHTS.append(self)
            self.HIGHLIGHTS.sort(key=lambda x: x.get_hand_position(),reverse=True)

            x = self.x
            y = self.y - config.get("highlight_movement")
            self.smooth_move_to(x,y,100/config.get("game_speed"),easing=0.5)
            self.highlighted = True

    def dehighlight(self):
        if self.motion:
            return
        if self.highlighted:
            if self in self.HIGHLIGHTS:
                self.HIGHLIGHTS.remove(self)
            self.HIGHLIGHTS.sort(key=lambda x: x.get_hand_position(),reverse=True)

            x = self.x
            y = self.y + config.get("highlight_movement")
            self.smooth_move_to(x,y,100/config.get("game_speed"),easing=0.5)
            self.highlighted = False

    def get_hand_position(self):
        if not self.hand:
            return 0
        return self.hand.hand.index(self)

    def remove_from_hand(self):
        if not self.hand:
            return
        self.hand.remove_card(self)
        self.hand = None
    
    def add_to_hand(self,hand: "Hand"):
        self.hand = hand
        self.hand.add_cards([self])

    def destroy(self):
        self.remove_from_hand()
        for item in self.id:
            gui.c.delete(item)
        self.id.clear()
    
    def flip(self):
        self.face_up = not self.face_up
        if self.face_up:
            self._get_image(self.color,self.value)
        else:
            self.image = gui.card_tileset.get(8,1)
        self.image = imaging.scale(self.image,self.scale_value)
        self.redraw()

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

    def _initial_render(self, x, y):
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
    
    def __ge__(self,other:Self):
        if self.value == other.value:
            return self.color >= other.color
        return self.value >= other.value
    
    def __le__(self,other:Self):
        if self.value == other.value:
            return self.color <= other.color
        return self.value <= other.value