"""UI Screen and main functions."""
import random

import customtkinter
from PIL import Image

from src.song_controller import Songs

song_control = Songs()


class App(customtkinter.CTk):
    """Main application window."""

    def __init__(self):
        super().__init__()

        # -------------------- App Setup -------------------- #

        self.title("Music Player")
        self.geometry("510x415")
        self._set_appearance_mode("dark")
        self.minsize(width=510, height=415)
        self.maxsize(width=510, height=415)

        # -------------------- Load Images -------------------- #

        """ Play Button"""
        self.play_img = customtkinter.CTkImage(
            light_image=Image.open("./buttons/play.png"),
            dark_image=Image.open("./buttons/play.png"),
            size=(60, 60)
        )

        """Pause Button"""
        self.pause_img = customtkinter.CTkImage(
            light_image=Image.open("./buttons/pause.png"),
            dark_image=Image.open("./buttons/pause.png"),
            size=(60, 60)
        )

        """ Previous Button"""
        self.prev_img = customtkinter.CTkImage(
            light_image=Image.open("./buttons/next_left.png"),
            dark_image=Image.open("./buttons/next_left.png"),
            size=(40, 40)
        )

        """ Next Button"""
        self.next_img = customtkinter.CTkImage(
            light_image=Image.open("./buttons/next_right.png"),
            dark_image=Image.open("./buttons/next_right.png"),
            size=(40, 40)
        )

        # -------------------- Main Image -------------------- #

        image = customtkinter.CTkImage(
            dark_image=Image.open("./main_img.jpg"),
            size=(250, 250)
        )

        self.song_image = customtkinter.CTkLabel(self, text=None, image=image)
        self.song_image.grid(row=0, column=0, padx=30, pady=(30, 0), sticky="nsew")

        self.song_progressbar = customtkinter.CTkProgressBar(
            self,
            orientation="horizontal",
            progress_color="cyan",
            mode="indeterminate"
        )
        self.song_progressbar.grid(row=1, column=0, padx=10, pady=20, sticky="ns")
        self.song_progressbar.set(0)
        self.song_progressbar.start()

        # -------------------- Footer Frame -------------------- #

        footer_frame = customtkinter.CTkFrame(
            self,
            corner_radius=0,
            width=720,
            height=130,
            fg_color="#363636"
        )
        footer_frame.grid(row=2, column=0, sticky="nsew")

        """ Song label"""
        self.song_label = customtkinter.CTkLabel(
            footer_frame,
            text="Play to Start",
            font=("Arial", 17),
            width=130,
            height=50,
            text_color="#3ADBE5",
            wraplength=160,
        )
        self.song_label.grid(row=0, column=0, pady=6, padx=(10, 0), sticky="w")

        """Previous / Play / Next buttons"""
        self.previous_song_button = customtkinter.CTkButton(
            footer_frame,
            fg_color="transparent",
            width=40,
            height=40,
            text=None,
            image=self.prev_img,
            command=self.handle_previous_song
        )
        self.previous_song_button.grid(row=0, column=1, padx=4)

        """Control button"""
        self.control_button = customtkinter.CTkButton(
            footer_frame,
            fg_color="transparent",
            width=25,
            height=55,
            text=None,
            image=self.play_img,
            command=self.toggle_play
        )
        self.control_button.grid(row=0, column=2)

        """Next button"""
        self.next_song_button = customtkinter.CTkButton(
            footer_frame,
            fg_color="transparent",
            width=40,
            height=40,
            text=None,
            image=self.next_img,
            command=self.handle_next_song
        )
        self.next_song_button.grid(row=0, column=3, padx=(0, 20))

        """ Volume slider"""
        self.slider = customtkinter.CTkSlider(
            footer_frame,
            from_=0, to=100,
            width=120,
            command=self.set_volume,
            number_of_steps=50,
            progress_color="#5D4DD1",
            button_color="cyan",
            button_hover_color="dark cyan"
        )
        self.slider.grid(row=0, column=4, pady=6)

        # ---------------- Layout ---------------- #

        self.columnconfigure(0, weight=1)
        footer_frame.columnconfigure(0, weight=0, minsize=155)

    # ============================================================
    # Functions
    # ============================================================

    def toggle_play(self):
        """Toggle play/pause and update UI."""

        if not song_control.songs:
            print("Não é possível tocar: sem músicas.")
            return

        if not song_control.playing:
            speed = 1.0 / random.randint(2, 4)
            self.song_progressbar.configure(indeterminate_speed=speed)

        song_control.button_action(
            button=self.control_button,
            play_image=self.play_img,
            pause_image=self.pause_img
        )

        song_control.set_mixer_volume(self.slider.get())

        self.song_label.configure(text=f"Playing:\n{song_control.current_song_name}")

    def set_volume(self, value):
        """Set mixer volume only if a song is playing."""
        song_control.set_mixer_volume(value)

    def handle_next_song(self):
        """Advance to next song."""
        song_control.next_song()

        """ Forces the 'Play' state and starts playback"""
        song_control.button_action(
            button=self.control_button,
            play_image=self.play_img,
            pause_image=self.pause_img,
            is_navigation=True
        )

        self.song_label.configure(text=f"Playing:\n{song_control.current_song_name}")

    def handle_previous_song(self):
        """Go to previous song."""
        song_control.previous_song()

        """ Forces the 'Play' state and starts playback"""
        song_control.button_action(
            button=self.control_button,
            play_image=self.play_img,
            pause_image=self.pause_img,
            is_navigation=True
        )

        self.song_label.configure(text=f"Playing:\n{song_control.current_song_name}")

    def handle_track_end(self):
        """Handle end of playlist."""
        song_control.reset_variables(csi=0, cp=True)
        song_control.button_action(
            button=self.control_button,
            play_image=self.play_img,
            pause_image=self.pause_img,
        )
        self.song_label.configure(text="Tracklist completed!")

    def stop_player(self):
        """Stop playback when closing window."""
        if song_control.current_playing:
            song_control.stop_player()
        print("Window closed")
        self.destroy()
