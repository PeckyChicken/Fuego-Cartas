import card
import config
import gui
import hand
import random

temp_hand = [card.Card(random.randint(0,359),random.randint(0,14)) for _ in range(8)]

player_hand = hand.Hand((config.get("window_width")/2,config.get("hand_y")),temp_hand)
player_hand.draw_hand()

gui.window.mainloop()