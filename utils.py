import re

def extract_episod_id(url:str):
    episode_id = re.search(r"episode\/(\w+)",
                            url).group(1)
    return episode_id