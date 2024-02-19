import customtkinter
from .music_controller import button_action
from PIL import Image
import time

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # --------------- App Setup --------------- #

        self.title("Music Player")
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

        image = customtkinter.CTkImage(dark_image=Image.open("./musics/a.png"),
                                       size=(250,250))
        self.song_image = customtkinter.CTkLabel(self,
                                                 text=None,
                                                 image=image)

        self.song_progressbar = customtkinter.CTkProgressBar(self,
                                                             orientation="horizontal",
                                                             progress_color=("white")
                                                             )
        
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
                                                         image=self.next_left_img)
        
        self.next_right_button = customtkinter.CTkButton(footer_frame,
                                                         hover="transparent",
                                                         fg_color="transparent",
                                                         width=40,
                                                         height=40,
                                                         text=None,
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
                                      command=self.get_value,
                                      number_of_steps=10)
        
        footer_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="nsew")
        footer_frame.grid_columnconfigure(0, weight=1)
        footer_frame.grid_columnconfigure(1, weight=1)
        footer_frame.grid_columnconfigure(2, weight=1)
        footer_frame.grid_columnconfigure(3, weight=1)
        footer_frame.grid_columnconfigure(4, weight=1)
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
        button_action(
            button=self.control_button,
            play_image=self.play_img,
            pause_image=self.pause_img)
  
    def get_value(self, value):
        '''
        Just get the value from the slider
        '''
        if value == self.slider.get():
            time.sleep(0.08)
            print(value)
