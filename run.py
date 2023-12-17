from youtube_client import YoutubeClient

def run():
    # Get the playlist list from YouTube
    youtube_client = YoutubeClient('./credentials/client_secret_1061033002100-2pj465cq3fhsspi0a85d8jh5cgp2hs4p.apps.googleusercontent.com.json')   
    playlists = youtube_client.get_playlists()
    
    



if __name__ == '__main__':
    run()