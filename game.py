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
        self.button = 0

    def inside(self,bounding_box):
        return (bounding_box[0] < self.x < bounding_box[2]) and (bounding_box[1] < self.y < bounding_box[3])
    
mouse = Cursor()

def mouse_motion(event):
    mouse.x = event.x
    mouse.y = event.y

def game_loop(delta):
    for card in temp_hand:
        if mouse.inside(card.bounding_box):
            card.highlight()
        else:
            card.dehighlight()
    

    gui.window.after(FRAME_TIME,lambda: game_loop(FRAME_TIME))

gui.window.after(FRAME_TIME,lambda: game_loop(FRAME_TIME))
gui.window.bind("<Motion>",mouse_motion)