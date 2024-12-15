import card
import config
import gui

class Hand:
    def __init__(self,coords,hand: list[card.Card]):
        self.coords = coords
        self.width: int = config.get("hand_max_width")
        self.height: int = config.get("card_height")
        self.scale: float = config.get("hand_card_scale")

        self.draw_space()
        self.hand = hand

    
    def draw_space(self):
        x1 = self.coords[0]-self.width/2
        y1 = self.coords[1]-(self.height/2)*self.scale
        x2 = self.coords[0]+self.width/2
        y2 = self.coords[1]+(self.height/2)*self.scale
        self.id = gui.c.create_rectangle(x1,y1,x2,y2,width=5)

    def draw_hand(self):
        ...
        
