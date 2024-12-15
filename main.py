import card
import config
import gui
import hand

player_hand = hand.Hand((config.get("window_width")/2,config.get("hand_y")),...)
a = card.Card(180,11)
a.scale(0.5)
a.move_to(*player_hand.coords)

gui.window.mainloop()