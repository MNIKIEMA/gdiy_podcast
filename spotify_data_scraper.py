import re
import json
import spotipy
from pathlib import Path, PurePath
import requests
from spotipy.oauth2 import SpotifyClientCredentials
from spotify_dlx import SpotifyDLXClient
from utils import extract_episod_id
"""
client = SpotifyDLXClient(root_podcast="./data", root="./data")
client.login(username="nikiemamahamadi01@gmail.com", password="")
client.download_episode(episode_id_str="6jCObFeQTf0VARXdMv9iE4")

ids = "6jCObFeQTf0VARXdMv9iE4"
end_point = "https://api.spotify.com/v1/shows/{738c17f1be7a4a6582328db622e08c9b}"
query = end_point
url = requests.get(query)
birdy_uri = "https://open.spotify.com/show/6jCObFeQTf0VARXdMv9iE4"
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="",
                                                                             client_secret=""))
results = spotify.show(show_id="6jCObFeQTf0VARXdMv9iE4",market="FR")
print(results['episodes']['items'][0])
"""
class SpotifyData:
    def __init__(self, root:Path, client_id:str, client_secret:str) -> None:
        self.root = root
        self.client_id = client_id
        self.client_secret = client_secret

    def loging(self):
        end_point = "https://api.spotify.com/v1/shows/{}"
        url = requests.get(end_point)
        episode_uri = "https://open.spotify.com/show/6jCObFeQTf0VARXdMv9iE4"
        spotify = spotipy.Spotify(client_credentials_manager=\
                                  SpotifyClientCredentials(client_id=self.client_id,
                                    client_secret=self.client_secret))
        return spotify
        
    def fetch_episodes(self):
        spotify = self.loging()
        results = spotify.show(show_id="6jCObFeQTf0VARXdMv9iE4",market="FR")
        
        episode = results['episodes']['items']
        results = spotify.next(results['episodes'])
        print(episode.__len__())
        while results['next']:
            results = spotify.next(results)
            episode.extend(results['items'])
        with open(PurePath(self.root,'gdiy_episode.json'), 'w', encoding='utf-8') as f:
            json.dump(episode, f, ensure_ascii=False, indent=4)

class SpotifyAudioLoader(object):
    def __init__(self,root_podcast,root, data_path, username, password):
        self.client = SpotifyDLXClient(root_podcast=root_podcast, root=root)
        self.client.login(username=username, password=password)
        self.data_path = data_path
    
    def load_data(self):
        with open(self.data_path, "r", encoding="utf-8") as fp:
            json_data = json.load(fp=fp)
        return json_data
    
    def process_data(self):
        data = self.load_data()
        for episode in data:
            link = episode["external_urls"]["spotify"]
            episode_id = extract_episod_id(url=link)
            self.client.download_episode(episode_id_str=episode_id)


def main():
    username="nikiemamahamadi01@gmail.com"
    password="MY_PASSWORD"
    root = "data/"
    root_podcast="data/"
    client_id="MY_ID"
    client_secret="MY_SECRET"
    data = SpotifyAudioLoader(root=root, root_podcast=root_podcast,
                              data_path="./data/gdiy_episode.json",
                              username=username, password=password)
    data.process_data()

if __name__=="__main__":
    main()