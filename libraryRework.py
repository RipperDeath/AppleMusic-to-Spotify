import sys
import xmltodict
 
class XmlLibraryParser:
    def __init__(self, path):
        self.path = path
        self.xmlToJson(self.path)
        self.libraryToJson()
        self.playlistToJson()

    def xmlToJson(self, path) -> object:
        #c0nert xml to json
        with open(path) as fd:
            doc = xmltodict.parse(fd.read())
            rawTrackList = doc['plist']['dict']['dict']
            playlistTackId = doc['plist']['dict']['array']

        return rawTrackList, playlistTackId


    def libraryToJson(self) -> object:
        rawTrackList, playlistTackId = self.xmlToJson(self.path)
        #get the dict from rawTrackList
        dict = rawTrackList['dict']
        #loop through all indexes in dict
        songArtist = []
        for index in dict:
            #get the string dict from index
            string = index['string']
            #prevent json dumb from giving end of file error
            if string == None:
                continue
            #get the song and artist from string
            song = string[0]
            artist = string[1]
            #add song and artist to list
            songArtist.append({'song': song, 'artist': artist})

        return songArtist

    def playlistToJson(self) -> object:
        rawTrackList, playlistTackId = self.xmlToJson(self.path)
        playlists = playlistTackId['dict']
        #skip first 2 dicts
        playlists = playlists[2:]
        #loop through all playlists
        playlistSongs = {'playlists': {}}
        for playlist in playlists:
            playlistName = playlist['string'][0]
            #add playlist key to dict
            playlistSongs['playlists'][playlistName] = []
            playlistTracks = playlist['array']['dict']
            for track in playlistTracks:
                trackId = track['integer']
                for index in rawTrackList['dict']:
                    ints = index['integer']
                    if ints[0] == trackId:
                        string = index['string']
                        song = string[0]
                        artist = string[1]
                        #add song and artist to playlist
                        playlistSongs['playlists'][playlistName].append({'song': song, 'artist': artist})
                        break

        return playlistSongs

if __name__ == '__main__':
    #path = os.environ['HOME'] + '/documents/Library.xml'
    XmlLibraryParser(sys.argv[1])
    #XmlLibraryParser(sys.argv[1])