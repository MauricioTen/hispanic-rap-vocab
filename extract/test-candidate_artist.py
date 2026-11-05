from dotenv import load_dotenv; load_dotenv()
from Genius_api import GeniusClient
print(GeniusClient().candidate_artists("Residente"))