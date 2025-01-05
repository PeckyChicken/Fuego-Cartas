import random
from contextvars import ContextVar

import card
import config
import gui
import hand

player_hand = hand.Hand((config.get("window_width")/2,config.get("hand_y")),hand=[])


FRAME_TIME = 1000//config.get("fps")

class Cursor:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.clicked = False
        self.button = None

    def inside(self,bounding_box):
        return (bounding_box[0] < self.x < bounding_box[2]) and (bounding_box[1] < self.y < bounding_box[3])
    
mouse = Cursor()

def select_card_from_deck(used_cards:list[card.Card],fallback=False):
    '''Since we don't have a full list of all 8656 cards, we need to simulate the list by using weights.'''
    colored_cards: list[int] = config.get("colored_cards")
    wild_cards: list[int] = config.get("wild_cards")
    cards = colored_cards + wild_cards
    duplicates: int = config.get("card_copies")
    colors: int = config.get("card_colors")
    weights = []
    for _card in cards:
        usage_count = len([x for x in used_cards if x.value == _card])
        weights.append((colors*duplicates) - usage_count)
    if len(cards) == 0:
        if not fallback:
            raise IndexError("select_card_from_deck: All cards are used.")
        value = 14
        color = 0
        return color,value #Fallback on a wild card if all cards are used.
    value = random.choices(cards,weights,k=1)[0]

    if value in wild_cards:
        color = 0
        return color,value
    
    used_cards_of_value = [x for x in used_cards if x.value == value]
    possible_colors = list(range(colors))*duplicates
    for c in used_cards_of_value:
        possible_colors.remove(c.color)
    color = random.choice(possible_colors)

    return color,value


temp_hand: list[card.Card] = []
for _ in range(8):
    temp_hand.append(card.Card(*select_card_from_deck(temp_hand,fallback=True),hand=player_hand))

temp_hand.sort()
player_hand.add_cards(temp_hand)

player_hand.draw_hand()
    


def mouse_motion(event):
    mouse.x = event.x
    mouse.y = event.y

def mouse_click(event):
    mouse.clicked = True
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

def game_loop(delta):
    for hand_card in player_hand.hand[::-1]:
        if mouse.inside(hand_card.bounding_box):
            check_for_highlight(hand_card)
        else:
            if hand_card.highlighted:
                hand_card.dehighlight()
    

    gui.window.after(FRAME_TIME,lambda: game_loop(FRAME_TIME))



def check_for_highlight(hand_card:card.Card):
    if not hand_card.highlighted:
        if hand_card.hand:
            position = hand_card.get_hand_position()
            if not any(x.highlighted and x.get_hand_position() > position for x in card.Card.HIGHLIGHTS):
                hand_card.highlight()
            
        else:
            hand_card.highlight()
    
    card.Card.HIGHLIGHTS = remove_duplicate_highlights(player_hand.hand)
    

gui.window.after(FRAME_TIME,lambda: game_loop(FRAME_TIME))

gui.window.bind("<Motion>",mouse_motion)
gui.window.bind("<Button>",mouse_click)
gui.window.bind("<ButtonRelease>",mouse_release)
