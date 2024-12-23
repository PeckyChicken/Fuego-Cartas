import card
import config
import gui
import hand

a = card.Card(180,11)
a.scale(0.5)
b = card.Card(180,12)
b.scale(0.5)
player_hand = hand.Hand((config.get("window_width")/2,config.get("hand_y")),[a,b])
player_hand.draw_hand()

gui.window.mainloop()