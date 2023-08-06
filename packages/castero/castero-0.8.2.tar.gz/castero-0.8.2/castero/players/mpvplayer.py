import time

from castero.config import Config
from castero.player import Player, PlayerDependencyError


class MPVPlayer(Player):
    """Interface for the mpv media player.
    """
    NAME = "mpv"

    def __init__(self, title, path, episode) -> None:
        """
        Overrides method from Player; see documentation in that class.
        """
        super().__init__(title, path, episode)

        import mpv
        self.mpv = mpv

    @staticmethod
    def check_dependencies():
        """Checks whether dependencies are met for playing a player.

        Overrides method from Player; see documentation in that class.
        """
        try:
            import mpv
            mpv.MPV()
        except (ImportError, NameError, OSError, AttributeError):
            raise PlayerDependencyError(
                "Dependency mpv not found, which is required for playing"
                " media files"
            )

    def _create_player(self) -> None:
        """Creates the player object while making sure it is a valid file.

        Overrides method from Player; see documentation in that class.
        """
        self._player = self.mpv.MPV()
        self._player.vid = False
        self._player.pause = False

        self._player.play(self._path)

        self._duration = 5

    def play(self) -> None:
        """Plays the media.

        Overrides method from Player; see documentation in that class.
        """
        if self._player is None:
            self._create_player()

        self._player.pause = False
        self._state = 1

    def stop(self) -> None:
        """Stops the media.

        Overrides method from Player; see documentation in that class.
        """
        if self._player is not None:
            self._player.terminate()
            self._state = 0

    def pause(self) -> None:
        """Pauses the media.

        Overrides method from Player; see documentation in that class.
        """
        if self._player is not None:
            self._player.pause = True
            self._state = 2

    def seek(self, direction, amount) -> None:
        """Seek forward or backward in the media.

        Overrides method from Player; see documentation in that class.
        """
        assert direction == 1 or direction == -1
        if self._player is not None:
            self._player.seek(direction * amount)

    def change_rate(self, direction, display=None) -> None:
        """Increase or decrease the playback speed.

        Overrides method from Player; see documentation in that class.
        """
        assert direction == 1 or direction == -1
        if self._player is not None:
            new_rate = self._player.speed + 0.1 * direction
            self._player.speed = new_rate
            if display:
                display.change_status(
                    "Playback speed set to {:0.2f}".format(new_rate))

    def set_rate(self, rate) -> None:
        """Set the playback speed.

        Overrides method from Player; see documentation in that class.
        """
        if self._player is not None:
            self._player.speed = rate

    def set_volume(self, volume) -> None:
        """Set the player volume.

        Overrides method from Player; see documentation in that class.
        """
        if self._player is not None:
            self._player.volume = volume

    @property
    def duration(self) -> int:
        """int: the duration of the player"""
        result = 0
        if self._player is not None:
            d = self._player.duration
            result = 5000 if d is None else d * 1000
        return result

    @property
    def volume(self) -> int:
        """int: the volume of the player"""
        if self._player is not None:
            return self._player.volume

    @property
    def time(self) -> int:
        """int: the current time of the player"""
        if self._player is not None:
            t = self._player.time_pos
            return 0 if t is None else t * 1000

    @property
    def time_str(self) -> str:
        """str: the formatted time and duration of the player"""
        result = "00:00:00/00:00:00"
        if self._player is not None:
            time_seconds = int(self.time / 1000)
            length_seconds = int(self.duration / 1000)
            t = time.strftime('%H:%M:%S', time.gmtime(time_seconds))
            d = time.strftime('%H:%M:%S', time.gmtime(length_seconds))
            result = "%s/%s" % (t, d)
        return result
