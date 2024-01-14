from youtube_client import YoutubeClient

def run():
    # Get the playlist list from YouTube
    youtube_client = YoutubeClient('./credentials/client_secret.json')   
    playlists = youtube_client.get_playlists()
    
    # Choose what playlist to extract music from
    for index, playlist in enumerate(playlists):
        print(f"{index}: {playlist.title}")
    choice = int(input("Enter the playlist: "))
    chosen_playlist = playlists[choice]
    print(f"You selected: {chosen_playlist.title}")
    
    # For each video in playlist, get track and artist
    songs = youtube_client.get_videos(chosen_playlist.id)
    print(f"Attempting to add {len(songs)} songs...")
    for song in songs:
        print(song.track)

    
        



if __name__ == '__main__':
    run()