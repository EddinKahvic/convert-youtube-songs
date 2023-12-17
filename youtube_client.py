import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import yt_dlp

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

class Song(object):
    def __init__(self, artist, track):
        self.artist = artist
        self.track = track

class Playlist(object):
    def __init__(self, id, title):
        self.id = id
        self.title = title

class YoutubeClient(object):
    def __init__(self, client_secrets_file_location):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        
        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file_location, scopes)
        credentials = flow.run_console()
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)
        
        self.youtube_client = youtube_client


    def get_playlists(self):
        request = self.playlists().list(
            part="id, snippet",
            maxResults=20,
            mine=True
        )
        response = request.execute()
        
        playlists = [Playlist(item['id'], item['snippet']['title']) for item in response['items']]
        return playlists 


    def get_liked_videos(self):
        request = self.videos().list(
            part="id, snippet",
            myRating="like"
        )
        response = request.execute()
        liked_videos = [liked_video for liked_video in response['items']]
        return liked_videos


    def get_videos(self, playlist_id):
        request = self.playlistItems().list(
            part="id, snippet",
            playlistId=playlist_id
        )
        response = request.execute()
        
        songs = []
        
        for item in response['items']:
            video_id = item['snippet']['resrouceId']['videoId']
            artist, track = get_artist_and_track(video_id)
            if artist and track:
                songs.append(Song(artist, track))
                return songs


    def get_artist_and_track(self, video_id):
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        
        video = yt_dlp.YoutubeDL({'quiet': True}).extract_info(
            youtube_url, download=False
        )
        
        artist = video['artist']
        track = video['track']
        return artist, track