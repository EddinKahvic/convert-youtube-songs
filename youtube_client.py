import os

import google_auth_oauthlib
import googleapiclient.discovery
import yt_dlp

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

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
        part="snippet, id",
        maxResults=20,
        mine=True
    )
    pass

def get_videos(self, playlist_id):
    # Only retrive videos with the VideoCategory.id = 10 (Music)
    pass

def get_artist_and_track(self, video_id):
    pass