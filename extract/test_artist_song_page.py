from dotenv import load_dotenv; load_dotenv()
from Genius_api import GeniusClient
r = GeniusClient().artist_songs_page(221938, 1)   # Lil Supa
print(r.keys(), len(r["songs"]), r["next_page"])