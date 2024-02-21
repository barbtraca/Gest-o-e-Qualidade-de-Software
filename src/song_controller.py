''' Song Controller '''
import os
from pygame import mixer
from customtkinter import CTkImage, CTkButton

mixer.init()

SONG_PATH = "././songs/"
DEFAULT_VOLUME = 0.5
MAX_VOLUME = 1

class Songs():
    '''
        Songs class
    '''
    def __init__(self) -> None:
        self.current_playing = False
        self.current_song_index = 0
        self.song_lengh = None
        self.songs = self.find_mp3()
        print(self.songs)
  
    def find_mp3(self):
        '''
            Find all the mp3 files from the /songs/ folder
            and append it into the mp3_files list
        '''
        mp3_files = []
        for root, _, files in os.walk(SONG_PATH):
            for file in files:
                if file.endswith(".mp3"):
                    mp3_files.append(root + file)
        return mp3_files

    def play_song(self):
        '''
            Play the current song
        '''
        if self.song_lengh is None:
            mixer.music.load(self.songs[self.current_song_index])
            mixer.music.set_volume(DEFAULT_VOLUME)
            self.song_lengh = mixer.Sound(file=self.songs[self.current_song_index]).get_length()
            self.song_lengh = 5
            print("TOCANDO MUSICA")
            mixer.music.play()
        else: mixer.music.unpause()

    def pause_song(self):
        '''
            Pause the current song
        '''
        mixer.music.pause()

    def next_song(self):
        '''
            Play the next song of the track
        '''
        self.current_song_index += 1
        if self.song_lengh is not None:
            mixer.music.unload()

    def previous_song(self):
        '''
            Play the previous song of the track
        '''
        try:
            mixer.mixer_music.unload()
        except AttributeError:
            pass
        self.current_song_index -= 1
        self.song_lengh = None
        if self.current_song_index < 0:
            print("Reached first song")
            self.current_song_index = 0
            self.current_playing = not self.current_playing
            return True
        return False

    def button_action(self,
                      button = CTkButton,
                      play_image = CTkImage,
                      pause_image = CTkImage) -> None:
        '''
            A button trigger to start a song or pause it
            including the chage of the button img
        '''
        try:
            print(self.songs[self.current_song_index])
        except: pass
        self.current_playing = not self.current_playing
        if self.current_playing:
            button.configure(image=pause_image)
            self.play_song()
        else:
            self.pause_song()
            button.configure(image=play_image)

    def set_mixer_volume(self, value):
        '''
            Set the song volume as the value from the slider
        '''
        try:
            mixer.music.set_volume(MAX_VOLUME * (value / 100))
        except AttributeError:
            pass

    def stop_player(self):
        '''
            Just stop the music to don't have any bugs
        '''
        self.current_playing = not self.current_playing
        mixer.music.stop()
    
    def reset_variables(self, csi = 0, cp = False, sl = None):
        '''
            Reset variables
        '''
        self.current_song_index = csi
        self.current_playing = cp
        self.song_lengh = sl
