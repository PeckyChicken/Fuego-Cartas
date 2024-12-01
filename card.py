import gui
import colors
from PIL import Image,ImageTk

class Card:
    def __init__(self,color:int,value:int):
        img = ImageTk.PhotoImage(colors.shift(gui.card_tileset.get(0,1),78))
        gui.c.create_image(300,300,image=img)