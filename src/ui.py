import customtkinter
from .music_controller import button_action
from PIL import Image

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # --------------- App Setup --------------- #

        self.title("Music Player")
        self.geometry("720x480")
        self._set_appearance_mode("dark")
        self.minsize(width=720, height=480) 
        self.maxsize(width=720, height=480)

        # --------------- Photos --------------- #

        self.play_image = customtkinter.CTkImage(
            light_image=Image.open("./buttons/play.png"),
            dark_image=Image.open("./buttons/play.png"),
            size=(60, 60)
        )
        self.pause_image = customtkinter.CTkImage(
                light_image=Image.open("./buttons/pause.png"),
                dark_image=Image.open("./buttons/pause.png"),
                size=(60, 60)
        )
        # --------------- Frame Objects --------------- #

        footer_frame = customtkinter.CTkFrame(self, 
                                                   corner_radius=0, 
                                                   height=130,
                                                   border_color="#393939",
                                                #    fg_color="#000000"
                                                )
        footer_frame.grid(row=3, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)

        self.song_music = customtkinter.CTkLabel(footer_frame, 
                                                 text="Song Music.",
                                                 font=("Arial", 19),
                                                 text_color="#000000")
        self.song_music.grid(row=0, column=0, padx=10, pady=10)

        self.control_button = customtkinter.CTkButton(footer_frame,
                                                      hover="transparent",
                                                      fg_color="transparent",
                                                      width=60,
                                                      height=60,
                                                      text=None,
                                                      command=self.activate_button,
                                                      image=self.play_image)
                                                      
        self.control_button.grid(row=0, column=1, padx=10, pady=10)
        # self.song_progressbar = customtkinter.CTkProgressBar(footer_frame,
        #                                                      orientation="horizontal",
        #                                                      progress_color=("white")
        #                                                      )
        # self.song_progressbar.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

    def activate_button(self):
        button_action(
            button=self.control_button, 
            play_image=self.play_image, 
            pause_image=self.pause_image)
        


