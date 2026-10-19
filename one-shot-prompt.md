# Podcast Opportunity Explorer — One-Shot Build Prompt

Build a runnable local Streamlit prototype from this file, the dataset repository,
and public internet. Inspect existing code; preserve unrelated teammate work.
Choose styling and nonessential wording.

## 1. Vision and scope

An iHeartMedia content-acquisition manager has a category gap and limited time to
investigate podcasts. Help them decide which feeds to research first by comparing
publishing recency, episode count, and a Podcast Index discovery signal. Explicit filters, attrition counts, and deterministic ordering improve on
inconsistent manual directory searches. This stakeholder workflow is a product
hypothesis, not validated iHeartMedia practice.

| User selects | Tool shows | User decides next |
|---|---|---|
| Science, 90 days, at least 20 episodes | Stage counts and ranked eligible feeds | Which feeds merit editorial and external audience research |
| Business, 30 days, a higher episode minimum | A smaller pool and where feeds were excluded | Whether to relax criteria or investigate the remaining feeds |
| A category and an enabled discovery-score minimum | Feeds passing that additional threshold | Which feeds warrant initial investigation using this limited signal |

Build one **Acquisition screen** page. Exclude maps, exports, feed-profile pages,
localization, outreach, composite scores, and deal recommendations.

## 2. Design principles and pieces

- **Separate presentation, rules, and access:** changes to widgets or storage should
  not change screening behavior; each piece must be independently checkable.
- **One rule contract, two executors:** pure pandas is the sample reference;
  SQLite handles full-source preparation and queries. Shared fixtures detect drift.
- **Prepare once, query repeatedly:** millions of raw rows stay on disk, so widget
  interactions do not repeat normalization or GUID sorting.
- **Show uncertainty:** preserve missing values and disclose metadata limitations,
  because this tool supports research rather than commercial valuation.

```text
controls → source adapter → pandas / SQLite executor → ScreeningResult → UI
```

Suggested modules (adapt names to existing code):

| Piece | Input → output / responsibility | Independent check |
|---|---|---|
| `src/contracts.py` | Plain values → structures below; no I/O or Streamlit | Import and settings validation |
| `src/load_data.py` | Mode and paths → SourceInfo and sample DataFrame or owned read-only connection; inspect schema | Missing-file fallback and actionable errors |
| `src/screening.py` | Raw sample, Settings, UTC as-of date → ScreeningResult; pure transformations | Fixed fixture |
| `src/sql_screening.py` | Connection, Settings, same as-of date → ScreeningResult; owns SQL preparation and queries | Temporary SQLite fixture equivalence |
| `app.py` | Controls and contracts → rendered page; no screening logic | Defaults and empty-state smoke checks |
| `tests/`, `README.md` | Public contracts → regression checks and reproducible instructions | Setup without full database |

Contracts:

- `Settings`: normalized category; `active_days` in {30, 90, 180}; nonnegative
  integer `min_episodes`; optional finite nonnegative `min_score` (`None` disables it).
- `SourceInfo`: mode, resolved path, identity `(path, size_bytes, mtime_ns)`, raw row
  count, schema notes, sorted distinct nonblank normalized categories from all raw
  rows. Category discovery precedes GUID reduction and user filters.
- `ScreeningResult`: nullable UTC `snapshot_date`, ordered stage counts defined in
  §4, all ranked eligible display rows plus internal `id`, GUID rows removed,
  raw future-timestamp row count, and deterministic quality warnings. Both
  executors return identical fields, values, missing semantics, and ordering.

Share pure scalar helpers only; SQL performs its own set transformations.

## 3. Data, environment, and execution

Dataset repository: `https://github.com/USC-DSO-576-PS/dataset_podcast-index`.
Read its README and `data_overview_podcast-index.md` (§§5–6); clone beside this
project if absent, using existing GitHub authorization. If access is denied,
report the required access rather than inventing data.

| Source | Default path relative to project root | Execution |
|---|---|---|
| Sample | `../dataset_podcast-index/sample/podcasts_sample.csv` | pandas; default even if full database exists |
| Optional full snapshot | `../dataset_podcast-index/data/podcastindex_feeds.db` | SQLite; about 4.7 million feeds |

Use Python 3.11+, Streamlit, pandas, pytest, and standard-library `sqlite3`.
Provide dependency declarations and these exact project-root commands in README:

```sh
python -m pip install -r requirements.txt
streamlit run app.py
pytest
```

Configure `PODCAST_SOURCE=sample|sqlite`, `PODCAST_SAMPLE_PATH`, and
`PODCAST_SQLITE_PATH`; resolve relative paths against the project, not the working
directory. Requested but absent SQLite falls back to sample with a visible notice.
Missing sample, invalid mode, or incompatible schema produces an actionable error.
Inspect SQLite tables/types and identify the table containing the required fields;
if multiple qualify, report ambiguity. Require `id`, `title`, `podcastGuid`,
`newestItemPubdate`, `language`, `category1`–`category8`, `episodeCount`, `host`,
`popularityScore`, and `explicit`. Reject missing, nonintegral, duplicate, or
out-of-signed-64-bit-range IDs after numeric parsing.

The full download is optional: follow the dataset README's `download_data.py` and
unpacking instructions (about 1.81 GB compressed, 5.06 GB unpacked, 8 GB free space
for download/unpacking, plus additional space for the derived cache). Never
fetch it automatically or modify the dataset repository.

### Data evidence and resulting choices

The overview (§§5–6) motivates the sentinel, category, language, GUID, and score
rules in §4. Recheck its snapshot-specific claims against the selected source.

A direct CSV inspection on 2026-10-18 found **6,000 rows, 40 columns, 6,000 unique
IDs, 312 zero `newestItemPubdate` values, 145 blank languages, one blank GUID,
and nine excess rows sharing nonblank trimmed GUIDs**. Categories 9 and 10 were
entirely blank; language examples included `en`, `en-us`, and `en-US`.
Sample SHA-256:
`14629adee2a6ff127fe24f8e6edbf3c4d9f69e3ee58b60bbe7dbf9501d6883c4`.
These are profiling counts, not screening expectations. Retaining episode/score
zero is product policy; it does not prove a measured zero.

### Storage and performance

Cache sample reads and source metadata by SourceInfo identity. For full mode,
build a rebuildable, gitignored local SQLite cache keyed by source identity,
rule version, and as-of date:

1. Read the source in read-only mode. Normalize required fields into an on-disk
   table using SQL and deterministic scalar functions where needed; store raw
   diagnostics, available categories, and the pre-reduction snapshot.
2. Materialize GUID-retained rows with a window function following §4. Store
   distinct `(feed_id, category)` pairs to avoid duplicate matches. Index the
   category lookup and retained language/timestamp fields for interactive queries.
3. Publish the completed cache atomically; coordinate concurrent builders and
   never reuse a partial cache. Open a separate owned connection per operation
   or session, closing it afterward; do not share unsafe connections.
4. Query counts and eligible rows from the prepared cache. Transfer only display
   columns plus `id` and aggregate metadata to the UI. Cache results by all
   Settings fields and the preparation key; retain no raw full-source DataFrame.

Use disk-backed SQLite temporary work and show preparation progress. Target
interactions within two seconds on the available laptop; measure cold preparation,
warm queries, rendering, and result sizes separately. Report unresolved delays.
All eligible rows remain available.

For later cloud use, publish the prepared tables as a versioned object-store
snapshot queried by a managed SQL service; replace the local adapter/executor
while preserving the contracts. Cloud deployment is outside this build.

## 4. Exact screening contract

Apply these rules in order, using one explicitly supplied UTC as-of **date** per
evaluation (the app captures today's UTC date once; tests pass a fixed date).

1. **Parsing.** Numeric parsing consumes the entire trimmed value, including
   scientific notation; blanks, nulls, nonnumeric values, NaN, and infinities are
   missing. Do not use SQLite's permissive `CAST` alone. Text nulls become empty
   strings; trim with Python Unicode whitespace semantics in both executors.
2. **Timestamps.** Interpret `newestItemPubdate` as Unix seconds. Accept only
   finite positive integral seconds through `253402300799` (9999-12-31 23:59:59
   UTC); other values are invalid. Use integer seconds internally and Python
   UTC datetime / ISO text for output, avoiding pandas nanosecond limits.
   In-range timestamps on a calendar date after the as-of date are also invalid;
   count these future rows in the raw source. Same-day nonmidnight times are valid.
3. **Snapshot/activity.** Before GUID reduction or user filters, snapshot is the
   maximum valid timestamp in the complete source. Activity is the inclusive
   interval `[snapshot - active_days * 86400, snapshot]`. With no valid timestamps,
   return null snapshot, no rows, zero post-load stage counts, and a warning;
   still report GUID removals and raw diagnostics.
4. **Language/categories.** Trim and lowercase language, then split before the
   first `-` or `_`; English means exactly `en`. Trim and lowercase each of the
   eight categories. Match if any equals the selected normalized category.
5. **Episode counts/scores.** Parsed negative values are missing; preserve zero
   and nonnegative decimals. Missing episodes act as zero for thresholds and
   tie-breaks but display as missing. Missing scores act as zero only for an
   enabled score threshold; display missing and rank after all numeric scores.
   There is no assumed score maximum. All threshold comparisons are inclusive.
6. **GUID reduction.** Trim GUIDs and compare case-sensitively. Retain every blank
   GUID row. For each nonblank GUID retain the latest valid timestamp (invalid
   last), then highest effective episode count, then smallest numeric ID.
   Apply this before eligibility filters; GUID removals = raw minus retained rows.
7. **Eligibility/ranking.** Retained rows must have a valid active timestamp,
   English, matching category, minimum episodes, and enabled score minimum.
   Order by score descending (missing last), effective episodes descending,
   trimmed title ascending (null title becomes empty), then numeric ID ascending.
   Use Unicode code-point ordering / SQLite UTF-8 BINARY collation for titles.

Compute these stages in the executors, never the UI:

| Stage | Count definition |
|---|---|
| Loaded feeds | All raw rows; equals SourceInfo row count |
| Valid latest-episode timestamp | GUID-retained rows with valid timestamps |
| Active English feeds | Previous stage within activity interval and English |
| Category-matching feeds | Previous stage matching any category field |
| Eligible feeds | Previous stage passing episode and enabled score thresholds |

Counts cannot increase; eligible count equals returned row count. GUID removals
are a separate diagnostic, not another stage. Raw future counts can overlap removals.

## 5. Starting view and presentation

| Control | Initial value |
|---|---|
| Category | `science` if available, otherwise first sorted category |
| Activity days | 90; choices 30/90/180 |
| Minimum episodes | 20; nonnegative integer |
| Enable minimum discovery score | Off; numeric field starts at 0 and accepts finite nonnegative values |

English is fixed. If categories are absent, disable screening and explain why.
Render the initial result without requiring extra configuration. Show, in order:

1. Source mode, raw count, UTC activity-reference snapshot, and any fallback notice.
2. Five attrition counts, then quality notes: GUID removals and collision risk,
   raw future count, invalid/missing-field summaries, and relevant schema warnings.
   GUID reduction is a heuristic that can remove genuine opportunities when
   unrelated shows share a GUID; it is not verified show deduplication.
3. All eligible rows in a sortable table: `title`, matching category (selected
   category once per row), normalized language, latest episode UTC datetime,
   `episodeCount`, `host`, `popularityScore`, `explicit`. Keep `id` internal;
   render missing values distinctly from zero. Client sorting changes neither
   eligibility nor counts. For no matches, preserve controls/counts and explain
   that the user can relax filters.
4. Explain snapshot-relative activity and lexicographic score/episode ordering.
   The score reflects Podcast Index API-client requests; `host` is the
   RSS-serving domain, not proof of ownership/network; language is not geography.
   Keep this limitation warning visible:

> Each result is a podcast feed, not necessarily a unique show. Categories and
> languages are publisher-provided metadata. popularityScore is a discovery
> signal, not listeners, downloads, revenue, rights, ownership, brand safety, or
> acquisition value. Every shortlisted feed requires audience, editorial,
> ownership, rights, financial, and brand-safety review.

## 6. Build order and acceptance

Build contracts/source inspection → pure pandas rules and fixture tests → sample
page → SQLite preparation/executor and equivalence tests → README and verification.
Keep raw data, archives, credentials, caches, and generated large files out of Git.

### Fixed fixture

Insert this same raw fixture into pandas and temporary SQLite. As-of date:
`2026-09-01`; Settings: science, 30 days, 20 episodes, score disabled. Dates below
mean midnight UTC converted to Unix seconds. Empty cells are actual empty strings;
unspecified categories are blank, host is `example.org`, explicit is 0.

| id | podcastGuid | title | newestItemPubdate | language | category1 | category8 | episodeCount | popularityScore |
|---|---|---|---|---|---|---|---|---|
| 1 | dup | Old | 2026-08-01 | en | science | | 50 | 9 |
| 2 | dup | Alpha | 2026-09-01 | en-US | science | | 20 | 5 |
| 3 | | Beta | 2026-08-02 | en_gb | | Science | 20 | 5 |
| 4 | | Beta | 2026-08-15 | en | science | | 20 | 5 |
| 5 | zero | Zero | 0 | en | science | | 20 | 5 |
| 6 | future | Future | 2026-09-02 | en | science | | 20 | 5 |
| 7 | french | French | 2026-08-15 | fr | science | | 20 | 5 |
| 8 | business | Business | 2026-08-15 | en | business | | 20 | 5 |
| 9 | short | Short | 2026-08-15 | en | science | | 19 | 5 |

Expected snapshot: `2026-09-01T00:00:00Z`; stages: **9 → 6 → 5 → 4 → 3**;
GUID removals: **1**; future rows: **1**; ranked IDs: **[2, 3, 4]**.
ID 3 tests the inclusive activity boundary and category8. Enabling score minimum
6 changes only the final count to zero.

Add focused equivalence cases for Unicode whitespace/case, repeated categories,
missing numbers versus zero, malformed/nonfinite/decimal numbers, invalid IDs,
invalid/absent/all-invalid timestamps, timestamp range limits and fractional
seconds, same-day nonmidnight times, GUID ties by episodes then ID, invalid dates
within GUID groups, and score/episode/title ranking (including non-ASCII titles).
Compare all result fields and warnings after canonical missing-value conversion.
Temporary SQLite tests are mandatory without the full snapshot; test cache reuse,
invalidation, and rebuilding after interrupted preparation as well.

### Completion evidence

- Run `pytest` and report outcomes, including executor equivalence.
- Start the sample app without a full database. Exercise defaults, all activity
  windows, two categories, zero minimum episodes, a high score threshold, and
  no-match behavior. Check visible warnings and counts against an independent
  sample calculation; compare several records to raw timestamps/categories/GUIDs
  and expected ranking. Report measured responsiveness.
- If a full snapshot exists, inspect its schema and record source identity,
  snapshot, Settings, counts, cold preparation, warm query, and rendering timings.
  Otherwise explicitly mark full-source integration/performance unverified.
- Inspect Git status/diff for unintended teammate changes or data. Hand off changed
  files, setup/run/test commands, check results, schema differences, and remaining
  limitations. Never claim an unrun check passed.
