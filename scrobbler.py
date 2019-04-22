import time
import datetime
from collections import namedtuple

import requests

Track = namedtuple("Track", ["artist", "title", "timestamp"])

class Scrobbler(object):
    """
    Class to fetch now playing track from Wappuradio API and scrobbling it to Last.fm
    """

    def __init__(self, lastfm_network, lastfm_username):
        self.wappuradio_api_url = "https://wappuradio.fi/api/nowplaying"
        self.now_playing_track = None
        self.lastfm_network = lastfm_network
        self.lastfm_username = lastfm_username

    def get_now_playing_track(self):
        """
        Fetch now playing track from Wappuradio API with requests and parse data.

        Returns:
            collections.namedtuple("Track", ["artist", "title", "timestamp"])
        or
            None

        """

        try:
            now_playing = requests.get(self.wappuradio_api_url)
            artist_title = now_playing.json()["song"].split(" - ")

            # Fallback to "-" splitter if the song doesn't have whitespaces around
            # the splitter
            if not artist_title:
                artist_title = now_playing.json()["song"].split("-")
                artist_title = [item.strip() for item in artistTitle]

            return Track(
                artist=artist_title[0],
                title=artist_title[1],
                timestamp=(
                    time.mktime(datetime.datetime.strptime(now_playing.json()["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ").timetuple()) +
                    datetime.datetime.now().astimezone().tzinfo.utcoffset(None).seconds
                )
            )
        except Exception as err:
            print("Problem with fetching now playing data from Wappuradio API or something else\n", err)
            return None

    def scrobble(self, track):
        """
        Scrobble track to Last.fm with pylast.

        Params: collections.namedtuple("Track", ["artist", "title", "timestamp"])

        """

        if track and (not self.now_playing_track or track.timestamp != self.now_playing_track.timestamp):
            try:
                self.lastfm_network.scrobble(
                    artist=track.artist,
                    title=track.title,
                    timestamp=track.timestamp
                )

                lastfm_recent_tracks = self.lastfm_network.get_user(self.lastfm_username).get_recent_tracks(limit=1)
                if lastfm_recent_tracks:
                    lastfm_recent_track = lastfm_recent_tracks[0]
                    print("Confirmation from Last.fm: {0:s} - {1:s} @ {2:s} / {3:s}".format(
                        lastfm_recent_track.track.artist.name,
                        lastfm_recent_track.track.title,
                        lastfm_recent_track.playback_date,
                        lastfm_recent_track.timestamp
                    ))

                self.now_playing_track = track
            except Exception as err:
                print("Problem with internet connection, Last.fm network or scrobbling\n", err)
