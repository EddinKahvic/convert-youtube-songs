import os
import sys
import google_auth_oauthlib.flow
import googleapiclient.discovery
import yt_dlp
import re


class Playlist(object):
    def __init__(self, id, title):
        self.id = id
        self.title = title


class YoutubeClient(object):
    def __init__(self, client_secrets_file_location):
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        
        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file_location, scopes)
        credentials = flow.run_local_server(port=5000)
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials, num_retries=0)
        
        self.youtube_client = youtube_client


    def get_playlists(self):
        request = self.youtube_client.playlists().list(
            part="id, snippet",
            maxResults=20,
            mine=True
        )
        response = request.execute()
        
        playlists = [Playlist(item['id'], item['snippet']['title']) for item in response['items']]
        return playlists 


    def get_videos(self, playlist_id):
        request = self.youtube_client.playlistItems().list(
            part="id, snippet",
            maxResults=500,
            playlistId=playlist_id
        )
        response = request.execute()
        
        songs = []
        
        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            track = self.get_track(video_id)
            if track:
                songs.append(track)
                
        return songs


    def get_track(self, video_id):
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            
            # filter, only 'Music' is allowed
            if 'Music' in info['categories']:
                
                # Extract true title - get rid of: [], (), whitespace
                title = info['title']
                true_title = "".join(re.split("\(|\)|\[|\]", title)[::2]).strip()
                return true_title
            
            
    def run(self):
        
        # Get the playlist list from YouTube
        playlists = self.get_playlists()
        
        # Choose what playlist to extract music from
        for index, playlist in enumerate(playlists):
            print(f"{index}: {playlist.title}")
        choice = int(input("Enter the YouTube playlist: "))
        chosen_playlist = playlists[choice]
        print(f"You selected: {chosen_playlist.title}")
        
        # For each video in playlist, get track
        songs = self.get_videos(chosen_playlist.id)
        print(f"Attempting to add {len(songs)} songs...")
        
        # Add song titles to "songs.txt"
        textfile = open('songs.txt', 'w', encoding="utf-8")
        for song in songs:
            textfile.write(f'{song}\n')
        textfile.close()
        
        