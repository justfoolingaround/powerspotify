# PowerSpotify

Your Spotify Premium? More like *our* Spotify Premium.

I'll not clarify the process as you need to be a bit familiar with how Spotify functions internally to use this. A good tl;dr is that: A normal Spotify and a premium Spotify differ in **1** request (in terms of content delivery!).

## Safe?

Probably, if you run it in a small scale, that is.

## Usage

ngrok as of right now supports free static domains. This means that you can keep your local machine or Github workflow running "permanently" without ever having to worry about domains or anything.

Your environment or `.env` file should look something like this (the fields filled of course.):

```
SPOTIFY_USERNAME=
SPOTIFY_PASSWORD=
NGROK_DOMAIN=
NGROK_TOKEN=
PORT=5000
```

```sh
$ python powerspotify.py
```
