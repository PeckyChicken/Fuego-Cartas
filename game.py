import random
from contextvars import ContextVar
from typing import Optional

import card
import config
import gui
import hand
import imaging

player_hand = hand.Hand((config.get("window_width")/2,config.get("hand_y_pos")*config.get("window_height")),hand=[])


FRAME_TIME = 1000//config.get("fps")

class Cursor(gui.Point):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.clicked = False
        self.clicked_this_frame = False
        self.button = None    
    
mouse = Cursor()

class Game:
    def __init__(self,start_card:card.Card):
        self.stack = [start_card]
        self.color = start_card.color
        self.value = start_card.value
        self.wild_card: card.Card|None = None
        self.cover = []

        self.wild_font = _card.font.copy()
        self.wild_font["size"] = config.get("wild_text_size")

        self.x = config.get("play_position")[0]*config.get("window_width")
        self.y = config.get("play_position")[1]*config.get("window_height")
        start_card.rescale(config.get("play_scale"))
        start_card.fix_image()
        start_card.move_to(self.x,self.y)
    
    def validate(self,_card:card.Card):
        if _card.value in config.get("wild_cards"):
            return True
        
        return self.color == _card.color or self.value == _card.value
    
    def play(self,_card:card.Card,color=None):
        self.stack.append(_card)
        self.color = _card.color if color is None else color
        self.value = _card.value

        if not _card.face_up:
            _card.flip()

        if _card.value in config.get("wild_cards"):
            _card._get_image(color,_card.value)

        _card.rescale(config.get("play_scale"))
        while card.Card.MOTION:
            ...
        _card.smooth_move_to(self.x,self.y,ms=200/config.get("game_speed"),update_bounding_box=True,easing=2)
        _card.remove_from_hand()
    
    def wild_card_setup(self,_card:card.Card):
        self.wild_card = _card
        for item in self.cover:
            gui.c.delete(item)

        self.cover.clear()
        self.cover.append(gui.c.create_image(config.get("window_width")/2,config.get("window_height")/2,image=gui.cover))
        self.cover.append(gui.c.create_text(config.get("window_width")*config.get("wild_text_placement")[0],config.get("window_height")*config.get("wild_text_placement")[1],text="Select color for Wild Card.",font=self.wild_font,fill="white"))

        player_hand.render_hand()


class ColorSelection:
    def __init__(self,width=config.get("window_width"),height=config.get("window_height")):
        self.colors = range(config.get("card_colors"))
        self.cover_id = []
        self.color_ids = []
        self.text_ids = []
        self.visible = False
        self.last_darkened_color = 0
        self.width = width
        self.height = height
        
    def render_colors(self,colors=None):
        self.delete_colors()

        self.cover_id.append(gui.c.create_rectangle(0,0,self.width,self.height,fill=config.get("background_color")))

        if colors is None:
            colors = self.colors
        
        
        self.rows = config.get("wild_selection_rows")
        self.columns = len(colors)//self.rows

        self.margin = config.get("wild_selection_margin")

        self.box_width = (self.width)/self.columns - self.margin
        self.box_height= (self.height)/self.rows - self.margin

        pixel_width = self.columns*(self.box_width+self.margin) - self.margin
        pixel_height= self.rows*(self.box_height+self.margin) - self.margin

        self.start_x = self.width/2 - pixel_width/2
        self.start_y = self.height/2 - pixel_height/2

        font_size = self.box_width // len("#FF0000")

        _font = game.wild_font.copy()
        _font["size"] = int(font_size)

        for index,color in enumerate(colors):
            x = self.start_x + (index%self.columns)*(self.box_width+self.margin)
            y = self.start_y + (index//self.columns)*(self.box_height+self.margin)
            fill_color = imaging.rgb_to_hex(*imaging.red_shift(color))
            self.color_ids.append(gui.c.create_rectangle(x,y,x+self.box_width,y+self.box_height,fill=fill_color))
            self.text_ids.append(gui.c.create_text(x+self.box_width/2,y+self.box_height/2,text=fill_color,font=_font,fill="white"))
        
        self.visible = True
    
    def pick_color_at_point(self,point:gui.Point):
        for index,_ in enumerate(self.color_ids):
            x1 = self.start_x + (index%self.columns)*(self.box_width+self.margin)
            x2 = x1 + self.box_width
            y1 = self.start_y + (index//self.columns)*(self.box_height+self.margin)
            y2 = y1 + self.box_height

            bounding_box = (x1,y1,x2,y2)
            if point.inside(bounding_box):
                return index
        return None

    def darken_color(self,color):
        if len(self.color_ids) <= color or color < 0:
            raise IndexError(f"darken_color: Color index: {color}. Number of colors: {len(self.color_ids)}. Out of range.")
    
        self.clear_darkened_color()

        _id = self.color_ids[color]
        gui.c.itemconfig(_id,fill=imaging.rgb_to_hex(*imaging.red_shift(color,rgb=(255*config.get("highlight_darken_value"),0,0))),outline=config.get("highlight_color"))

        self.last_darkened_color = color

    def clear_darkened_color(self,color=None):
        if self.last_darkened_color is None:
            return
        if color is None:
            color = self.last_darkened_color
        gui.c.itemconfig(self.color_ids[color],fill=imaging.rgb_to_hex(*imaging.red_shift(color)),outline="black")

        self.last_darkened_color = None
    
    def reset_colors(self):
        for index,_id in enumerate(self.color_ids):
            fill_color = imaging.rgb_to_hex(*imaging.red_shift(index))
            if gui.c.itemcget(_id,"fill") != fill_color:
                gui.c.itemconfig(_id,fill=fill_color)
    
    def delete_colors(self):
        for _id in self.color_ids+self.text_ids+self.cover_id:
            gui.c.delete(_id)
        
        self.color_ids.clear()
        self.text_ids.clear()
        self.cover_id.clear()

        self.visible = False
        

class Deck:
    def __init__(self,colored_cards:list[int]=config.get("colored_cards"),wild_cards:list[int]=config.get("wild_cards"),duplicates:list[int]=config.get("duplicates"),num_colors:int=config.get("card_colors")):
        self.used_cards: list[card.Card] = []
        self.colored_cards: list[int] = colored_cards
        self.wild_cards: list[int] = wild_cards
        self.cards = self.colored_cards + self.wild_cards
        self.duplicates = duplicates
        self.num_colors = num_colors
        self.next_card: card.Card|None = None
        self.setup_next_card()

    def setup_next_card(self):
        next_card = self._select_card(fallback=False)

        x = config.get("deck_position")[0]*config.get("window_width")
        y = config.get("deck_position")[1]*config.get("window_height")
        self.next_card = card.Card(*next_card,hand=None)

        self.next_card.rescale(config.get("play_scale"))
        self.next_card.move_to(x, y)
        self.next_card.flip()

    def select_next_card(self) -> card.Card:
        next_card = self.next_card
        if not next_card.face_up:
            next_card.flip()
        self.add_used_card(self.next_card)
        self.setup_next_card()
        return next_card

    def _select_card(self, fallback=False) -> tuple[int, int]:
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
            color = -1
            return color, value  # Fallback on a wild card if all cards are used.
        value = random.choices(self.cards, weights, k=1)[0]

        if value in self.wild_cards:
            color = -1
            return color, value
        
        used_cards_of_value = [x for x in self.used_cards if x.value == value]
        possible_colors = [x for x in range(self.num_colors)] * self.duplicates[value]
        for c in used_cards_of_value:
            possible_colors.remove(c.color)
        color = random.choice(possible_colors)

        return color, value

    def add_used_card(self, _card: card.Card):
        self.used_cards.append(_card)
    
    def return_to_deck(self,_card:card.Card):
        if _card in self.used_cards:
            self.used_cards.remove(_card)

deck = Deck()

def mouse_motion(event):
    mouse.set_coords(event.x,event.y)

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

def evaluate_highlight(_card:card.Card):
    if mouse.clicked_this_frame and _card.hand == player_hand:
        if game.wild_card:
            if _card.value in config.get("colored_cards"):
                set_wild_color(_card=_card)
            if _card.value in config.get("wild_cards"):
                color_selection.render_colors()
            return

        if not game.validate(_card):
            return

        if _card.value in config.get("wild_cards"):
            game.wild_card_setup(_card)
            return
        
        game.play(_card)
        return
    
    if color_selection.visible and _card.hand == player_hand:
        if _card.value in config.get("colored_cards"):
            color_selection.darken_color(_card.color)


def set_wild_color(*,_card:Optional[card.Card]=None,color:Optional[int]=None):
    if (color is None) is (_card is None): # XNOR
        raise ValueError("set_wild_color: Exactly 1 of _card and color must be provided.")
    
    if _card is not None:
        _card.dehighlight()
    
    game.play(game.wild_card,color=color or _card.color)
    game.wild_card = None
    color_selection.delete_colors()

    for item in game.cover:
        gui.c.delete(item)
    game.cover.clear()


def game_loop(delta):
    for _card in player_hand.hand[::-1]:
        if mouse.inside(_card.bounding_box):
            check_for_highlight(_card)
        else:
            if _card.highlighted:
                _card.dehighlight()

    if color_selection.visible:
        color = color_selection.pick_color_at_point(mouse)
        if color is None:
            color_selection.clear_darkened_color()
        else:
            if mouse.clicked_this_frame:
                set_wild_color(color=color)
            else:

                color_selection.darken_color(color)
        

    for _card in card.Card.HIGHLIGHTS:
        evaluate_highlight(_card)
    
    if mouse.inside(deck.next_card.bounding_box) and mouse.clicked_this_frame:
        pickup_next_card()
    
    mouse.clicked_this_frame = False

    gui.window.after(FRAME_TIME,lambda: game_loop(FRAME_TIME))

def pickup_next_card():
    _card = deck.select_next_card()
    _card.add_to_hand(player_hand)
    _card.fix_image()
    player_hand.sort()

for _ in range(9):
    _card = deck.select_next_card()
    _card.add_to_hand(player_hand)
    _card.fix_image()

player_hand.sort()

start_card: card.Card = deck.select_next_card()
while start_card.value in config.get("wild_cards"):
    deck.return_to_deck(start_card)
    start_card = deck.select_next_card()

game = Game(start_card)

color_selection = ColorSelection(config.get("window_width"),config.get("window_height")*config.get("wild_selection_scale"))

gui.window.after(FRAME_TIME,lambda: game_loop(FRAME_TIME))

gui.window.bind("<Motion>",mouse_motion)
gui.window.bind("<Button>",mouse_click)
gui.window.bind("<ButtonRelease>",mouse_release)
