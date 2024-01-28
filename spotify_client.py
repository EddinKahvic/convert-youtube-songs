import requests
import os
from time import time
from flask import Flask, redirect, request, jsonify, session
from dotenv import load_dotenv
import urllib.parse
from datetime import datetime

load_dotenv('./credentials/.env')

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
redirect_uri = 'http://127.0.0.1:5000/callback'

authorize_url = 'https://accounts.spotify.com/authorize'
token_url = 'https://accounts.spotify.com/api/token'
api_base_url = 'https://api.spotify.com/v1'


@app.route('/')
def index():
    return "<a href='/login'>Authorize</a>"

@app.route('/login')
def login():
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
        return redirect('/playlists')
    
@app.route('/playlists')
def playlists():
    if 'access_token' not in session:
        return redirect('/login')
    
    t = time()
    if t > session['expires_at']:
        return redirect('/refresh-token')
        
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    
    response = requests.get(url=api_base_url + '/me/playlists', headers=headers)
    playlists = response.json()
    return jsonify(playlists)

@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')
    
    if datetime.now().timestamp > session['expires_at']:
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
