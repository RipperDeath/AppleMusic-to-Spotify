import os
import sys
import spotipy
import argparse
from config import * #CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from spotipy.oauth2 import SpotifyOAuth
from libraryRework import XmlLibraryParser

#detect if os is windows or mac
if sys.platform == 'win32':
    try:
        path = os.environ['USERPROFILE'] + '\\Music\\iTunes\\Library.xml'
    except:
        print('iTunes library not found, please make sure You export your library to xml')
        sys.exit()
elif sys.platform == 'darwin':
    try:
        path = os.environ['HOME'] + '/documents/Library.xml'
    except:
        print('iTunes library not found, please make sure You export your library to xml')
        sys.exit()
else:
    print('OS not supported')
    sys.exit()

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
args = parser.parse_args()

class SpotifyLibraryConvert:
    def __init__(self, path):
        self.path = path
        
    def addToLibrary(self):
        data = XmlLibraryParser(self.path).libraryToJson()
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
        sp.current_user_saved_tracks_add(tracks=[songIdList])
        #print('Added ' + song + ' by ' + artist + ' to spotify')

    def makePlaylist(self):
        data = XmlLibraryParser(self.path).playlistToJson()
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
    convert = SpotifyLibraryConvert(path)
    
    convert.addToLibrary()
    convert.makePlaylist()
        