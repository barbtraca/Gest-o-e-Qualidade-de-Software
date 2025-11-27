import unittest
from unittest.mock import patch, MagicMock

# Import the App class and the global song_control instance
from src.ui import App, song_control
import customtkinter


# --- Mocks ---
class MockedButton:
    """Mock of the CTkButton class using MagicMock to track calls."""

    def __init__(self):
        self.configure = MagicMock()


class MockedImage:
    """Mock of the CTkImage class."""
    pass


MockedWidget = MagicMock()  # Used for CTkLabel, CTkProgressBar, CTkFrame


# --------------------------------------------------------------------------------------
# UNIT TESTS FOR THE UI CLASS (App)
# --------------------------------------------------------------------------------------

# DECORADORES DE CLASSE: Os mocks serão injetados no setUp.
@patch('src.ui.App.__init__', return_value=None)
@patch('src.ui.customtkinter.CTkImage', new=MockedImage)
@patch('src.ui.Image.open')
class TestAppFunctions(unittest.TestCase):

    # ----------------------- Initial Setup -----------------------

    # Usar *args para capturar os 3 mocks injetados pelos decoradores de classe.
    # Isso evita o TypeError.
    def setUp(self, *args):  # <--- CORREÇÃO CRÍTICA AQUI

        # Patching all critical CTk widget constructors that fail the Tcl initialization
        patcher_label = patch('src.ui.customtkinter.CTkLabel', new=MockedWidget)
        patcher_button = patch('src.ui.customtkinter.CTkButton', new=MockedWidget)
        patcher_progressbar = patch('src.ui.customtkinter.CTkProgressBar', new=MockedWidget)
        patcher_frame = patch('src.ui.customtkinter.CTkFrame', new=MockedWidget)
        patcher_slider = patch('src.ui.customtkinter.CTkSlider', new=MockedWidget)

        # Start all patches applied to the constructors
        self.mock_label = patcher_label.start()
        self.mock_button_widget = patcher_button.start()
        self.mock_progressbar = patcher_progressbar.start()
        self.mock_frame = patcher_frame.start()
        self.mock_slider_widget = patcher_slider.start()

        # Ensure they are stopped after the test
        self.addCleanup(patcher_label.stop)
        self.addCleanup(patcher_button.stop)
        self.addCleanup(patcher_progressbar.stop)
        self.addCleanup(patcher_frame.stop)
        self.addCleanup(patcher_slider.stop)

        # 1. Initialize the App instance
        self.app = App()

        # 2. Manually configure the essential UI attributes
        self.app.control_button = MockedButton()
        self.app.song_label = MagicMock(spec=['configure'])
        self.app.song_progressbar = MagicMock(spec=['configure', 'start', 'get'])

        # Mocks for images
        self.app.play_img = MockedImage()
        self.app.pause_img = MockedImage()

        # Mock for the volume slider
        self.app.slider = MagicMock(spec=['get'])
        self.app.slider.get.return_value = 50.0

        # 3. Patch the global song_control instance
        self.mock_song_control = MagicMock(spec=song_control)
        patcher_control = patch('src.ui.song_control', new=self.mock_song_control)
        patcher_control.start()
        self.addCleanup(patcher_control.stop)

        # Define a default state for the controller
        self.mock_song_control.current_song_name = "Test Song 1"
        self.mock_song_control.songs = ["path1", "path2"]
        self.mock_song_control.playing = True

    # ----------------------- Playback Tests (toggle_play) -----------------------

    def test_toggle_play_calls_controller_and_updates_label(self, *args):
        """Tests if toggle_play calls the controller's button_action and updates the song label."""
        self.app.toggle_play()
        self.mock_song_control.button_action.assert_called_once_with(
            button=self.app.control_button,
            play_image=self.app.play_img,
            pause_image=self.app.pause_img
        )
        self.mock_song_control.set_mixer_volume.assert_called_with(50.0)
        expected_text = f"Playing:\n{self.mock_song_control.current_song_name}"
        self.app.song_label.configure.assert_called_with(text=expected_text)

    def test_toggle_play_updates_progressbar_speed_when_starting(self, *args):
        """Tests if progress bar speed is configured when the song is starting (not playing)."""
        self.mock_song_control.playing = False
        self.app.toggle_play()
        self.app.song_progressbar.configure.assert_called()

    def test_toggle_play_handles_no_songs(self, *args):
        """Tests if toggle_play returns early if the song list is empty."""
        self.mock_song_control.songs = []
        self.app.toggle_play()
        self.mock_song_control.button_action.assert_not_called()
        self.app.song_label.configure.assert_not_called()

    # ----------------------- Navigation Tests -----------------------

    def test_handle_next_song(self, *args):
        """Tests if handle_next_song navigates, forces play, and updates the label."""
        self.app.handle_next_song()
        self.mock_song_control.next_song.assert_called_once()
        self.mock_song_control.button_action.assert_called_once_with(
            button=self.app.control_button,
            play_image=self.app.play_img,
            pause_image=self.app.pause_img,
            is_navigation=True
        )
        expected_text = f"Playing:\n{self.mock_song_control.current_song_name}"
        self.app.song_label.configure.assert_called_with(text=expected_text)

    def test_handle_previous_song(self, *args):
        """Tests if handle_previous_song navigates, forces play, and updates the label."""
        self.app.handle_previous_song()
        self.mock_song_control.previous_song.assert_called_once()
        self.mock_song_control.button_action.assert_called_once_with(
            button=self.app.control_button,
            play_image=self.app.play_img,
            pause_image=self.app.pause_img,
            is_navigation=True
        )
        expected_text = f"Playing:\n{self.mock_song_control.current_song_name}"
        self.app.song_label.configure.assert_called_with(text=expected_text)

    # ----------------------- Utility Tests -----------------------

    def test_set_volume(self, *args):
        """Tests if set_volume calls the controller's set_mixer_volume."""
        test_volume = 75.0
        self.app.set_volume(test_volume)
        self.mock_song_control.set_mixer_volume.assert_called_once_with(test_volume)

    def test_handle_track_end(self, *args):
        """Tests handling when the tracklist is completed."""
        self.app.handle_track_end()
        self.mock_song_control.reset_variables.assert_called_once_with(csi=0, cp=True)
        self.mock_song_control.button_action.assert_called_once()
        self.app.song_label.configure.assert_called_with(text="Tracklist completed!")

    def test_stop_player_calls_stop_if_playing(self, *args):
        """Tests if stop_player calls the controller stop_player method when current_playing is True."""
        self.mock_song_control.current_playing = True
        with patch.object(self.app, 'destroy') as mock_destroy:
            self.app.stop_player()
            self.mock_song_control.stop_player.assert_called_once()
            mock_destroy.assert_called_once()

    def test_stop_player_does_not_call_stop_if_not_playing(self, *args):
        """Tests if stop_player does NOT call the controller stop_player method when current_playing is False."""
        self.mock_song_control.current_playing = False
        with patch.object(self.app, 'destroy') as mock_destroy:
            self.app.stop_player()
            self.mock_song_control.stop_player.assert_not_called()
            mock_destroy.assert_called_once()


# --------------------------------------------------------------------------------------
# All Test Execution
# --------------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()