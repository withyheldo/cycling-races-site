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
]

def fetch(url):
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.text

def parse_pcs_today(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text("\n", strip=True)
    races = []
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    for line in lines:
        if any(keyword in line for keyword in ["WorldTour", "UCI", "MTB", "gravel", "cyclo-cross", "road"]):
            races.append({
                "date": TODAY.isoformat(),
                "race": line[:120],
                "url": "https://www.procyclingstats.com/calendar/uci/today",
                "stage": "Upcoming race",
                "route": "TBA",
                "category": "Calendar event",
                "distance": "TBA",
                "elevation": "TBA",
                "difficulty": "TBA",
                "profile_summary": "Upcoming cycling event from calendar page.",
                "discipline": "Cycling",
                "uk": "TBA",
                "usa": "TBA",
                "canada": "TBA"
            })
            if len(races) >= 10:
                break
    return races

def parse_uci_all(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text("\n", strip=True)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    races = []

    for line in lines:
        if len(races) >= 10:
            break
        if any(month in line for month in ["Aug", "Sep", "Oct", "Nov", "Dec"]):
            races.append({
                "date": TODAY.isoformat(),
                "race": line[:120],
                "url": "https://www.uci.org/calendar/all/2jnxYAuvjgttyHi6YQ94EJ",
                "stage": "Upcoming race",
                "route": "TBA",
                "category": "Calendar event",
                "distance": "TBA",
                "elevation": "TBA",
                "difficulty": "TBA",
                "profile_summary": "Upcoming cycling event from UCI calendar.",
                "discipline": "Cycling",
                "uk": "TBA",
                "usa": "TBA",
                "canada": "TBA"
            })
    return races

def main():
    races = []

    for url in SOURCES:
        try:
            html = fetch(url)
            if "procyclingstats" in url:
                races.extend(parse_pcs_today(html))
            else:
                races.extend(parse_uci_all(html))
        except Exception:
            continue

    deduped = []
    seen = set()
    for race in races:
        key = (race["race"], race["url"])
        if key not in seen:
            seen.add(key)
            deduped.append(race)

    OUT.write_text(json.dumps(deduped, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
