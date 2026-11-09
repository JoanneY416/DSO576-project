"""Independently check the current app's sample counts; do not start a server."""
import ast
import csv
import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "data/podcasts_sample.csv"


def current_functions():
    # Execute the actual calculation definitions without the Streamlit UI.
    tree = ast.parse((ROOT / "app.py").read_text())
    definitions = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in {"load_feeds", "screen_feeds"}:
            node.decorator_list = []
            definitions.append(node)
    scope = {"pd": pd, "CATEGORY_COLUMNS": [f"category{i}" for i in range(1, 9)]}
    exec(compile(ast.Module(body=definitions, type_ignores=[]), "app.py", "exec"), scope)
    return scope["load_feeds"], scope["screen_feeds"]


def oracle(rows, category, language, days, minimum, explicit, score):
    # Independent CSV + Python loop calculation, without pandas filters.
    def date(row):
        try:
            value = float(row["newestItemPubdate"])
            return datetime.fromtimestamp(value, timezone.utc) if value else None
        except (ValueError, OverflowError, OSError):
            return None

    def number(row, key, default):
        try:
            return float(row[key]) if row[key].strip() else default
        except ValueError:
            return default

    dates = [date(r) for r in rows]
    snapshot = max(d for d in dates if d is not None)
    active = []
    for row, stamp in zip(rows, dates):
        lang = row["language"].strip().lower()
        matches = lang.startswith("en") if language == "English (all variants)" else lang == language
        if stamp is not None and snapshot - timedelta(days=days) <= stamp <= snapshot and matches:
            active.append(row)
    matching = [r for r in active if category in [r[f"category{i}"].strip().lower() for i in range(1, 9)]]
    episodes = [r for r in matching if number(r, "episodeCount", 0) >= minimum]
    if explicit != "Any":
        wanted = 1 if explicit == "Explicit only" else 0
        episodes = [r for r in episodes if number(r, "explicit", -1) == wanted]
    qualified = [r for r in episodes if number(r, "popularityScore", -1) >= score]
    seen = set()
    eligible = []
    for row in qualified:
        guid = row["podcastGuid"].strip()
        if guid and guid in seen:
            continue
        if guid:
            seen.add(guid)
        eligible.append(row)
    eligible.sort(key=lambda r: (-number(r, "popularityScore", -1), -number(r, "episodeCount", 0), r["title"]))
    return [len(rows), len(active), len(matching), len(episodes), len(qualified), len(eligible)], eligible, snapshot


def main():
    with SOURCE.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames
        rows = list(reader)
    load, screen = current_functions()
    feeds = load(str(SOURCE))
    settings = [
        ("sofia-baseline", "music", "es", 90, 20, "Any", 0),
        ("sofia-no-minimum", "music", "es", 90, 0, "Any", 0),
        ("sophie-health", "health", "English (all variants)", 90, 20, "Any", 0),
        ("english-default", "true crime", "English (all variants)", 90, 20, "Any", 0),
        ("english-30-days", "true crime", "English (all variants)", 30, 20, "Any", 0),
        ("english-60-days", "true crime", "English (all variants)", 60, 20, "Any", 0),
        ("spanish-explicit", "music", "es", 90, 0, "Explicit only", 0),
        ("spanish-not-explicit", "music", "es", 90, 0, "Not explicit only", 0),
        ("spanish-score-100", "music", "es", 90, 0, "Any", 100),
        ("spanish-5000-episodes", "music", "es", 90, 5000, "Any", 0),
    ]
    results = []
    for name, *arguments in settings:
        expected, records, snapshot = oracle(rows, *arguments)
        actual, counts, actual_snapshot = screen(feeds, *arguments)
        assert list(counts.values()) == expected, (name, counts, expected)
        assert actual["id"].astype(str).tolist() == [str(r["id"]) for r in records], name
        assert actual_snapshot.to_pydatetime() == snapshot, name
        assert all(a >= b for a, b in zip(expected, expected[1:])), name
        results.append({"case": name, "counts": expected, "titles": actual["title"].tolist(), "status": "PASS"})
        print(name, expected, "PASS")

    # Tiny worked fixture: inclusive date boundary, category8, blank GUIDs,
    # first-occurrence GUID handling and language matching.
    raw = pd.DataFrame({
        "latest_episode": pd.to_datetime(["2026-01-31", "2026-01-01", "2026-01-15", "2025-12-31", "2026-01-20"], utc=True),
        "language_normalized": ["es", "es", "es", "es", "es-mx"],
        "guid_normalized": ["same", "", "same", "", ""],
        "episode_count": [20, 10, 30, 20, 20],
        "discovery_score": [1, 3, 9, 1, 1],
        "explicit": [0, 1, 0, 0, 0],
        "title": ["First", "Boundary", "Duplicate", "Too old", "Regional"],
        **{f"category{i}": ["music"] * 5 if i == 8 else [""] * 5 for i in range(1, 9)},
    })
    answer, counts, _ = screen(raw, "music", "es", 30, 0, "Any", 0)
    assert list(counts.values()) == [5, 3, 3, 3, 3, 2]
    assert answer["title"].tolist() == ["Boundary", "First"]
    reversed_answer, _, _ = screen(raw.iloc[::-1], "music", "es", 30, 0, "Any", 0)
    assert reversed_answer["title"].tolist() == ["Duplicate", "Boundary"]
    print("worked-fixture PASS; reversing input changes the surviving GUID record (documented limitation)")
    report = {"source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              "app_sha256": hashlib.sha256((ROOT / "app.py").read_bytes()).hexdigest(),
              "rows": len(rows), "columns": len(fields), "snapshot": snapshot.isoformat(),
              "cases": results, "worked_fixture": "PASS", "guid_input_order_sensitive": True,
              "scope": "Current repository calculations; not live-deployment verification or browser tests."}
    target = ROOT / "validation-check-results.json"
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print("Saved", target.name)


if __name__ == "__main__":
    main()
