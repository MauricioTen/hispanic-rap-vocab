import os
import time
import requests

BASE_URL = "https://api.genius.com"

class GeniusClient:
    def __init__(self, token: str | None = None):
        self.session = requests.Session()
        token = token or os.environ["GENIUS_ACCESS_TOKEN"]
        self.session.headers["Authorization"] = f"Bearer {token}"


    def _get(self, path: str, *, max_retries: int = 3, **params) -> dict:
        URL = f"{BASE_URL}{path}"

        for attempt in range(max_retries):
            resp = self.session.get(f"{BASE_URL}{path}", params=params, timeout=30)

            if resp.status_code == 429 or resp.status_code >= 500:
                wait_time = 2 ** attempt #exponential backoff: 1s, 2s, 4s...
                print(f"Request failed with status code {resp.status_code}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                continue #loop again

            # non-transient error (4xx), raise an exception    
            resp.raise_for_status()   

            #sucessful response, return the JSON data (2xx status code)
            return resp.json()["response"]

        resp.raise_for_status()  # Raise an exception for any remaining errors


    def candidate_artists(self, name: str, pages: int = 3) -> dict[int, str]:
        found = {}
        for page in range(1, pages + 1):
            response = self._get("/search", q=name, page=page)
            for hit in response["hits"]:
                artist = hit["result"]["primary_artist"]
                found[artist["id"]] = artist["name"]
        return found










