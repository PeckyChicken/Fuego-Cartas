from contextvars import ContextVar
import random

import card
import config
import gui
import hand

temp_hand = [card.Card(random.randint(0,359),random.randint(0,14)) for _ in range(8)]
temp_hand.sort()

player_hand = hand.Hand((config.get("window_width")/2,config.get("hand_y")),temp_hand)
player_hand.draw_hand()

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
    highlights = 0
    #Search backward through the list to ensure the topmost card gets selected
    for hand_card in hand_cards:
        if hand_card.highlighted:
            if highlights:
                hand_card.dehighlight()
            highlights += 1
    return highlights

def game_loop(delta):
    for hand_card in player_hand.hand:
        if mouse.inside(hand_card.bounding_box):
            check_for_highlight(hand_card)
        else:
            if hand_card.highlighted:
                hand_card.dehighlight()
    

    gui.window.after(FRAME_TIME,lambda: game_loop(FRAME_TIME))

def check_for_highlight(hand_card):
    highlights = 0
    if not hand_card.highlighted and highlights == 0:
        hand_card.highlight()
    highlights = remove_duplicate_highlights(player_hand.hand)

gui.window.after(FRAME_TIME,lambda: game_loop(FRAME_TIME))

gui.window.bind("<Motion>",mouse_motion)
gui.window.bind("<Button>",mouse_click)
gui.window.bind("<ButtonRelease>",mouse_release)
