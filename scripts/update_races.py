from pathlib import Path
import json
from datetime import date
import requests
from bs4 import BeautifulSoup

OUT = Path("races.json")
TODAY = date.today()
HEADERS = {"User-Agent": "Mozilla/5.0"}

SOURCES = [
    "https://www.procyclingstats.com/calendar/uci/today",
    "https://www.uci.org/calendar/all/2jnxYAuvjgttyHi6YQ94EJ",
    "https://www.uci.org/calendar/road/2ruOnavHX0dMGTCRozdYAU",
    "https://www.uci.org/calendar/mtb/",
]

def fetch(url):
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.text

def guess_races_from_text(text, source_url):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    races = []
    for line in lines:
        if len(line) < 8:
            continue
        if any(k in line for k in ["Tour", "World", "UCI", "Classic", "Race", "Championship", "Road", "MTB", "Cyclo", "Gravel"]):
            races.append({
                "date": TODAY.isoformat(),
                "race": line[:120],
                "url": source_url,
                "stage": "Upcoming event",
                "route": "TBA",
                "category": "Calendar event",
                "distance": "TBA",
                "elevation": "TBA",
                "difficulty": "TBA",
                "profile_summary": "Upcoming cycling event from calendar source.",
                "discipline": "Cycling",
                "uk": "TBA",
                "usa": "TBA",
                "canada": "TBA"
            })
    return races

def scrape_source(url):
    html = fetch(url)
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text("\n", strip=True)
    return guess_races_from_text(text, url)

def main():
    races = []
    for url in SOURCES:
        try:
            races.extend(scrape_source(url))
        except Exception:
            continue

    deduped = []
    seen = set()
    for race in races:
        key = (race["race"], race["url"])
        if key not in seen:
            seen.add(key)
            deduped.append(race)

    if not deduped:
        raise RuntimeError("No races found from calendar sources")

    OUT.write_text(json.dumps(deduped, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
