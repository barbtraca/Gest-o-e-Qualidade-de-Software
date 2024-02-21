''' UI Scree and main functions '''
from threading import Thread
import customtkinter
from PIL import Image
from src.song_controller import Songs

song_control = Songs()
class App(customtkinter.CTk):
    '''
        Screen Class
    '''
    def __init__(self):
        super().__init__()

        # --------------- App Setup --------------- #

        self.title("Music Player")
        self.geometry("510x415")
        self._set_appearance_mode("dark")
        self.minsize(width=510, height=415)
        self.maxsize(width=510, height=415)

        # --------------- Photos --------------- #

        self.play_img = customtkinter.CTkImage(
            light_image=Image.open("./buttons/play.png"),
            dark_image=Image.open("./buttons/play.png"),
            size=(60, 60)
        )
        self.pause_img = customtkinter.CTkImage(
                light_image=Image.open("./buttons/pause.png"),
                dark_image=Image.open("./buttons/pause.png"),
                size=(60, 60)
        )

        self.previous_song_button = customtkinter.CTkImage(
            light_image=Image.open("./buttons/next_left.png"),
                dark_image=Image.open("./buttons/next_left.png"),
            size=(40, 40)
        )

        self.next_song_button = customtkinter.CTkImage(
            light_image=Image.open("./buttons/next_right.png"),
                dark_image=Image.open("./buttons/next_right.png"),
            size=(40, 40)
        )

        # Center

        image = customtkinter.CTkImage(dark_image=Image.open("././main_img.jpg"),
                                       size=(250,250))
        self.song_image = customtkinter.CTkLabel(self,
                                                 text=None,
                                                 image=image)

        self.song_progressbar = customtkinter.CTkProgressBar(self,
                                                             orientation="horizontal",
                                                             progress_color=("cyan"),
                                                             )
        self.song_progressbar.set(0)

        self.song_image.grid(row=0, column=0, padx=30, pady=(30, 0), sticky="nsew")
        self.song_progressbar.grid(row=1, column=0, padx=10, pady=20, sticky="ns")

        # --------------- Frame Objects --------------- #

        footer_frame = customtkinter.CTkFrame(self,
                                      corner_radius=0,
                                      width=720,
                                      height=130,
                                      border_color="#393939",
                                     )

        self.song_label = customtkinter.CTkLabel(footer_frame,
                                          text="Play to Start",
                                          font=("Arial", 19),
                                          width=130,
                                          height=50,
                                          text_color="#000000",
                                          wraplength=160)
        self.previous_song_button = customtkinter.CTkButton(footer_frame,
                                                         hover="transparent",
                                                         fg_color="transparent",
                                                         width=40,
                                                         height=40,
                                                         text=None,
                                                         command=self.l_button,
                                                         image=self.previous_song_button)

        self.next_song_button = customtkinter.CTkButton(footer_frame,
                                                         hover="transparent",
                                                         fg_color="transparent",
                                                         width=40,
                                                         height=40,
                                                         text=None,
                                                         command=self.r_button,
                                                         image=self.next_song_button)

        self.control_button = customtkinter.CTkButton(footer_frame,
                                               hover="transparent",
                                               fg_color="transparent",
                                               width=25,
                                               height=55,
                                               text=None,
                                               command=self.activate_button,
                                               image=self.play_img
                                            )

        self.slider = customtkinter.CTkSlider(footer_frame,
                                      from_=0, to=100,
                                      width=120,
                                      command=self.set_volume,
                                      number_of_steps=10)
        footer_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.song_label.grid(row=0, column=0, pady=6, padx=(10, 0), sticky="w")
        self.previous_song_button.grid(row=0, column=1, pady=6, padx=(4, 0))
        self.control_button.grid(row=0, column=2, pady=10)
        self.next_song_button.grid(row=0, column=3, pady=6, padx=(0, 20))
        self.slider.grid(row=0, column=4, pady=6)

        self.columnconfigure(0, weight=1)
        footer_frame.columnconfigure(0, weight=0, minsize=160)

    # Functions

    def activate_button(self):
        ''' 
            Activate the play/pause button, calling the button_action
            function
        '''
        song_control.button_action(
            button=self.control_button,
            play_image=self.play_img,
            pause_image=self.pause_img)
        
        song_control.set_mixer_volume(self.slider.get())
        self.song_label.configure(text=f"Playing:\n{song_control.current_song_name}")

    def set_volume(self, value):
        '''
            Set the song volume
        '''
        if song_control.song_lengh is not None:
            self.after(100, song_control.set_mixer_volume(value=value))
        else: pass

    def completed_track(self):
        '''
            Message the user when the track list has completed
        '''
        song_control.reset_variables(
            csi= 0,
            cp = True,
            sl = None)
        song_control.button_action(
                            button=self.control_button,
                            play_image=self.play_img,
                            pause_image=self.pause_img
                            )
        self.song_label.configure(text=f"Playing:\n{song_control.current_song_name}")
        print("You track list has completed!")

    def r_button(self):
        '''
            Goes to the next song of the track
        '''
        if song_control.current_playing:
            song_control.reset_variables(
                csi=song_control.current_song_index,
                cp =song_control.current_playing)
            self.activate_button()
        song_control.next_song()
        song_control.reset_variables(csi=song_control.current_song_index)
        try:
            self.activate_button()
        except IndexError:
            self.completed_track()

    def l_button(self):
        '''
            Goes to the previous song of the track
        '''
        if song_control.current_playing:
            self.activate_button()
        song_control.previous_song()
        self.activate_button()

    def stop_player(self):
        '''
            Stop playing music
        '''
        if song_control.current_playing:
            song_control.stop_player()
        print("Window closed")
        self.destroy()
