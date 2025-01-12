import random
from contextvars import ContextVar
from typing import Optional

import card
import config
import gui
import hand

player_hand = hand.Hand((config.get("window_width")/2,config.get("hand_y_pos")*config.get("window_height")),hand=[])


FRAME_TIME = 1000//config.get("fps")

class Cursor:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.clicked = False
        self.clicked_this_frame = False
        self.button = None

    def inside(self,bounding_box):
        return (bounding_box[0] < self.x < bounding_box[2]) and (bounding_box[1] < self.y < bounding_box[3])
    
mouse = Cursor()

class Game:
    def __init__(self,start_card:card.Card):
        self.stack = [start_card]
        self.color = start_card.color
        self.value = start_card.value

        self.x = config.get("play_position")[0]*config.get("window_width")
        self.y = config.get("play_position")[1]*config.get("window_height")
        start_card.rescale(config.get("play_scale"))
        start_card.move_to(self.x,self.y)
    
    def validate(self,_card:card.Card):
        if _card.value in config.get("wild_cards"):
            return True
        
        return self.color == _card.color or self.value == _card.value
    
    def play(self,_card:card.Card,color=None):
        self.stack.append(_card)
        self.color = color or _card.color
        self.value = _card.value

        if not _card.face_up:
            _card.flip()

        _card.rescale(config.get("play_scale"))
        while card.Card.MOTION:
            ...
        _card.smooth_move_to(self.x,self.y,ms=200/config.get("game_speed"),update_bounding_box=True,easing=2)
        _card.remove_from_hand()

class Deck:
    def __init__(self,colored_cards:list[int]=config.get("colored_cards"),wild_cards:list[int]=config.get("wild_cards"),duplicates:list[int]=config.get("duplicates"),num_colors:int=config.get("card_colors")):
        self.used_cards: list[card.Card] = []
        self.colored_cards: list[int] = colored_cards
        self.wild_cards: list[int] = wild_cards
        self.cards = self.colored_cards + self.wild_cards
        self.duplicates = duplicates
        self.num_colors = num_colors

    def select_card(self, fallback=False) -> tuple[int, int]:
        '''Since we don't have a full list of all 10080 cards, we need to simulate the list by using weights.
        
        Returns (color, value)'''
        weights = []
        for _card in self.cards:
            usage_count = sum(1 for x in self.used_cards if x.value == _card)
            weight = self.duplicates[_card] * (self.num_colors if _card in self.colored_cards else 1) - usage_count
            weights.append(weight)

        if sum(weights) <= 0:
            if not fallback:
                raise IndexError("select_card_from_deck: All cards are used.")
            value = 13
            color = 0
            return color, value  # Fallback on a wild card if all cards are used.
        value = random.choices(self.cards, weights, k=1)[0]

        if value in self.wild_cards:
            color = 0
            return color, value
        
        used_cards_of_value = [x for x in self.used_cards if x.value == value]
        possible_colors = [x for x in range(self.num_colors)] * self.duplicates[value]
        for c in used_cards_of_value:
            possible_colors.remove(c.color)
        color = random.choice(possible_colors)

        return color, value

    def add_used_card(self, _card: card.Card):
        self.used_cards.append(_card)

deck = Deck()

def mouse_motion(event):
    mouse.x = event.x
    mouse.y = event.y

def mouse_click(event):
    mouse.clicked = True
    mouse.clicked_this_frame = True
    mouse.button = event.num

def mouse_release(event):
    mouse.clicked = False
    mouse.button = None

def remove_duplicate_highlights(hand_cards: list[card.Card]):
    highlights: list[card.Card] = []
    for hand_card in hand_cards:
        if hand_card.highlighted:
            highlights.append(hand_card)

            if highlights:
                for highlight in highlights[:-1]:
                    highlight.dehighlight()
                highlights[-1].highlight()
            highlights.sort(key=lambda x: x.get_hand_position())
    return highlights


def check_for_highlight(hand_card:card.Card):
    if not hand_card.highlighted:
        if hand_card.hand:
            position = hand_card.get_hand_position()
            if not any(x.highlighted and x.get_hand_position() > position for x in card.Card.HIGHLIGHTS):
                hand_card.highlight()
            
        else:
            hand_card.highlight()
    
    card.Card.HIGHLIGHTS = remove_duplicate_highlights(player_hand.hand)



temp_hand: list[card.Card] = []
for _ in range(9):
    _card = card.Card(*deck.select_card(fallback=True),hand=player_hand)
    if random.randint(0,1):
        _card.flip()
    temp_hand.append(_card)
    deck.add_used_card(temp_hand[-1])

temp_hand.sort()
player_hand.add_cards(temp_hand)

player_hand.draw_hand()

start_card = deck.select_card(fallback=True)
while start_card[1] in config.get("wild_cards"):
    start_card = deck.select_card(fallback=True)

start_card = card.Card(*start_card)
deck.add_used_card(start_card)
game = Game(start_card)

def game_loop(delta):
    for _card in player_hand.hand[::-1]:
        if mouse.inside(_card.bounding_box):
            check_for_highlight(_card)
        else:
            if _card.highlighted:
                _card.dehighlight()
    
    for _card in card.Card.HIGHLIGHTS:
        if mouse.clicked_this_frame and _card.hand == player_hand and game.validate(_card):
            game.play(_card)
    
    if mouse.clicked_this_frame:
        mouse.clicked_this_frame = False

    gui.window.after(FRAME_TIME,lambda: game_loop(FRAME_TIME))




gui.window.after(FRAME_TIME,lambda: game_loop(FRAME_TIME))

gui.window.bind("<Motion>",mouse_motion)
gui.window.bind("<Button>",mouse_click)
gui.window.bind("<ButtonRelease>",mouse_release)
