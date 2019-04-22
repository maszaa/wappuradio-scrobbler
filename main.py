import os
import time
import webbrowser

import pylast

from scrobbler import Scrobbler

def main():
    try:
        lastfm_api_key = os.environ.get("LASTFM_API_KEY")
        lastfm_secret = os.environ.get("LASTFM_SECRET")

        lastfm_network = pylast.LastFMNetwork(api_key=lastfm_api_key, api_secret=lastfm_secret)
        lastfm_session_key_generator = pylast.SessionKeyGenerator(lastfm_network)
        lastfm_auth_url = lastfm_session_key_generator.get_web_auth_url()

        webbrowser.open_new_tab(lastfm_auth_url)

        input("Press any key to continue after you've authorized this application in Last.fm...")

        lastfm_session_key, lastfm_username = lastfm_session_key_generator.get_web_auth_session_key_username(lastfm_auth_url)

        lastfm_network = pylast.LastFMNetwork(api_key=lastfm_api_key, api_secret=lastfm_secret, session_key=lastfm_session_key)
        scrobbler = Scrobbler(lastfm_network=lastfm_network, lastfm_username=lastfm_username)

        while True:
            track = scrobbler.get_now_playing_track()
            scrobbler.scrobble(track)

            time.sleep(60)
    except Exception as err:
        print("Problem with internet connection or Last.fm network\n", err)
        sys.exit(1)

if __name__ == "__main__":
    main()
