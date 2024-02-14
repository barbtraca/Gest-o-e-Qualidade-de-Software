from pygame import mixer
from customtkinter import CTkImage, CTkButton
mixer.init()

current_playing = False



def button_action(button = CTkButton, play_image = CTkImage, pause_image = CTkImage) -> None:
    print(button)
    global current_playing
    
    if current_playing:
        button.configure(image=pause_image)
        print(pause_image)
    else:
        button.configure(image=play_image)

    current_playing = not current_playing

