import sys
import datetime, time
import requests
import pylast


def getNowPlaying():
    try:
        nowPlaying = requests.get("https://wappuradio.fi/api/nowplaying")
        artistTitle = nowPlaying.json()["song"].split('-')
        return artistTitle[0].rstrip(), artistTitle[1].lstrip(), \
               nowPlaying.json()["timestamp"]
    except requests.ConnectionError:
        print("Problem with fetching now playing data from Wappuradio API")
        return False, False, False

def scrobble(username, network):
    oldStartedPlaying = ""
    while True:
        artist, title, startedPlaying = getNowPlaying()
        if startedPlaying != oldStartedPlaying and \
           artist and title and startedPlaying:
            oldStartedPlaying = startedPlaying
            network.scrobble(artist = artist, title = title, \
                             timestamp = int(time.mktime(datetime.datetime.now().timetuple())))
            
            # Confirm the scrobble
            print("Confirmation from Last.fm:")
            print(network.get_user(username).get_recent_tracks(limit=1)[0])

        time.sleep(60)

def main():
    apiKey = sys.argv[1]
    apiSecret = sys.argv[2]

    username = sys.argv[3]
    passwordHash = pylast.md5(sys.argv[4])

    # Create connection to Last.fm
    network = pylast.LastFMNetwork(api_key=apiKey, api_secret=apiSecret,
                                   username=username, password_hash=passwordHash)

    scrobble(username, network)


main()
