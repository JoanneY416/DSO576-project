"""Recalculate Kellen's two observed live screens without importing app.py."""
import csv
import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data/podcasts_sample.csv"
OBSERVED_ON = "2026-11-08 America/Los_Angeles"
OBSERVED_TITLES = [
    "The UNspecial Podcast", "Dear Son,", "The Chop Shop Show",
    "Schoolyard Sports with Lane Frank", "Dreamland Chronicles",
    "Nancy's Nook Podcast", "Beyond Dollars & Sense",
]


def numeric(row, field, default):
    try:
        return float(row[field]) if row[field].strip() else default
    except ValueError:
        return default


def timestamp(row):
    value = numeric(row, "newestItemPubdate", 0)
    return datetime.fromtimestamp(value, timezone.utc) if value else None


def main():
    with DATA.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    dates = [timestamp(row) for row in rows]
    snapshot = max(date for date in dates if date is not None)
    cutoff = snapshot - timedelta(days=90)
    active = [row for row, date in zip(rows, dates)
              if date is not None and cutoff <= date <= snapshot
              and row["language"].strip().lower().startswith("en")]
    category = [row for row in active
                if any(row[f"category{i}"].strip().lower() == "kids"
                       for i in range(1, 9))]
    episodes = [row for row in category if numeric(row, "episodeCount", 0) >= 20]
    cases = []
    for explicit in ["Any", "Not explicit only"]:
        flagged = [row for row in episodes if explicit == "Any"
                   or numeric(row, "explicit", -1) == 0]
        qualified = [row for row in flagged if numeric(row, "popularityScore", -1) >= 0]
        seen, eligible = set(), []
        for row in qualified:
            guid = row["podcastGuid"].strip()
            if guid and guid in seen:
                continue
            if guid:
                seen.add(guid)
            eligible.append(row)
        eligible.sort(key=lambda row: (-numeric(row, "popularityScore", -1),
                                      -numeric(row, "episodeCount", 0), row["title"]))
        actual_titles = [row["title"] for row in eligible]
        observed_titles = [title for title in OBSERVED_TITLES
                           if explicit == "Any" or title != "The Chop Shop Show"]
        # The current app labels its combined episode/explicit stage as episode-only.
        displayed_counts = [len(rows), len(active), len(category), len(flagged),
                            len(qualified), len(eligible)]
        observed_counts = [6000, 316, 9, 7, 7, 7] if explicit == "Any" else [6000, 316, 9, 6, 6, 6]
        assert actual_titles == observed_titles, (explicit, actual_titles)
        assert displayed_counts == observed_counts, (explicit, displayed_counts)
        cases.append({
            "explicit_preference": explicit,
            "independent_counts": {"loaded": len(rows), "active_english": len(active),
                                   "kids_category": len(category), "episode_only": len(episodes),
                                   "after_explicit": len(flagged), "after_score": len(qualified),
                                   "eligible": len(eligible)},
            "observed_live_displayed_counts": observed_counts,
            "ordered_titles_match_live": True,
            "rows": [{key: row[key] for key in
                      ["id", "title", "explicit", "episodeCount", "popularityScore",
                       "podcastGuid", "newestItemPubdate", "description"]} for row in eligible],
        })
        print(explicit, displayed_counts, "PASS; episode-only count:", len(episodes))
    report = {
        "observed_on": OBSERVED_ON,
        "source_sha256": hashlib.sha256(DATA.read_bytes()).hexdigest(),
        "app_sha256": hashlib.sha256((ROOT / "app.py").read_bytes()).hexdigest(),
        "snapshot_utc": snapshot.isoformat(), "cutoff_utc": cutoff.isoformat(),
        "invalid_latest_episode_rows": sum(date is None for date in dates),
        "settings": {"category": "kids", "language": "English (all variants)",
                     "days": 90, "min_episodes": 20, "min_score": 0},
        "cases": cases,
        "scope": "Independent sample calculations compared with two recorded live screens; not age-suitability validation.",
    }
    (ROOT / "kellen-case-audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print("Saved kellen-case-audit.json")


if __name__ == "__main__":
    main()
