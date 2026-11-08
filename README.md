# Podcast Opportunity Explorer

## What it is

Podcast Opportunity Explorer is a transparent screening tool for iHeartMedia content-acquisition managers. It helps them make an initial research queue of active podcast feeds that match a category, language, episode-history, explicit-content, and discovery-score screen. This matters because researchers have limited time and need a reproducible way to identify feeds for deeper review.

The app is a screening tool, not an acquisition recommendation. It does not measure audience size, revenue, ownership, rights, brand safety, or deal value. Every shortlisted feed still needs verified audience analytics plus editorial, commercial, ownership, and rights review.

## Live app

<https://dso576-project-podcast-index.streamlit.app/>

The team tested the link in an incognito browser window. Before submitting, test it again without signing in and wake it if Streamlit has put it to sleep.

## Demo video

**To add before submission:** replace this sentence with the team's public, unlisted demo-video link and test it in an incognito browser window.

## Data

The live app uses `data/podcasts_sample.csv`, a 6,000-row course sample from Podcast Index rather than the full Podcast Index catalog. It therefore reports results only for feeds represented in that sample; a promising feed absent from the sample cannot appear in its queue. Each row is a crawled podcast feed, not necessarily a unique show.

The app defines activity from the latest nonzero episode timestamp in the sample. A feed is active when its latest episode falls within the selected window before that snapshot date. Language and category are self-declared feed metadata, and repeated nonblank Podcast GUIDs are deduplicated. Blank GUIDs remain because they cannot be deduplicated safely.

## Run on a laptop

In PowerShell, bash, or zsh, run these commands from the repository's parent folder:

```text
cd DSO576-project
uv sync
uv run streamlit run app.py
```

To independently check the two documented default-screen counts:

```text
cd DSO576-project
uv run python check_numbers.py
```

## Project files

- `app.py` — Streamlit app and screening rules.
- `test_app.py` — automated regression test for duplicate GUID handling.
- `check_numbers.py` — independent CSV-based count check used in the validation.
- `validation.md` — the working source for `validation.pdf`.
