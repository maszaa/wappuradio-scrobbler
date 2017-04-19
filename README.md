# wappuradio-scrobbler
Fetches now playing information from https://wappuradio.fi/api/nowplaying every 60 seconds and submits the track information to Last.fm API with the help of pylast (if the timestamp of the info has changed).

## Requirements
Python 3.x, pylast and requests

## Usage
First you need to get yourself an api key here https://www.last.fm/api/account/create<br>
Then you can start scorbbling by running the script:<br>
`python scrobbler.py API_key API_secret username password`
