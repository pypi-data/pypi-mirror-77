# spotify-client
Client for interacting with the Spotify API

## Usage

First install the package with pip:

`pip install spotify-client`

Then import the client for usage in your application:

```python
from spotify_client import SpotifyClient

SPOTIFY_CLIENT_ID = 'client_id_from_spotify'
SPOTIFY_SECRET_KEY = 'secret_key_from_spotify'

client = SpotifyClient(SPOTIFY_CLIENT_ID, SPOTIFY_SECRET_KEY, identifier='test-spotify-client')
```

You'll need to generate your client ID and secret keys for authenticating with Spotify from their API console. You can
find the steps for doing that in the [Spotify documentation](https://developer.spotify.com/documentation/general/guides/app-settings/).

The client will make a request to generate the access_token the first time it makes a call to the API. It will then
cache the access token as an instance variable, to use in future requests by that client instance. This avoids the
overhead of having to make a request for the access token on each request to the API.

You can optionally pass an identifier to the constructor. This will be used in logging messages by the client to
uniquely identify logs for the client instance.
