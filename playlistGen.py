import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

#Client_ID, Client_Secret, and Redirect_URI set in enviroment variables

scope = 'playlist-modify-public'
#Would have to change username for each individual
username = 'brad.dinger13'

token = SpotifyOAuth(scope=scope, username=username)
spotifyObject = spotipy.Spotify(auth_manager=token)

def getSongSeedRecs(songRecList, numRecs):
    result = spotifyObject.recommendations(seed_tracks = songRecList, limit = numRecs)
    return result

def createPlaylist():
    #Playlist creation
    playlistName = input('\nEnter name of playlist:')
    playlistDesc = input('Enter playlist description:')

    spotifyObject.user_playlist_create(user=username, name=playlistName, public=True, collaborative=False, description=playlistDesc)

def getCreatedPlaylist():
    #Gets users playlists
    playlists = spotifyObject.user_playlists(user=username)

    #Newest playlist URI
    newPlaylistURI = playlists['items'][0]['id']
    return newPlaylistURI

def seedInput():
    #Take in seed songs
    songSeeds = input('\nEnter seed song: ')
    print()
    songURIs=[]
    songRecList=[]
    
    #Allows searching for songs
    result = spotifyObject.search(q=songSeeds, type='track')
    length = result['tracks']['total']

    #Finds top 10 search results
    if length >= 10:
        for x in range(0, 10):
            trackName = result['tracks']['items'][x]['name']
            albumName = result['tracks']['items'][x]['album']['name']
            trackURI = result['tracks']['items'][x]['uri']
            artistName = result['tracks']['items'][x]['album']['artists'][0]['name']

            print(f"{x+1}. {trackName} - {albumName} by {artistName}")

            songURIs.append(trackURI)
    else:
        for x in range(0, length):
            trackName = result['tracks']['items'][x]['name']
            albumName = result['tracks']['items'][x]['album']['name']
            trackURI = result['tracks']['items'][x]['uri']
            artistName = result['tracks']['items'][x]['album']['artists'][0]['name']

            print(f"{x+1}. {trackName} - {albumName} by {artistName}")

            songURIs.append(trackURI)
    
    songChoice = int(input('\nEnter number 1-10 to choose a song:'))
    

    if songChoice >= 1 and songChoice <=10:
        x = songChoice - 1
    else:
        print("\nInput must be a number between 1 and 10!")
        quit()
        
    #Used for adding songs to playlist
    songRecList.append(songURIs[x])
    return songRecList

if __name__ == "__main__":
    #Enter Seed Song
    songRecList = seedInput()

    #Get song seed recomendations
    numRecs = (int(input("Enter desired playlist length (between 5-100): ")) - 1)
    if numRecs < 4 or numRecs > 99:
        print("Try again with a number between 5 and 100!")
        quit()
    recList = getSongSeedRecs(songRecList, numRecs)
    for x in range(0,numRecs):
        print(recList['tracks'][x]['name'])
        trackURI = recList['tracks'][x]['uri']
        songRecList.append(trackURI)

    choice = input("\nEnter 'Y' to keep this playlist: ")

    if choice == 'Y' or choice == 'y':
        createPlaylist()
        #Add Songs to playlist
        newPLaylist = getCreatedPlaylist()
        spotifyObject.playlist_add_items(playlist_id=newPLaylist, items=songRecList)
    else: 
        print("Okay, please try again!")