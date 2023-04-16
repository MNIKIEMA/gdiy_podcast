import json
import spotipy
from pathlib import Path, PurePath
import requests
from spotipy.oauth2 import SpotifyClientCredentials
from spotify_dlx import SpotifyDLXClient
"""
client = SpotifyDLXClient(root_podcast="./data", root="./data")
client.login(username="nikiemamahamadi01@gmail.com", password="@NMahamadi@@@")
client.download_episode(episode_id_str="6jCObFeQTf0VARXdMv9iE4")

ids = "6jCObFeQTf0VARXdMv9iE4"
end_point = "https://api.spotify.com/v1/shows/{738c17f1be7a4a6582328db622e08c9b}"
query = end_point
url = requests.get(query)
birdy_uri = "https://open.spotify.com/show/6jCObFeQTf0VARXdMv9iE4"
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="738c17f1be7a4a6582328db622e08c9b",
                                                                             client_secret="c41ce866883b4ea4892daae6aca5f09e"))
results = spotify.show(show_id="6jCObFeQTf0VARXdMv9iE4",market="FR")
print(results['episodes']['items'][0])
"""
class SpotifyData:
    def __init__(self, root:Path, client_id:str, client_secret:str) -> None:
        self.root = root
        self.client_id = client_id
        self.client_secret = client_secret

    def loging(self):
        end_point = "https://api.spotify.com/v1/shows/{738c17f1be7a4a6582328db622e08c9b}"
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

def main():
    root = "./data/"
    client_id="738c17f1be7a4a6582328db622e08c9b"
    client_secret="c41ce866883b4ea4892daae6aca5f09e"
    data = SpotifyData(root=root, client_id=client_id,
                       client_secret=client_secret)
    data.fetch_episodes()

if __name__=="__main__":
    main()