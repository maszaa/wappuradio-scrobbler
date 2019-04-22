# wappuradio-scrobbler
Fetches now playing information from https://wappuradio.fi/api/nowplaying every 60 seconds and submits the track information to Last.fm API with the help of pylast (if the timestamp of the info has changed).

## Requirements
Python 3.x (tested with 3.7.3).

## Usage
1. Create API account: https://www.last.fm/api/account/create.
2. Copy `template.env.sh` to `env.sh` and insert Last.fm API key and shared secret there.
3. Run `start.sh`.
4. The script opens a Last.fm website to authorize the application. Authorize the application.
5. Press any key in your terminal to start scrobbling.
