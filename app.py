"""Podcast Opportunity Explorer: a screening tool, not a deal recommendation."""

from pathlib import Path

import pandas as pd
import streamlit as st
from babel import Locale
from babel.core import UnknownLocaleError


DATA_PATH = Path(__file__).parent / "data" / "podcasts_sample.csv"
CATEGORY_COLUMNS = [f"category{i}" for i in range(1, 9)]


@st.cache_data
def load_feeds(path: str) -> pd.DataFrame:
    """Load the public sample and make screening fields explicit."""
    feeds = pd.read_csv(path, low_memory=False)
    feeds["latest_episode"] = pd.to_datetime(
        feeds["newestItemPubdate"].replace(0, pd.NA), unit="s", utc=True
    )
    feeds["language_normalized"] = feeds["language"].fillna("").str.strip().str.lower()
    feeds["guid_normalized"] = feeds["podcastGuid"].fillna("").str.strip()
    feeds["episode_count"] = pd.to_numeric(feeds["episodeCount"], errors="coerce").fillna(0)
    feeds["discovery_score"] = pd.to_numeric(
        feeds["popularityScore"], errors="coerce"
    ).fillna(-1)
    for column in CATEGORY_COLUMNS:
        feeds[column] = feeds[column].fillna("").str.strip().str.lower()
    return feeds


def category_options(feeds: pd.DataFrame) -> list[str]:
    values = pd.concat([feeds[column] for column in CATEGORY_COLUMNS])
    return sorted(value for value in values.unique() if value)


def language_label(code: str) -> str:
    """Turn a source language tag such as en-us into a readable English label."""
    try:
        return Locale.parse(code, sep="-").get_display_name("en").title()
    except (UnknownLocaleError, ValueError):
        return code


def screen_feeds(
    feeds: pd.DataFrame,
    category: str,
    language: str,
    days_active: int,
    min_episodes: int,
    explicit_preference: str,
    min_discovery_score: int,
) -> tuple[pd.DataFrame, dict[str, int], pd.Timestamp]:
    """Apply the project's stated screening rules and retain audit counts."""
    snapshot = feeds["latest_episode"].max()
    active_start = snapshot - pd.Timedelta(int(days_active), unit="D")
    valid_date = feeds["latest_episode"].notna()
    language_match = (
        feeds["language_normalized"].str.startswith("en")
        if language == "English (all variants)"
        else feeds["language_normalized"].eq(language)
    )
    active_language = feeds.loc[
        valid_date
        & (feeds["latest_episode"] >= active_start)
        & (feeds["latest_episode"] <= snapshot)
        & language_match
    ].copy()
    category_match = active_language[CATEGORY_COLUMNS].eq(category).any(axis=1)
    matching_category = active_language.loc[category_match].copy()
    enough_episodes = matching_category.loc[
        matching_category["episode_count"] >= min_episodes
    ].copy()
    if explicit_preference == "Explicit only":
        enough_episodes = enough_episodes.loc[enough_episodes["explicit"].eq(1)].copy()
    elif explicit_preference == "Not explicit only":
        enough_episodes = enough_episodes.loc[enough_episodes["explicit"].eq(0)].copy()
    score_qualified = enough_episodes.loc[
        enough_episodes["discovery_score"] >= min_discovery_score
    ].copy()

    # A nonblank GUID represents one feed for this demonstration. Keep its first
    # occurrence; feeds without a GUID stay because they cannot be deduplicated safely.
    duplicate_guid = score_qualified["guid_normalized"].ne("") & score_qualified[
        "guid_normalized"
    ].duplicated(keep="first")
    eligible = score_qualified.loc[~duplicate_guid].copy()
    eligible = eligible.sort_values(
        ["discovery_score", "episode_count", "title"],
        ascending=[False, False, True],
        kind="stable",
    )
    counts = {
        "Loaded sample feeds": len(feeds),
        "Active selected-language feeds": len(active_language),
        "Matching category": len(matching_category),
        "Meeting episode minimum": len(enough_episodes),
        "Meeting score minimum": len(score_qualified),
        "Eligible feeds": len(eligible),
    }
    return eligible, counts, snapshot


st.set_page_config(page_title="Podcast Opportunity Explorer", layout="wide")
st.markdown(
    """
    <style>
      .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"],
      [data-testid="stSidebar"] {
        background-color: #ffffff;
        color: #151515;
      }
      p, h1, h2, h3, label, [data-testid="stMarkdownContainer"] {
        color: #151515 !important;
      }
      [data-testid="stSidebar"] { background-color: #f7f7f7; }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("Podcast Opportunity Explorer")
st.caption("A transparent research-screening tool for iHeartMedia acquisition managers.")

feeds = load_feeds(str(DATA_PATH))
categories = category_options(feeds)
default_index = categories.index("true crime") if "true crime" in categories else 0
language_codes = sorted(language for language in feeds["language_normalized"].unique() if language)
language_options = {"English (all variants)": "English (all variants)"}
for code in language_codes:
    label = f"{language_label(code)} ({code})"
    language_options[label] = code
default_language = 0

with st.sidebar:
    st.header("Screening controls")
    with st.form("screening_form"):
        category = st.selectbox("Category", categories, index=default_index)
        language_choice = st.selectbox(
            "Language", list(language_options), index=default_language
        )
        language = language_options[language_choice]
        days_active = st.selectbox("Active within", (30, 60, 90, 180), index=2, format_func=lambda n: f"{n} days")
        min_episodes = st.number_input("Minimum episodes", min_value=0, max_value=5000, value=20, step=5)
        explicit_preference = st.selectbox("Explicit-content preference", ("Any", "Explicit only", "Not explicit only"))
        min_discovery_score = st.number_input("Minimum discovery score", min_value=0, max_value=100, value=0, step=1)
        st.form_submit_button("Search feeds", type="primary", use_container_width=True)

eligible, counts, snapshot = screen_feeds(
    feeds,
    category,
    language,
    days_active,
    int(min_episodes),
    explicit_preference,
    int(min_discovery_score),
)
st.caption(f"Source snapshot: latest valid episode in this 6,000-feed sample, {snapshot.date():%B %-d, %Y}.")

columns = st.columns(len(counts))
for column, (label, value) in zip(columns, counts.items()):
    column.metric(label, f"{value:,}")

st.subheader("Feeds to research next")
st.write(
    f"{len(eligible):,} **{language_choice}** **{category}** feed(s) meet the selected screening rules. "
    "This is a research queue, not a recommendation to acquire or partner."
)

if eligible.empty:
    st.info("No feeds in the sample meet these settings. Try a wider activity window, a lower episode minimum, or another category.")
else:
    table = eligible[
        [
            "title",
            "category1",
            "latest_episode",
            "episode_count",
            "host",
            "discovery_score",
            "explicit",
        ]
    ].rename(
        columns={
            "title": "Title",
            "category1": "Primary category",
            "latest_episode": "Latest episode (UTC)",
            "episode_count": "Episodes",
            "host": "Host domain",
            "discovery_score": "Discovery score",
            "explicit": "Explicit flag",
        }
    )
    st.dataframe(table, use_container_width=True, hide_index=True)

with st.expander("Definitions and limits", expanded=True):
    st.markdown(
        f"""
        - **One row** is one crawled podcast feed, not necessarily one unique show.
        - **Active** means its latest nonzero episode timestamp is within the selected window before the sample's latest valid timestamp ({snapshot.date():%Y-%m-%d}), not necessarily active today.
        - **Language** and **category** are self-declared feed metadata; category is a match in category fields 1–8.
        - Repeated nonblank Podcast GUIDs are deduplicated by retaining the first feed; blank GUIDs remain because they cannot be reliably deduplicated.
        - The discovery score is a Podcast Index discovery signal. It is **not** audience size, downloads, revenue, ownership, rights, brand safety, or acquisition value.
        - Shortlisted feeds still require audience, rights, ownership, editorial, commercial, and brand-safety review before any partnership decision.
        - This public demonstration uses a 6,000-row course sample, not the full Podcast Index catalog.
        """
    )
