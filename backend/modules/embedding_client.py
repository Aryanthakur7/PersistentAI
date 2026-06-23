import requests
from config import EMBED_URL


def get_embedding(text):

    r = requests.post(
        EMBED_URL,
        json={"text": text}
    )
    
    r.raise_for_status()
    
    return r.json()["embedding"]
