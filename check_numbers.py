"""Independently reproduce the two published screening counts from the CSV sample.

This intentionally does not import the Streamlit app. It uses the CSV module to
check the default True Crime/English screen at two activity windows.
"""

import csv
from datetime import datetime, timedelta, timezone
from pathlib import Path


DATA_PATH = Path(__file__).parent / "data" / "podcasts_sample.csv"
CATEGORY_COLUMNS = [f"category{i}" for i in range(1, 9)]


def latest_episode(row: dict[str, str]) -> datetime | None:
    value = row["newestItemPubdate"].strip()
    if not value or value == "0":
        return None
    return datetime.fromtimestamp(int(value), tz=timezone.utc)


def eligible_count(rows: list[dict[str, str]], days_active: int, snapshot: datetime) -> int:
    start = snapshot - timedelta(days=days_active)
    seen_guids: set[str] = set()
    count = 0

    for row in rows:
        episode = latest_episode(row)
        language = row["language"].strip().lower()
        categories = {row[column].strip().lower() for column in CATEGORY_COLUMNS}
        episode_count = int(row["episodeCount"] or 0)
        discovery_score = int(row["popularityScore"] or -1)

        if episode is None or not start <= episode <= snapshot:
            continue
        if not language.startswith("en") or "true crime" not in categories:
            continue
        if episode_count < 20 or discovery_score < 0:
            continue

        guid = row["podcastGuid"].strip()
        if guid and guid in seen_guids:
            continue
        if guid:
            seen_guids.add(guid)
        count += 1

    return count


with DATA_PATH.open(newline="", encoding="utf-8") as file:
    feeds = list(csv.DictReader(file))

snapshot = max(episode for row in feeds if (episode := latest_episode(row)) is not None)
print(f"Rows loaded: {len(feeds)}")
print(f"Snapshot: {snapshot.date().isoformat()}")
for days in (30, 90):
    print(f"Eligible True Crime English feeds, {days} days: {eligible_count(feeds, days, snapshot)}")
