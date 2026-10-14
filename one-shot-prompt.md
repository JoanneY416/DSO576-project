# Podcast Opportunity Explorer — One-Shot Build Prompt

*How to read this prompt:* **Vision** and **Design** explain the product and
architecture. **Precise contracts** names each independently buildable piece.
The remaining sections give the data, reliability, and completion decisions a
coding agent needs; the paste-ready block below is the implementation request.

## 1. Vision

**Who uses it.** An iHeartMedia content-acquisition manager who needs to find
podcasts worth researching when the company has a gap in a content category.
They have limited time for initial review and need a consistent way to narrow a
very large catalog into a manageable investigation queue.

**The decision it serves.** Which podcast feeds should move to preliminary
editorial and commercial research first. The tool does not decide which show to
acquire, value, or offer a partnership to.

**Why it is better than the current approach.** Without the tool, a manager may
search podcast directories manually, rely on personal familiarity, or receive
an unstructured list of suggestions. That process makes it difficult to apply
the same activity and catalog-history criteria consistently or to explain why a
feed was included. The tool applies transparent rules to the Podcast Index
catalog and shows how each screen reduces the candidate pool.

**What the user cares about.**

- Whether a feed is publishing recently enough to merit review.
- Whether it has enough episode history to suggest an established publishing
  record.
- Whether it fills the selected content-category gap.
- A discovery signal that can help prioritize research, without confusing it
  for audience size or commercial value.
- A clear explanation of the data’s limitations: feed metadata does not show
  listeners, ownership, rights, partnership availability, revenue, or
  brand-safety suitability.

**Concrete use cases.**

- A manager needs more active English-language science podcasts. They select
  “Science,” an activity window of 90 days, and a minimum of 20 episodes. The
  tool shows filter attrition and a ranked feed queue. The manager selects a
  small number of feeds for editorial review and external audience research.

- A manager is looking for recently active business podcasts but wants to focus
  staff time on more established feeds. They select “Business,” require
  activity within 30 days, and raise the episode minimum. The tool shows which
  feeds remain and why the pool became smaller. The manager decides whether the
  criteria are too restrictive or whether the remaining feeds should be
  investigated.

- A manager wants an initial list of category-matching feeds with a stronger
  Podcast Index discovery signal. They enable a minimum `popularityScore`. The
  tool ranks eligible feeds and clearly labels the score as a discovery signal
  rather than evidence of downloads, revenue, or acquisition value. The manager
  uses the results only to prioritize due diligence.

## 2. Design

Build the prototype as a short, one-way pipeline. Each piece has a small public
contract, can be built and tested in one agent session, and should fail with an
actionable error at its own boundary rather than creating a large, intertwined
agent-written application.

```text
CSV sample or SQLite snapshot
            ↓
source inspection and read
            ↓
normalization, deduplication, screening, and ranking
            ↓
screening result: counts, rows, snapshot date, data-quality notes
            ↓
Streamlit controls and presentation
```

### Design principles

1. **One set of screening rules for both sources.** The CSV prototype and the
   SQLite path must have logically equivalent normalization, eligibility,
   deduplication, attrition, and ranking rules. Otherwise a result changes just
   because the data source changes, making the tool hard to trust.

2. **Filter large data where it lives.** The full SQLite database is too large
   to load into pandas on every interaction. Inspect its schema, filter,
   deduplicate, aggregate, and rank in SQL where practical, then return only
   the records and counts required by the page. This keeps the full-source app
   responsive and memory-safe.

3. **Keep business logic pure and independent of the UI.** Cleaning,
   screening, ranking, and count calculations take data and settings as inputs
   and return results without reading widgets, files, or session state. This
   makes the most consequential logic easy to unit-test on a tiny invented
   table and prevents UI changes from quietly changing decisions.

4. **One piece, one job, one clear contract.** Source loading does not render;
   screening does not open files or create widgets; Streamlit does not recreate
   data rules. A piece should be understandable, buildable, and checkable by
   itself in one agent session. Its errors should identify the broken source,
   schema, or input rather than fail somewhere downstream.

5. **Expose uncertainty instead of inventing certainty.** The page presents an
   investigation queue and its filter attrition, not a commercial score or
   acquisition recommendation. Missing metadata, duplicate feeds, and the
   limits of `popularityScore` remain visible to the manager.

6. **Start small and preserve a runnable path.** The tracked sample CSV is the
   default development and test path. The absence of the local SQLite snapshot
   must not prevent the prototype from starting; the page should state which
   source it is using.

## 3. Precise contracts

**1. Source loader — `src/load_data.py`**

- **Job:** Locate the sample CSV or optional SQLite snapshot, inspect and
  validate required columns, and read only the data needed for screening.
- **Receives:** A source choice or the default source paths, plus the selected
  screen settings when SQL can apply them safely.
- **Passes:** A source metadata object (source mode, source row count, and
  schema notes) and a feed DataFrame or SQL result containing the fields needed
  by `screening.py`.
- **Checks alone:** It can validate both source schemas, report missing columns
  clearly, and confirm that the sample path works when SQLite is absent.

**2. Screening logic — `src/screening.py`**

- **Job:** Convert timestamps, normalize language and categories, deduplicate
  nonblank GUIDs, apply the active/category/episode/score rules, calculate
  attrition, and apply the specified ranking tie-breaks.
- **Receives:** Feed records and a small plain settings object: category,
  active-days window, minimum episodes, and optional minimum discovery score.
- **Passes:** A `ScreeningResult` (or equivalent simple structure) containing
  the snapshot date, attrition counts, ranked display rows, and data-quality
  notes such as GUID rows removed.
- **Checks alone:** Unit tests use a tiny invented DataFrame to verify every
  data rule and expected result order without Streamlit or either real source.

**3. App page — `app.py`**

- **Job:** Render the controls, call the loader and screening logic, and show
  source context, attrition, the sortable results table, empty states, and the
  mandatory limitations text.
- **Receives:** Widget values and the loader/screening outputs.
- **Passes:** Nothing to another application piece; it presents the completed
  investigation queue to the user.
- **Checks alone:** It starts against the sample source, handles no matching
  feeds cleanly, and never contains a second copy of the screening rules.

**4. Tests and run instructions — `tests/test_screening.py`, `README.md`**

- **Job:** Preserve the screening contract and make the local prototype
  repeatable for a teammate or evaluator.
- **Receives:** The public functions from `screening.py` and the app's required
  local commands.
- **Passes:** Fast regression checks and exact setup, run, and test commands.
- **Checks alone:** Tests run without the full SQLite snapshot; the README
  explains optional full-source use separately.

## 4. Data and technical design

The dataset repository is `dataset_podcast-index/`. Its tracked
`sample/podcasts_sample.csv` is the small, repeatable development source; pandas
can load it for the prototype and pure-data tests. Its `download_data.py`
downloads the optional full SQLite snapshot into its gitignored `data/` folder.
The archive is about 1.81 GB and expands to about 5.06 GB, so the README must
state that the sample is sufficient and the full snapshot needs about 8 GB free
disk space. The source loader must give a clear sample-mode fallback when that
snapshot is absent.

The SQLite snapshot is the full-scale source: inspect its actual schema, then
use Python's standard-library `sqlite3` SQL to filter, deduplicate, aggregate,
and rank, returning only the page’s counts and display columns instead of
loading 4.7M+ rows into pandas. Use pandas only for the small sample and pure
screening functions. Keep a read-only SQLite connection and source metadata
cached by source path and modification time; do not cache a user’s filter result
in a way that can become stale. Keep source access separate from pure screening
logic and the Streamlit UI, and preserve equivalent rules across sources.

Use a small `requirements.txt` with Streamlit, pandas, and pytest; `sqlite3` is
part of Python. The README must give these local commands after dependencies are
installed: `streamlit run app.py` and `pytest`. For later cloud deployment,
replace the local source adapter with a managed query service or an object-store
snapshot cache, while retaining the same `load_data.py` contract and pure
screening logic.

## 5. Assumptions, edge cases, and data quality

- A row is a crawled RSS/Atom feed, not necessarily one unique show.
- Zero, missing, or invalid timestamps are missing; never interpret them as
  January 1970.
- The snapshot date is the latest valid timestamp, and the active boundary is
  inclusive.
- Normalize language and all category fields before filtering; blanks do not
  match.
- Deduplicate only nonblank GUIDs; retain blank GUIDs and disclose duplicates
  removed.
- Missing episode counts filter as zero but remain visibly missing; missing
  discovery scores filter as zero only when a minimum score is enabled.
- `popularityScore`, host, language, and categories are metadata, not evidence
  of audience, ownership, geography, rights, value, or suitability.

## 6. Build order and “done when” checks

Build source inspection/loading first, then pure normalization and screening
functions with tiny-table tests, then the sample CSV path and Streamlit page,
then the optional SQLite path, README, and final verification. Done means the
sample app starts without SQLite; tests cover timestamp, language, category,
GUID, boundary, and ranking rules; displayed attrition reconciles to a sample
result; the limitations warning is visible; and Git has no raw or generated
large data staged. The final handoff reports changed files, commands, check
results, and any SQLite schema differences.

Use one tiny invented table for the pure screening tests: include two rows with
the same nonblank GUID but different timestamps, a blank-GUID row, `en-US`,
`en_gb`, a category only in `category8`, a zero timestamp, and equal scores and
episode counts. The expected result must retain the newest nonblank-GUID row,
retain the blank-GUID row, exclude the zero timestamp, normalize both English
tags, find the eighth-category match, and resolve the tie by title then `id`.

## How to use this file

This is the single prompt to give a coding agent after the items in **Before you
run it** are checked. Replace only the bracketed paths if this project is cloned
somewhere else. Do not silently broaden the product beyond the acquisition
screen described here.

## Before you run it

- [ ] Confirm the SQLite snapshot exists locally at
  `../dataset_podcast-index/data/podcastindex_feeds.db` (it is intentionally
  ignored by Git).
- [ ] Run the prototype on the tracked sample first:
  `../dataset_podcast-index/sample/podcasts_sample.csv`.
- [ ] Decide whether the deliverable is a local Streamlit prototype only
  (recommended for this assignment) or needs deployment later.
- [ ] Have a team member review the displayed definitions and limitations below.

## Prompt

```text
You are building a small, local Streamlit prototype in this repository:

    DSO576-project/

Build only the iHeartMedia content-acquisition workspace of the Podcast
Opportunity Explorer. Its user is an iHeartMedia content-acquisition manager
who has a category gap and needs a transparent queue of podcasts to research.
The page creates an initial screening list; it must never claim to recommend,
value, acquire, or guarantee a partnership with a podcast.

Start by inspecting this repository and `dataset_podcast-index`. This prompt and
the dataset repository are sufficient to build the app; inspect the dataset
repository's README and data overview before using its full snapshot.

## Deliverable

Create a runnable local Streamlit app, concise README/run instructions, and
tests for the pure data logic. Keep raw data, credentials, downloaded archives,
and derived large files out of Git. Prefer a small, readable implementation
over an elaborate framework.

The app must work with the tracked CSV sample first:

    ../dataset_podcast-index/sample/podcasts_sample.csv

It should also support the local full SQLite snapshot when it is present:

    ../dataset_podcast-index/data/podcastindex_feeds.db

Do not require the full database to start the sample prototype. For the SQLite
path, filter and aggregate in SQL; do not load all 4.7M+ rows into pandas.
The dataset repository's `download_data.py` retrieves the optional snapshot;
its archive needs about 1.81 GB to download and about 8 GB free disk space to
download and unpack. The README must say that the sample is enough to run the
prototype and must provide `streamlit run app.py` and `pytest` commands after
dependency installation.

## Product scope

Build one page, “Acquisition screen,” with these controls:

1. Category: one normalized category selected from the available categories.
2. Active within: 30, 90, or 180 days; default 90.
3. Minimum episode count: a numeric input; default 20.
4. Optional minimum discovery score (`popularityScore`); default disabled.

Show, in this order:

- the source mode (sample CSV or full SQLite), source row count, and the
  snapshot date used for the activity calculation;
- filter attrition: loaded feeds, feeds with a valid latest-episode timestamp,
  active English feeds, category-matching feeds, and eligible feeds;
- a ranked, sortable table with `title`, matching category or categories,
  language, latest episode date, `episodeCount`, `host`, `popularityScore`, and
  `explicit`;
- a short definition/limitations panel.

No map, export feature, feed-profile page, localization workspace, audience
estimate, composite score, outreach automation, or deal recommendation.

## Exact data rules

Use the Podcast Index feed grain: one row is a crawled RSS/Atom feed, not
necessarily one unique show.

1. Convert `newestItemPubdate` Unix timestamps to UTC. A zero, missing, or
   invalid timestamp is missing, never January 1970.
2. Define `snapshot_date` as the maximum valid `newestItemPubdate` in the
   selected source. A feed is active when its date is on or after
   `snapshot_date - active_days`; state whether the boundary is inclusive and
   test it.
3. Normalize language by trimming whitespace, lowercasing, and taking the part
   before `-` or `_`. English means normalized language exactly `en`.
4. Normalize all eight category columns (`category1` through `category8`) by
   trimming whitespace and lowercasing. A feed matches the selected category if
   any normalized category field equals it. Ignore blank categories.
5. Deduplicate before ranking. For a nonblank `podcastGuid`, retain one row per
   GUID: the row with the most recent valid `newestItemPubdate`, then the
   largest `episodeCount`, then the smallest stable `id`. Retain every blank
   GUID because blank values cannot be reliably deduplicated. Report the number
   of rows removed by this rule in an expandable data-quality note.
6. Treat missing or invalid `episodeCount` as zero for the minimum-episode
   screen, but preserve a clearly displayed missing value where appropriate.
7. Treat missing `popularityScore` as zero only when an optional minimum score
   is applied. Otherwise display it as missing/zero exactly as stored; document
   which convention you choose.
8. Rank eligible feeds by `popularityScore` descending, then `episodeCount`
   descending, then `title` ascending, then `id` ascending. Do not calculate a
   composite score.

For the full database, first inspect the actual schema with SQLite rather than
assuming a sample-only column type. Implement the same rules in SQL where
practical, returning only the display columns and counts needed by the page.
Keep the sample and full-source results logically equivalent.

## Required wording and guardrails

Make this warning visible on the page:

“Each result is a podcast feed, not necessarily a unique show. Categories and
languages are publisher-provided metadata. popularityScore is a discovery
signal, not listeners, downloads, revenue, rights, ownership, brand safety, or
acquisition value. Every shortlisted feed requires audience, editorial,
ownership, rights, financial, and brand-safety review.”

Also explain that the host is the RSS-serving domain and is not proof of
ownership or network affiliation. Never infer creator geography from language.

## Suggested file structure

Use this only if it fits the existing repository; do not overwrite a teammate's
work:

    app.py                 # Streamlit page and widget wiring
    src/load_data.py       # source selection and SQLite/CSV loading
    src/screening.py       # pure cleaning, screening, ranking, and counts
    tests/test_screening.py
    requirements.txt or pyproject.toml
    README.md              # setup and run steps, if one does not already exist

Keep cleaning and screening functions independent of Streamlit so they can be
unit-tested on a small invented DataFrame. Cache source reads appropriately, but
do not cache user-specific filters in a way that produces stale results.

## Acceptance checks

Before reporting completion, run and report these checks:

1. The app starts against the sample CSV without the full database.
2. The test suite covers: zero timestamp handling; `en-US` and `en_gb` matching
   English; a category found only in `category8`; nonblank GUID deduplication;
   blank-GUID retention; the active-window boundary; and the ranking tie-breaks.
3. Counts in the attrition display reconcile with the result table for at least
   one sample configuration.
4. The page includes the required warning and makes no unsupported commercial
   claim.
5. `git status` confirms raw data and generated large files are not staged.

When finished, provide: (a) the files created or changed, (b) exact commands to
run the sample prototype and tests, (c) the checks performed and their results,
and (d) any assumptions or schema differences found in the full database.
```

## How to finish after the first build

1. Run the app with the sample data and test the three activity windows, at
   least two categories, a zero episode threshold, and a high score threshold.
2. Inspect a few table rows manually: compare their timestamp, categories, GUID,
   and sort order with the source data.
3. Run the same screen against the full SQLite snapshot. Record the snapshot
   date, selected settings, row counts at each attrition stage, and any schema
   differences in a small version-controlled results note.
4. Have a teammate review the limitations text. It should clearly separate an
   investigation queue from evidence of audience, ownership, rights, safety, or
   deal value.
5. Only after those checks, consider the broader Riverside localization
   workspace. It needs Riverside product data or creator research; feed-language
   counts alone are not a localization business case.
