import soundcloud
import urllib.request
import json
from tqdm import tqdm
import os
from flask import Flask, request

# Prompt the user for the artist name and file format
artist_name = input("Enter the name of the artist: ")
file_format = input("Enter the file format (mp3, ogg, or wav): ")

# Replace YOUR_API_KEY with your actual API key
client = soundcloud.Client(client_id='YOUR_API_KEY')

# Search for tracks by the specified artist
results = client.get('/tracks', q='artist: "' + artist_name + '"')

# Create a directory for the artist if it doesn't already exist
if not os.path.exists(artist_name):
    os.makedirs(artist_name)

# Iterate over all tracks in the search results and download them
for track in tqdm(results):
    # Download the track
    file_name = track.title + "." + file_format
    file_path = os.path.join(artist_name, file_name)
    try:
        urllib.request.urlretrieve(track.download_url + "?client_id=" + client.client_id, file_path)
    except Exception as e:
        print("Error downloading track:", e)

print("All tracks from artist downloaded successfully!")

# Set up a Flask server to handle webhook requests
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    # Get the payload of the webhook request
    payload = request.get_json()
    print(payload)

    # Check if the webhook is for a new track being posted by the artist
    if payload['resource'] == '/tracks' and payload['action'] == 'create':
        # Get the track data from the webhook payload
        track_data = payload['data']
        print(track_data)

        # Download the track
        file_name = track_data['title'] + "." + file_format
        file_path = os.path.join(artist_name, file_name)
        try:
            urllib.request.urlretrieve(track_data['download_url'] + "?client_id=" + client.client_id, file_path)
        except Exception as e:
            print("Error downloading track:", e)

        print("New track from artist downloaded successfully!")

    return "OK"

if __name__ == '__main__':
    app.run()
