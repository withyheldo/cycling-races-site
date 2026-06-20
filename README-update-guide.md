# LikeB1kes stage-by-stage update

## How to update the site
1. Open `races.json` in GitHub.
2. Click the pencil icon to edit.
3. Each object is one stage or one race day.
4. Change fields like `date`, `race`, `stage`, `route`, `profile`, and stream fields.
5. Commit to `main`.
6. Netlify will redeploy automatically from GitHub, and your GitHub Action can also trigger the build hook.

## Data format
Each item looks like:
```json
{
  "date": "2026-07-04",
  "race": "Tour de France",
  "stage": "Stage 1",
  "route": "Barcelone > Barcelone",
  "profile": "Team time trial",
  "discipline": "Road",
  "distance": "19.6 km",
  "uk": "TNT Sports / HBO Max",
  "usa": "Peacock",
  "canada": "FloBikes"
}
```
