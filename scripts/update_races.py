from pathlib import Path
import json

out = Path("races.json")

# Temporary starter data.
# This proves the workflow works by rewriting races.json.
races = [
    {
        "date": "2026-07-29",
        "race": "Tour de France",
        "url": "https://www.letour.fr/en/overall-route",
        "stage": "Stage 21",
        "route": "Thoiry > Paris Champs-Élysées",
        "category": "Flat Stage",
        "distance": "133 km",
        "elevation": "Low climbing",
        "difficulty": "1/5",
        "profile_summary": "Traditional finale on the Champs-Élysées.",
        "discipline": "Road",
        "uk": "TNT Sports / HBO Max",
        "usa": "Peacock",
        "canada": "FloBikes"
    }
]

out.write_text(json.dumps(races, indent=2) + "\n", encoding="utf-8")
