from pathlib import Path
from Genius_api import GeniusClient
from dotenv import load_dotenv
import csv
import time
import unicodedata

load_dotenv()

# Path(__file__).parent is the 'extract/' directory.
# .parent again moves up one level to 'latam-rap-vocab/'
BASE_DIR = Path(__file__).parent.parent

# Fixed filename (rapper instead of rappers) and robust path building:
INPUT = BASE_DIR / "data" / "hispanic_rappers_list_sample.csv"
OUTPUT = BASE_DIR / "data" / "hispanic_rappers_output.csv"


#normilize the artist names to match Genius API format
def normalize(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c)).lower().strip()


def main() -> None:
    client = GeniusClient()

    with INPUT.open(encoding="utf-8") as f:
        rappers = list(csv.DictReader(f))

    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rapper_name", "country", "candidate_id", "candidate_name", "is_exact_match"])

        for row in rappers:
            name = row["rapper_name"]
            candidates = client.candidate_artists(name)   # {id: name}
            print(f"{name}: {len(candidates)} candidates")

            for cand_id, cand_name in candidates.items():
                exact = normalize(name) == normalize(cand_name)   # compare normalize(name) with normalize(cand_name)
                writer.writerow([name, row["country"], cand_id, cand_name, exact])

            time.sleep(1)  # be polite to the API


if __name__ == "__main__":
    main()