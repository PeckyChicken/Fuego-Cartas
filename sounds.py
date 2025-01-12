from pygame import mixer

mixer.init()

def play_sound(sound:mixer.Sound):
    sound.play()

hover_sound = mixer.Sound("Assets/card_hover.wav")
