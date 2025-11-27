"""Song Controller."""
import os
from pygame import mixer
from customtkinter import CTkImage, CTkButton

mixer.init()

SONG_PATH = "./songs/"
DEFAULT_VOLUME = 0.5
MAX_VOLUME = 1.0


class Songs:
    """Manage songs, playback and state."""

    def _init_(self) -> None:
        self.current_playing = False
        self.current_song_index = 0
        self.playing = False
        self.songs = self._find_songs()
        self.current_song_name = ""

    # ----------------------- Song Loading ----------------------- #

    def _find_songs(self):
        """Return list of song file paths inside /songs/."""
        song_files = []
        for root, _, files in os.walk(SONG_PATH):
            for file in files:
                song_files.append(os.path.join(root, file))
        return song_files

    # ----------------------- Playback ----------------------- #

    def play_song(self):
        """Play or resume current song."""
        if not self.playing:
            current_song = self.songs[self.current_song_index]
            mixer.music.load(current_song)
            mixer.music.set_volume(DEFAULT_VOLUME)
            mixer.music.play()
            self.playing = True
        else:
            mixer.music.unpause()

    def pause_song(self):
        """Pause current song."""
        if self.playing:
            mixer.music.pause()

    def next_song(self):
        """Advance to next song."""
        self.current_song_index += 1
        if self.playing:
            mixer.music.unload()

    def previous_song(self):
        """Go to previous song."""
        self.playing = False
        self.current_song_index -= 1

        if self.current_song_index < 0:
            print("Reached first song")
            self.current_song_index = 0

    # ----------------------- UI Trigger ----------------------- #

    def button_action(self, button: CTkButton, play_image: CTkImage, pause_image: CTkImage):
        """Handle play/pause button click."""
        self.current_playing = not self.current_playing
        self.current_song_name = os.path.basename(self.songs[self.current_song_index]).split(".")[0]

        if self.current_playing:
            button.configure(image=pause_image)
            self.play_song()
        else:
            self.pause_song()
            button.configure(image=play_image)

    # ----------------------- Utility ----------------------- #

    def set_mixer_volume(self, value):
        """Set volume (slider value is 0–100)."""
        try:
            mixer.music.set_volume((value / 100) * MAX_VOLUME)
        except Exception:
            pass

    def stop_player(self):
        """Stop music and reset state."""
        self.current_playing = False
        mixer.music.stop()

    def reset_variables(self, csi=0, cp=False, p=False):
        """Reset playback variables."""
        self.current_song_index = csi
        self.current_playing = cp
        self.playing = p