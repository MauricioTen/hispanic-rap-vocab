import json
from dotenv import load_dotenv
from Genius_api import GeniusClient

# 1. Load environment variables (.env)
load_dotenv()

# 2. Initialize the client
c = GeniusClient()

# 3. Fetch the data from the API
data = c._get("/search", q="Nach")

# 4. Save the dictionary into a JSON file
with open("genius_search_nach.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("✅ Successfully saved search results to genius_search_nach.json!")