from youtube_client import YoutubeClient
#from spotify_client import SpotifyClient

def run():
    # Get the playlist list from YouTube
    youtube_client = YoutubeClient('./credentials/client_secret.json')
    playlists = youtube_client.get_playlists()
    
    # Choose what playlist to extract music from
    for index, playlist in enumerate(playlists):
        print(f"{index}: {playlist.title}")
    choice = int(input("Enter the YouTube playlist: "))
    chosen_playlist = playlists[choice]
    print(f"You selected: {chosen_playlist.title}")
    
    # For each video in playlist, get track
    songs = youtube_client.get_videos(chosen_playlist.id)
    print(f"Attempting to add {len(songs)} songs...")
    
    # Add song titles to "songs.txt"
    textfile = open('songs.txt', 'w')
    for song in songs:
        textfile.write(f'{song}\n')
        
    textfile.close()

    
    # run spotify_client, getting auth-token
    # fetch spotify_id
    # fetch owned spotify playlists
    # choose the desired playlist
    # search for all the songs on spotify, returning the uris.
    # check if the song already exists in the playlist (optional)
    # add songs to specified playlist in increments of 100 (single request limit)
    
        
        

    
        



if __name__ == '__main__':
    run()