"""Handles custom music/sound being played."""

import pygame
from ..io.logging import play_logger as logger


class Sound:
    def __init__(self, file_name, volume=1.0, loops=1):
        """
        Initialize the Sound object.
        :param file_name: The sound file to load.
        :param volume: The initial volume (0.0 to 1.0).
        :param loops: Number of times to loop the sound (-1 for infinite).
        """
        pygame.mixer.init()
        self.sound = None
        self.channel = None
        self.file_path = file_name
        self.volume = volume
        self.loops = loops
        self.is_paused = False
        self.load(file_name)
        self.set_volume(volume)

    def load(self, file_name):
        """Load a sound file."""
        try:
            self.sound = pygame.mixer.Sound(file_name)

        except FileNotFoundError:
            logger.error("File not found", exc_info=True)
        logger.info("Loaded sound file", exc_info=True)

    def play(self):
        """Play the loaded sound with the specified loop settings, or resume a paused sound."""
        if not self.sound:
            logger.warning(
                "No sound loaded. Use the 'load' method first.", exc_info=True
            )

        self.channel = pygame.mixer.find_channel()
        if self.channel is None:
            logger.warning("No available channels to play the sound.", exc_info=True)

        if not self.is_playing():
            self.channel.play(self.sound, loops=self.loops)
        if self.is_paused:
            self.channel.unpause()
            self.is_paused = False

    def pause(self):
        """Pause the sound."""
        if self.channel.get_busy():
            self.channel.pause()
            self.is_paused = True

    def length_song(self):
        """Returns the length of the song as a float"""

        return round((self.channel.get_sound().get_length()), 2)

    def stop(self):
        """Stop current channel"""
        self.channel.stop()

    def set_volume(self, volume):
        """Set the volume of the sound (0.0 to 1.0)."""
        if not self.sound:
            logger.warning(
                "No sound loaded. Use the 'load' method first.", exc_info=True
            )
        if not 0.0 <= volume <= 1.0:
            logger.warning("Volume must be between 0.0 and 1.0", exc_info=True)
        self.volume = volume
        self.sound.set_volume(volume)

    def get_volume(self):
        """Get the current volume of the sound."""
        if not self.sound:
            logger.warning(
                "No sound loaded. Use the 'load' method first.", exc_info=True
            )
        volume = self.sound.get_volume()
        return volume

    def is_playing(self):
        """Check if the sound is currently playing."""
        if self.channel:
            return self.channel.get_busy()
        return False
