from pygame import mixer
import os
import time
from customtkinter import CTkImage, CTkButton
mixer.init()

MUSICS_PATH = "././musics/"
DEFAULT_VOLUME = 0.5
MAX_VOLUME = 1

class Musics():
    def __init__(self) -> None:
        self.current_playing = False
        self.current_song_index = 0
        self.song_lengh = None
        self.musics = self.find_mp3()
        print(self.musics)
    
    def find_mp3(self):
        mp3_files = []
        for root, _, files in os.walk(MUSICS_PATH):
            for file in files:
                if file.endswith(".mp3"):
                    mp3_files.append(root + file)
        return mp3_files
     

    def play_music(self):
        mixer.music.load(self.musics[self.current_song_index])
        mixer.music.set_volume(DEFAULT_VOLUME)
        if self.song_lengh is None:
            self.song_lengh = mixer.Sound(file=self.musics[self.current_song_index]).get_length()
        mixer.music.play()

    def pause_music(self):
        mixer.music.pause()

    def button_action(self,
                      button = CTkButton,
                      play_image = CTkImage,
                      pause_image = CTkImage) -> None:
        
        self.current_playing = not self.current_playing
        if self.current_playing:
            button.configure(image=pause_image)
            self.play_music()
        else:
            self.pause_music()
            button.configure(image=play_image)

    def set_mixer_volume(self, value):
        try:
            mixer.music.set_volume(MAX_VOLUME * (value / 100))
        except AttributeError:
            pass


