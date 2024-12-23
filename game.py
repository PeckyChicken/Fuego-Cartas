import random

import card
import config
import gui
import hand

temp_hand = [card.Card(random.randint(0,359),random.randint(0,14)) for _ in range(8)]
temp_hand.sort()

player_hand = hand.Hand((config.get("window_width")/2,config.get("hand_y")),temp_hand)
player_hand.draw_hand()

FRAME_TIME = 60000/config.get("fps")


def game_loop(delta):
    ...


gui.window.after(FRAME_TIME,lambda: game_loop(FRAME_TIME))