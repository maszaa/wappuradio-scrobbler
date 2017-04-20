import sys
import datetime, time
import requests
import pylast


def getNowPlaying():
    try:
        nowPlaying = requests.get("https://wappuradio.fi/api/nowplaying")
        artistTitle = nowPlaying.json()["song"].split(" - ")
        # Fallback to '-' splitter if the song doesn't have whitespaces around the splitter
        if len(artistTitle) == 0:
            artistTitle = nowPlaying.json()["song"].split('-')
            artistTitle = [item.strip() for item in artistTitle]
        return artistTitle[0], artistTitle[1], nowPlaying.json()["timestamp"]
    except (KeyError, IndexError, requests.ConnectionError):
        print("Problem with fetching now playing data from Wappuradio API")
        return False, False, False

def scrobble(username, network):
    oldStartedPlaying = ""
    while True:
        artist, title, startedPlaying = getNowPlaying()
        if startedPlaying != oldStartedPlaying and artist and title:
            oldStartedPlaying = startedPlaying
            try:
                network.scrobble(artist = artist, title = title, \
                                 timestamp = int(time.mktime(datetime.datetime.now().timetuple())))
                
                # Confirm the scrobble
                print("Confirmation from Last.fm:")
                print(network.get_user(username).get_recent_tracks(limit=1))
            except (pylast.WSError, pylast.MalformedResponseError, pylast.NetworkError, \
                    pylast.ScrobblingError):
                print("Problem with internet connection, Last.fm network or scrobbling")

        time.sleep(60)

def main():
    if len(sys.argv) == 5:
        apiKey = sys.argv[1]
        apiSecret = sys.argv[2]

        username = sys.argv[3]
        passwordHash = pylast.md5(sys.argv[4])

        try:
            # Create connection to Last.fm
            network = pylast.LastFMNetwork(api_key=apiKey, api_secret=apiSecret,
                                           username=username, password_hash=passwordHash)
            scrobble(username, network)
        except (pylast.WSError, pylast.MalformedResponseError, pylast.NetworkError):
            print ("Problem with internet connection or Last.fm network")
            sys.exit(1)

    # Incorrect amount of arguments passed   
    print("Please give arguments API_key, API_secret, username and password" + \
          " when running the script")

main()
