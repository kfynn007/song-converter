from ytmusicapi import YTMusic
import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

yt = YTMusic()

def fetchFromApple(song_details, is_album):
    if is_album:
        url = f"https://itunes.apple.com/search?media=music&term={song_details}&entity=musicTrack&limit=1"
    else:
        url = f"https://itunes.apple.com/search?media=music&term={song_details}&entity=album&limit=1"

    r = requests.get(url=url)

    data = r.json()

    return data

@app.get("/youtube-to-apple")
def convertYoutubeUrlToAppleUrl(youtube_url):
    index = youtube_url.index("watch?")
    if index == -1:
        return None
    queryParams = youtube_url[index + len("watch?"):]
    parts = queryParams.split("&")
    videoId = parts[0].split('=')[1]

    res = yt.get_song(videoId=videoId)

    searchTerm = res['videoDetails']['title'] + ' by ' + res['videoDetails']['author']
    result = fetchFromApple(searchTerm)['results']
    if len(result) == 0:
        return None
    choice = result[0]['trackViewUrl']
    return choice


@app.get("/youtube-playlist-to-apple-playlist")
def convertYoutubePlaylistToApplePlayList(url):
    urls = []

    index = url.index("playlist?list=")
    if index == -1:
        return None

    queryParams = url[index+len('playlist?list='):]
    id = queryParams.split("&")[0]

    browse_id = yt.get_album_browse_id(id)

    album_details = yt.get_album(browse_id)


    print(album_details['title'])



    tracks = album_details['tracks']

    for track in tracks:

        artist = ''
        for person in track['artists']:
            name = person['name']
            artist += ' ' + name


        query = track['title'] + ' by ' + artist
        result = fetchFromApple(query)['results']
        if len(result) == 0:
            return None
        choice = result[0]['trackViewUrl']

        urls.append(choice)

    return urls


@app.get("/youtube-album-to-apple-album-final")
def convertYoutubeAlbumToAppleAlbum(url):

    index = url.index("playlist?list=")
    if index == -1:
        return None

    queryParams = url[index+len('playlist?list='):]
    id = queryParams.split("&")[0]

    browse_id = yt.get_album_browse_id(id)

    album_details = yt.get_album(browse_id)

    title = (album_details['title'])
    artists = album_details['artists']

    artist = ''

    for person in artists:
        name = person['name']
        artist += ' ' + name


    result = fetchFromApple(title+ ' by ' + artist, True)

    choice = result['results'][0]['trackViewUrl']
    return choice


