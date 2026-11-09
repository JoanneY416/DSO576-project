"""Regression checks for the current app, using hand-worked records."""
import pandas as pd
import pytest
from validate_current_mvp import ROOT, current_functions


def fixture():
    return pd.DataFrame({
        "latest_episode": pd.to_datetime(["2026-01-31", "2026-01-01", "2025-12-31", None], utc=True),
        "language_normalized": ["es"] * 4,
        "guid_normalized": ["", "", "", ""],
        "episode_count": [20, 10, 5, 30],
        "discovery_score": [2, 1, 0, 9],
        "explicit": [0, 1, 0, 0],
        "title": ["Latest", "Boundary", "Old", "Missing date"],
        **{f"category{i}": ["music"] * 4 if i == 8 else [""] * 4 for i in range(1, 9)},
    })


def screen(rows, language="es", episodes=0, score=0, explicit="Any"):
    return current_functions()[1](rows, "music", language, 30, episodes, explicit, score)


def test_inclusive_boundary_category8_and_missing_date():
    result, counts, _ = screen(fixture())
    assert result.title.tolist() == ["Latest", "Boundary"]
    assert list(counts.values()) == [4, 2, 2, 2, 2, 2]


@pytest.mark.parametrize("minimum,expected", [(10, ["Latest", "Boundary"]), (20, ["Latest"]), (21, [])])
def test_episode_boundary(minimum, expected):
    assert screen(fixture(), episodes=minimum)[0].title.tolist() == expected


@pytest.mark.parametrize("minimum,expected", [(1, ["Latest", "Boundary"]), (2, ["Latest"]), (3, [])])
def test_score_boundary(minimum, expected):
    assert screen(fixture(), score=minimum)[0].title.tolist() == expected


@pytest.mark.parametrize("preference,expected", [("Explicit only", ["Boundary"]), ("Not explicit only", ["Latest"])])
def test_explicit_filter(preference, expected):
    assert screen(fixture(), explicit=preference)[0].title.tolist() == expected


def test_language_selection():
    rows = fixture()
    rows["latest_episode"] = pd.to_datetime(["2026-01-31"] * 4, utc=True)
    rows["language_normalized"] = ["en", "en-us", "es", "es-mx"]
    assert set(screen(rows, language="English (all variants)")[0].title) == {"Latest", "Boundary"}
    assert screen(rows)[0].title.tolist() == ["Old"]


def test_loader_zero_and_missing_numeric_values(tmp_path):
    row = {"newestItemPubdate": 0, "language": " ES ", "podcastGuid": " ", "episodeCount": "", "popularityScore": "bad", **{f"category{i}": " Music " for i in range(1, 9)}}
    source = tmp_path / "tiny.csv"
    pd.DataFrame([row]).to_csv(source, index=False)
    result = current_functions()[0](str(source))
    assert pd.isna(result.latest_episode.iloc[0])
    assert result.episode_count.iloc[0] == 0
    assert result.discovery_score.iloc[0] == -1
    assert result.language_normalized.iloc[0] == "es"
    assert result.guid_normalized.iloc[0] == ""


def test_empty_result_ui():
    # The legacy test imports the UI during collection. Isolate its global state.
    import subprocess
    import sys
    code = '''from streamlit.testing.v1 import AppTest
app = AppTest.from_file("app.py", default_timeout=60).run()
assert not app.exception
next(w for w in app.number_input if w.label == "Minimum episodes").set_value(5000)
next(w for w in app.button if w.label == "Search feeds").click()
app.run()
assert not app.exception
assert any("No feeds in the sample" in item.value for item in app.info)
'''
    subprocess.run([sys.executable, "-c", code], check=True, cwd=ROOT, capture_output=True, text=True)
