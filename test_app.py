import pandas as pd

from validate_current_mvp import current_functions

# Importing app.py runs its UI during collection and contaminates AppTest.
# Load the real calculation definitions without starting the Streamlit form.
_, screen_feeds, eligible_display_table = current_functions(include_display=True)


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


def test_eligible_display_table_shows_all_source_category_fields() -> None:
    eligible = pd.DataFrame(
        {
            "title": ["Example feed"],
            **{
                f"category{i}": ["true crime" if i == 3 else ""]
                for i in range(1, 9)
            },
            "latest_episode": pd.to_datetime(["2026-01-10"], utc=True),
            "episode_count": [20],
            "host": ["example.com"],
            "discovery_score": [4],
            "explicit": [0],
        }
    )

    table = eligible_display_table(eligible)

    assert list(table.columns) == [
        "Title",
        "Primary category",
        "Secondary category 1",
        "Secondary category 2",
        "Secondary category 3",
        "Secondary category 4",
        "Secondary category 5",
        "Secondary category 6",
        "Secondary category 7",
        "Latest episode (UTC)",
        "Episodes",
        "Host domain",
        "Discovery score",
        "Explicit flag",
    ]
    assert table.loc[0, "Secondary category 2"] == "true crime"
