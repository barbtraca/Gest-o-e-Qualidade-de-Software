''' UI Scree and main functions '''
from threading import Thread
import time
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

        self.title("MP3 Player")
        self.geometry("510x425")
        self._set_appearance_mode("dark")
        self.minsize(width=510, height=425)
        self.maxsize(width=510, height=425)
        
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

        self.next_left_img = customtkinter.CTkImage(
            light_image=Image.open("./buttons/next_left.png"),
                dark_image=Image.open("./buttons/next_left.png"),
            size=(40, 40)
        )

        self.next_right_img = customtkinter.CTkImage(
            light_image=Image.open("./buttons/next_right.png"),
                dark_image=Image.open("./buttons/next_right.png"),
            size=(40, 40)
        )

        # Center

        image = customtkinter.CTkImage(dark_image=Image.open("./songs/a.png"),
                                       size=(250,250))
        self.song_image = customtkinter.CTkLabel(self,
                                                 text=None,
                                                 image=image)

        self.song_progressbar = customtkinter.CTkProgressBar(self,
                                                             orientation="horizontal",
                                                             progress_color=("white"),
                                                             )
        self.song_progressbar.set(0)

        self.song_image.grid(row=0, column=0, padx=30, pady=(30, 0), columnspan=2)
        self.song_progressbar.grid(row=1, column=0, padx=10, pady=20, columnspan=2)

        # --------------- Frame Objects --------------- #

        footer_frame = customtkinter.CTkFrame(self,
                                      corner_radius=0,
                                      width=720,
                                      height=130,
                                      border_color="#393939",
                                     )

        self.song_music = customtkinter.CTkLabel(footer_frame,
                                          text="Song Musisd asdsadas.",
                                          font=("Arial", 17),
                                          text_color="#000000",
                                          wraplength=155)
        self.next_left_button = customtkinter.CTkButton(footer_frame,
                                                         hover="transparent",
                                                         fg_color="transparent",
                                                         width=40,
                                                         height=40,
                                                         text=None,
                                                         command=self.l_button,
                                                         image=self.next_left_img)

        self.next_right_button = customtkinter.CTkButton(footer_frame,
                                                         hover="transparent",
                                                         fg_color="transparent",
                                                         width=40,
                                                         height=40,
                                                         text=None,
                                                         command=self.r_button,
                                                         image=self.next_right_img)

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
        footer_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="nsew")
        self.song_music.grid(row=0, column=0, padx=35, pady=10)
        self.next_left_button.grid(row=0, column=1, pady=10)
        self.control_button.grid(row=0, column=2, pady=10)
        self.next_right_button.grid(row=0, column=3, pady=10)
        self.slider.grid(row=0, column=4, padx=20, pady=10)

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
        self.start_stop_song_countdown()

    def set_volume(self, value):
        '''
            Set the song volume
        '''
        if song_control.song_lengh is not None:
            self.after(100, song_control.set_mixer_volume(value=value))
        else: print("a")

    def start_stop_song_countdown(self):
        '''
            Inicialize the countdown
        '''
        countdown_thread = Thread(target=self.run_countdown)
        countdown_thread.start()

    def run_countdown(self):
        '''
            Decay every 1 second the music lengh
            when is equal or under 0, the function goes
            to the next music or stop the track
        '''
        if song_control.song_lengh is None: 
            time.sleep(1)
            song_control.song_lengh = song_control.song_lengh
        while song_control.song_lengh > 0 and song_control.current_playing:
            time.sleep(1)
            song_control.song_lengh -= 1
            print(song_control.song_lengh)
        if song_control.song_lengh <= 0:
            try:
                print("oi")
                song_control.next_song()
                song_control.reset_variables(
                    csi=song_control.current_song_index,
                    sl =None)
                self.activate_button()
                song_control.set_mixer_volume(self.slider.get())
            except IndexError:
                print("oi EXCEPT")
                song_control.reset_variables(
                    csi= 0,
                    cp = True,
                    sl = None)
                song_control.button_action(
                                    button=self.control_button,
                                    play_image=self.play_img,
                                    pause_image=self.pause_img
                                    )
                print("You track list has completed!")

    def r_button(self):
        '''
            Goes to the next song of the track
        '''
        if song_control.next_song():
            print("a")
            song_control.song_lengh = None
            self.activate_button()
        else:
            self.start_stop_song_countdown()
            self.control_button.configure(image=self.play_img)
            song_control.stop_player()
            print("Reached last song, current playing the first one!")
            
        
    def l_button(self):
        '''
            Goes to the previous song of the track
        '''
        if song_control.previous_song():
            self.activate_button()
        else:
            if not song_control.current_playing:
                self.activate_button()
            else:
                song_control.play_song()

    def stop_player(self):
        '''
            Stop playing music
        '''
        if song_control.current_playing:
            song_control.stop_player()
        print("Window closed")
        self.destroy()
