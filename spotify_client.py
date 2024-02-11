import requests
import os
from time import time
from flask import Flask, redirect, request, jsonify, session
from dotenv import load_dotenv
import urllib.parse
from datetime import datetime

class Playlist(object):
    def __init__(self, id, title):
        self.id = id
        self.title = title
        
load_dotenv('./credentials/.env')

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
redirect_uri = 'http://127.0.0.1:5000/callback'

authorize_url = 'https://accounts.spotify.com/authorize'
token_url = 'https://accounts.spotify.com/api/token'
api_base_url = 'https://api.spotify.com/v1'

current_time = time()
chosen_playlist_id = ''


@app.route('/')
def index():
    scope = 'user-read-private playlist-read-private playlist-modify-private'
    
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': redirect_uri,
        'show_dialog': True
    }
    
    auth_url = f'{authorize_url}?{urllib.parse.urlencode(params)}'
    
    return redirect(auth_url)

@app.route('/callback')
def callback(): 
    if 'error' in request.args:
        return jsonify({'error': request.args['error']})
    
    if 'code' in request.args: 
        request_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret
        }
        
        response = requests.post(token_url, data=request_body)
        token_info = response.json()
        
        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']
        
        if (session['user_id']):
            return redirect('/playlists')
        
        return redirect('/user')

@app.route('/user')
def user():
    if 'access_token' not in session:
        return redirect('/')
    
    if current_time > session['expires_at']:
        return redirect('/refresh-token')
    
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    
    user_info = requests.get('https://api.spotify.com/v1/me', headers=headers).json()
    session['user_id'] = user_info['id']
    return redirect('/playlists')

@app.route('/playlists')
def playlists():
    if 'access_token' not in session:
        return redirect('/')
    
    if current_time > session['expires_at']:
        return redirect('/refresh-token')
        
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    
    response = requests.get('https://api.spotify.com/v1/me/playlists', headers=headers).json()
    
    my_playlists = []
    
    for item in response['items']:
        owner_id = item['owner']['id']
        if session['user_id'] == owner_id:
            my_playlists.append(Playlist(item['id'], item['name']))
    
    
    for index, playlist in enumerate(my_playlists):
        print(f"{index}: {playlist.title}")
    choice = int(input("Enter the Spotify playlist: "))
    chosen_playlist = my_playlists[choice]
    print(f"You selected: {chosen_playlist.title}")
    chosen_playlist_id = chosen_playlist.id
    
    return redirect('/search')
            
@app.route('/search')
def search():
    pass

@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/')
    
    if current_time > session['expires_at']:
        request_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': client_id,
            'client_secret': client_secret
        }
        
        response = requests.post(token_url, data=request_body)
        new_token_info = response.json()
        
        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']
        
        return redirect('/playlists')
    

app.run(host='0.0.0.0', debug=True)
