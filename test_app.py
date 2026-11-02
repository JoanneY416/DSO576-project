import pandas as pd

from app import screen_feeds


def test_screening_keeps_blank_guid_and_removes_repeat_guid() -> None:
    feeds = pd.DataFrame(
        {
            "latest_episode": pd.to_datetime(["2026-01-10", "2026-01-09", "2026-01-08"], utc=True),
            "language_normalized": ["en-us", "en", "en"],
            "guid_normalized": ["same", "same", ""],
            "episode_count": [20, 30, 25],
            "discovery_score": [1, 9, 3],
            "title": ["First", "Duplicate", "No GUID"],
            **{f"category{i}": ["true crime", "true crime", "true crime"] if i == 1 else ["", "", ""] for i in range(1, 9)},
        }
    )
    eligible, counts, _ = screen_feeds(
        feeds, "true crime", "English (all variants)", 30, 20, "Any", 0
    )
    assert list(eligible["title"]) == ["No GUID", "First"]
    assert counts["Eligible feeds"] == 2
