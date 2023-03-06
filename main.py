import spotipy
import argparse
from config import * #CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from spotipy.oauth2 import SpotifyOAuth
from libraryRework import XmlLibraryParser

#spotify api credentials
scope = "user-library-modify playlist-modify-private playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=scope))

#testList = [{"song": "The Boy Is Mine","artist": "Brandy & Monica"}, {"song": "You Make Me Wanna...","artist": "Usher"}, {"song": "Too Close","artist": "Next"}, {"song": "U Know What's Up","artist": "Donell Jones"}]

#make cmd line args
parser = argparse.ArgumentParser(description='Convert iTunes library to Spotify')
parser.add_argument('-l', '--library', action='store_true', help='Add all songs in library to spotify')
parser.add_argument('-p', '--playlist', action='store_true', help='Add all playlists to spotify')
parser.add_argument('-lp', '--BOTH', action='store_true', help='Add all songs in library and playlists to spotify')
args = parser.parse_args()

class SpotifyLibraryConvert:
    def __init__(self):
        pass
   
    def addToLibrary(self):
        data = XmlLibraryParser().libraryToJson()
        songIdList = []
        for songArtist in data:
            song = songArtist['song']
            artist = songArtist['artist']
            #search for song and add to spotify
            results = sp.search(q='artist:' + artist + ' track:' + song, type='track')
            items = results['tracks']['items']
            if len(items) > 0:
                track = items[0]
                songIdList.append(track['id'])
                #print('adding track to list')
        sp.current_user_saved_tracks_add(tracks=[songIdList])
        #print('Added ' + song + ' by ' + artist + ' to spotify')

    def makePlaylist(self):
        data = XmlLibraryParser().playlistToJson()
        #create playlist and add songs to it
        for playlist in data['playlists']:
            playlistId = sp.user_playlist_create(user=sp.current_user()['id'], name=playlist)['id']
            songIdList = []
            for songArtist in data['playlists'][playlist]:
                song = songArtist['song']
                artist = songArtist['artist']
                #search for song and add to spotify
                results = sp.search(q='artist:' + artist + ' track:' + song, type='track')
                items = results['tracks']['items']
                if len(items) > 0:
                    track = items[0]
                    songIdList.append(track['id'])
            sp.user_playlist_add_tracks(user=sp.current_user()['id'], playlist_id=playlistId, tracks=songIdList)

if __name__ == '__main__':
    convert = SpotifyLibraryConvert()
    #get cmd line args
    if args.library:
        convert.addToLibrary()
    if args.playlist:
        convert.makePlaylist()
    if args.BOTH:
        convert.addToLibrary()
        convert.makePlaylist()
        