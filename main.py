from ytmusicapi import YTMusic
import requests

yt = YTMusic()
name = 'Miracle'
artist = 'moses bliss'

prefix = 'https://music.youtube.com/watch?v='

sample_youtube_url = "https://music.youtube.com/watch?v=GzMRxWGFQaY&si=TXSXelogE-Rbltvo"


def fetchFromApple(song_details):
    url = f"https://itunes.apple.com/search?media=music&term={song_details}&entity=musicTrack&limit=1"

    r = requests.get(url=url)

    data = r.json()

    return data


def getAuthorAndTitleFromUrl(youtube_url):
    index = youtube_url.index("watch?")
    if index == -1:
        return None
    queryParams = sample_youtube_url[index + len("watch?"):]
    parts = queryParams.split("&")
    videoId = parts[0].split('=')[1]

    res = yt.get_song(videoId=videoId)

    searchTerm = res['videoDetails']['title'] + ' by ' + res['videoDetails']['author']
    result = fetchFromApple(searchTerm)['results']
    if len(result) == 0:
        return None
    choice = result[0]['trackViewUrl']
    print(choice)


getAuthorAndTitleFromUrl(sample_youtube_url)



