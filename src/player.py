import shout
import time
import sys


class RadioConnectionException(Exception):
    pass


class RadioPlayer():
    def __init__(self, host="localhost", port=8501, user='source', password='hackme', mount='/mymout'):
        self._s = shout.Shout()
        self._s.host = host
        self._s.port = port
        self._s.user = user
        self._s.password = password
        self._s.mount = mount
        self._status = shout.SHOUTERR_UNCONNECTED

    @staticmethod
    def format_songname(song):
        result = song.split("/")[-1].split(".")
        result = ".".join(result[:len(result) - 1]).replace("_", " ").replace("-", " - ")
        return result

    def open_player(self):
        if self._status != shout.SHOUTERR_CONNECTED:
            self._status = self._s.open()
            if self._status != shout.SHOUTERR_CONNECTED:
                raise RadioConnectionException("Unable to connect to server: %d", self._status)

    def close_player(self):
        if self._status == shout.SHOUTERR_CONNECTED:
            self._s.close()

    def play_track(self, song_name="", song_file=""):
        self._s.format = 'mp3'
        # self._s.protocol = 'http' | 'xaudiocast' | 'icy'
        self._s.name = 'Deep South Sounds'
        # self._s.genre = 'Deep House'
        # self._s.url = 'http://www.deepsouthsounds.com/'
        # self._s.public = 0 | 1
        # self._s.audio_info = { 'key': 'val', ... }
        # (keys are shout.SHOUT_AI_BITRATE, shout.SHOUT_AI_SAMPLERATE,
        # shout.SHOUT_AI_CHANNELS, shout.SHOUT_AI_QUALITY)


        total = 0
        st = time.time()
        print "opening file %s" % song_file
        f = open(song_file)
        self._s.set_metadata({'song': str(song_name)})

        nbuf = f.read(4096)
        while 1:
            buf = nbuf
            nbuf = f.read(4096)
            total += len(buf)
            if len(buf) == 0:
                break
            self._s.send(buf)
            self._s.sync()
        f.close()

        et = time.time()
        br = total * 0.008 / (et - st)
        print "Sent %d bytes in %d seconds (%f kbps)" % (total, et - st, br)
        pass
