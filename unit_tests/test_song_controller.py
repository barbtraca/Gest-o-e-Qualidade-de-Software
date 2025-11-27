import unittest
from unittest.mock import patch, MagicMock

from src.song_controller import Songs, MAX_VOLUME


class MockedButton:
    """Mock of the CTkButton class using MagicMock to track calls."""

    def __init__(self):
        # FIX: Using MagicMock for the 'configure' method makes it traceable
        self.configure = MagicMock()


class MockedImage:
    """Mock of the CTkImage class."""
    pass

# --------------------------------------------------------------------------------------
# All Test Execution
# --------------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()

# --------------------------------------------------------------------------------------
# UNIT TESTS FOR THE SONGS CLASS
# --------------------------------------------------------------------------------------

# Patch the Pygame mixer for simulation
@patch('src.song_controller.mixer')
class TestSongs(unittest.TestCase):

    # ----------------------- Initial Setup -----------------------

    # Mock the song discovery method
    @patch('src.song_controller.Songs._find_songs')
    def setUp(self, mock_find_songs):
        # Configure simulated songs
        self.mock_songs_list = [
            "/path/to/song1.mp3",
            "/path/to/song2.wav",
            "/path/to/song3.ogg"
        ]
        # Return the list of simulated songs
        mock_find_songs.return_value = self.mock_songs_list

        # Create the Songs class instance
        self.player = Songs()

        # Create mocks for UI objects
        self.mock_button = MockedButton()
        self.mock_play_img = MockedImage()
        self.mock_pause_img = MockedImage()

        # Ensure initial state is clean
        self.player.reset_variables(csi=0, cp=False, p=False)
        self.player.current_playing = False

        # Mock os.path.basename to test song name extraction
        patcher_basename = patch('os.path.basename', return_value='song1.mp3')
        self.mock_basename = patcher_basename.start()
        self.addCleanup(patcher_basename.stop)

    # ----------------------- Loading Tests -----------------------

    def test_initial_state(self, mock_mixer):
        """Verifies if the initial state and song loading are correct."""
        self.assertEqual(self.player.current_song_index, 0)
        self.assertFalse(self.player.current_playing)
        self.assertFalse(self.player.playing)
        self.assertEqual(len(self.player.songs), 3)

    # ----------------------- Playback Tests (Play/Pause) -----------------------

    def test_play_song_load_and_play(self, mock_mixer):
        """Tests if the song is loaded and started when not currently playing."""
        mock_mixer.music.get_busy.return_value = False
        self.player.play_song()

        # Should load song 1
        mock_mixer.music.load.assert_called_with(self.mock_songs_list[0])
        # Should play
        mock_mixer.music.play.assert_called_once()
        # Should update the internal state
        self.assertTrue(self.player.playing)

    def test_play_song_resume(self, mock_mixer):
        """Tests if the song is unpaused when already running."""
        mock_mixer.music.get_busy.return_value = True
        self.player.playing = True
        self.player.play_song()

        # Should not load or play (only unpause)
        mock_mixer.music.load.assert_not_called()
        mock_mixer.music.play.assert_not_called()
        # Should unpause
        mock_mixer.music.unpause.assert_called_once()

    def test_pause_song(self, mock_mixer):
        """Tests if the song is correctly paused."""
        self.player.playing = True
        self.player.pause_song()

        # Should call the pause function
        mock_mixer.music.pause.assert_called_once()

    # ----------------------- Navigation Tests -----------------------

    def test_next_song_advances_index(self, mock_mixer):
        """Tests if it correctly advances to the next index."""
        self.player.current_song_index = 0
        self.player.next_song()
        self.assertEqual(self.player.current_song_index, 1)

    def test_next_song_loop_to_start(self, mock_mixer):
        """Tests if it loops back to the start of the list after the last song."""
        self.player.current_song_index = 2  # Last index
        self.player.next_song()
        self.assertEqual(self.player.current_song_index, 0)

    def test_next_song_stops_mixer_if_playing(self, mock_mixer):
        """Tests if the mixer is stopped/unloaded when skipping track while playing."""
        self.player.playing = True
        self.player.next_song()
        mock_mixer.music.unload.assert_called_once()

    def test_previous_song_decrements_index(self, mock_mixer):
        """Tests if it correctly goes back to the previous index."""
        self.player.current_song_index = 2
        self.player.previous_song()
        self.assertEqual(self.player.current_song_index, 1)

    def test_previous_song_loop_to_end(self, mock_mixer):
        """Tests if it loops back to the end of the list after the first song."""
        self.player.current_song_index = 0
        self.player.previous_song()
        self.assertEqual(self.player.current_song_index, 2)

    def test_previous_song_stops_mixer_if_playing(self, mock_mixer):
        """Tests if the mixer is stopped when going back a track while playing."""
        self.player.playing = True
        self.player.previous_song()
        mock_mixer.music.stop.assert_called_once()

    # ----------------------- UI Logic Tests (button_action) -----------------------

    def test_button_action_normal_click_to_play(self, mock_mixer):
        """Tests if the button inverts to Play if it was Paused."""
        self.player.current_playing = False

        self.player.button_action(self.mock_button, self.mock_play_img, self.mock_pause_img, is_navigation=False)

        # Should change to Play
        self.assertTrue(self.player.current_playing)
        # Should change the icon to Pause
        self.mock_button.configure.assert_called_with(image=self.mock_pause_img)
        # Should attempt to play the song
        self.assertTrue(mock_mixer.music.play.called or mock_mixer.music.unpause.called)

    def test_button_action_normal_click_to_pause(self, mock_mixer):
        """Tests if the button inverts to Pause if it was Playing."""
        self.player.current_playing = True
        self.player.playing = True

        self.player.button_action(self.mock_button, self.mock_play_img, self.mock_pause_img, is_navigation=False)

        # Should change to Pause
        self.assertFalse(self.player.current_playing)
        # Should change the icon to Play
        self.mock_button.configure.assert_called_with(image=self.mock_play_img)
        # Should pause the music
        mock_mixer.music.pause.assert_called_once()

    def test_button_action_navigation_forces_play(self, mock_mixer):
        """Tests if navigation forces the 'Play' state (current_playing=True) and loads the song."""
        self.player.current_playing = False

        # FIX APPLIED: Force the mixer to be "not busy" so play_song calls load()
        mock_mixer.music.get_busy.return_value = False

        self.player.button_action(self.mock_button, self.mock_play_img, self.mock_pause_img, is_navigation=True)

        # Should force Play, regardless of previous state
        self.assertTrue(self.player.current_playing)
        # Should change the icon to Pause
        self.mock_button.configure.assert_called_with(image=self.mock_pause_img)
        # Should load the new song, as get_busy() returned False
        self.assertTrue(mock_mixer.music.load.called)

    # ----------------------- Utility Tests -----------------------

    def test_set_mixer_volume(self, mock_mixer):
        """Tests if the volume is set correctly (slider value 0-100 to 0.0-1.0)."""

        self.player.set_mixer_volume(50)
        mock_mixer.music.set_volume.assert_called_with(0.5 * MAX_VOLUME)

        self.player.set_mixer_volume(100)
        mock_mixer.music.set_volume.assert_called_with(1.0 * MAX_VOLUME)

        self.player.set_mixer_volume(0)
        mock_mixer.music.set_volume.assert_called_with(0.0 * MAX_VOLUME)

    def test_stop_player(self, mock_mixer):
        """Tests if the player stops and resets all states."""
        self.player.current_playing = True
        self.player.playing = True

        self.player.stop_player()

        mock_mixer.music.stop.assert_called_once()
        self.assertFalse(self.player.current_playing)
        self.assertFalse(self.player.playing)

    def test_reset_variables(self, mock_mixer):
        """Tests if the variables are reset correctly."""
        self.player.current_song_index = 5
        self.player.current_playing = True
        self.player.playing = True

        self.player.reset_variables()

        self.assertEqual(self.player.current_song_index, 0)
        self.assertFalse(self.player.current_playing)
        self.assertFalse(self.player.playing)