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
        self.hand_ids= []

    
    def draw_space(self):
        x1 = self.coords[0]-self.width/2
        y1 = self.coords[1]-(self.height/2)*self.scale
        x2 = self.coords[0]+self.width/2
        y2 = self.coords[1]+(self.height/2)*self.scale
        self.id = gui.c.create_rectangle(x1,y1,x2,y2,width=5)

    def draw_hand(self):
        for card in self.hand:
            card.redraw()
        hand_size = len(self.hand)
        middle = self.coords[0]
        overlap = 1-config.get("card_overlap")
        offset = config.get("card_width") * (hand_size-1)/4*overlap
        draw_start = middle - offset
        for index,card in enumerate(self.hand):
            x = draw_start + index*config.get("card_width")*self.scale * overlap
            card.rescale(self.scale)
            card.move_to(x,self.coords[1])
    
    def add_cards(self,cards: list[card.Card]):
        self.hand.extend(cards)
        self.draw_hand()
    
    def remove_card(self,_card:card.Card):
        self.hand.remove(_card)
        self.draw_hand()

