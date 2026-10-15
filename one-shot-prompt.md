# Podcast Opportunity Explorer — One-Shot Build Prompt

Build a runnable local Streamlit prototype from this file and the dataset
repository alone. Inspect the existing project before editing; preserve
unrelated teammate work. This entire Markdown file is the build request.

## 1. Vision and scope

**User and decision.** An iHeartMedia content-acquisition manager has a content
category gap and limited time to investigate podcasts. The tool helps decide
which feeds to research first using publishing recency, episode history, and a
Podcast Index discovery signal. It produces one transparent research queue;
it does not estimate audience, acquisition value, or partnership availability.

**Why it helps.** Manual directory searches and unstructured suggestions make
consistent screening difficult. Explicit filters and attrition counts show
which feeds remain and why, while the table supports comparison of the three
metadata measures without combining them into a commercial score.

| Use case: user selects | Tool shows | Decision supported |
|---|---|---|
| Science, 90 days, at least 20 episodes | Attrition and eligible ranked feeds | Which feeds merit editorial review and external audience research |
| Business, 30 days, a higher episode minimum | Smaller pool and stage counts | Whether to relax criteria or investigate the remaining feeds |
| A category and an enabled minimum discovery score | Eligible feeds ordered by the rules below | Which feeds merit initial due diligence based on this limited signal |

Build only the single “Acquisition screen” page. Exclude maps, exports,
feed-profile pages, localization tools, outreach automation, composite scores,
and deal recommendations. Leave styling and nonessential wording to the agent.

## 2. Design principles and pieces

- **One rule contract, two execution paths.** A pure pandas implementation is
  the reference for the sample; a SQL implementation handles the full source.
  Identical fixture tests prevent source choice from changing the rules.
- **Filter large data where it lives.** Execute full-source normalization,
  deduplication, filtering, counts, and ranking in SQLite so millions of rows
  never enter pandas or Streamlit memory.
- **Separate presentation, rules, and source access.** The UI renders results;
  adapters manage I/O; screening implementations own transformations. This
  lets each piece be built and checked independently.
- **Show uncertainty.** Feed metadata supports an investigation queue, not
  verified commercial claims. Display missing values and quality notes.
- **Start with the sample.** A missing full database must never block startup.

```text
app controls → source adapter → pandas or SQLite screening → ScreeningResult → app
                                  same rules and output contract
```

Suggested files and public contracts (adapt names to existing code):

| Piece | Receives | Returns / responsibility | Independent check |
|---|---|---|---|
| `src/contracts.py` | Plain values | Shared Settings and ScreeningResult definitions below | Structures import without Streamlit or I/O |
| `src/load_data.py` | Source mode and paths | SourceInfo: mode, path, source identity, raw row count, schema notes, sorted available categories; reads sample or opens read-only SQLite | Missing-file fallback and actionable schema errors |
| `src/screening.py` | Sample DataFrame, Settings, explicit UTC as-of date | ScreeningResult using pure transformations; no files, widgets, or session state | Invented-table expected results |
| `src/sql_screening.py` | Read-only connection, Settings, same as-of date | ScreeningResult using equivalent SQL; no widgets | Same fixture inserted into temporary SQLite |
| `app.py` | Widgets and source/results contracts | Selects execution path and renders the page; no duplicate screening logic | Sample startup and empty-state smoke check |
| `tests/`, `README.md` | Public contracts and setup commands | Regression checks and reproducible run instructions | Works without the downloaded database |

`Settings`: normalized category, active_days (30/90/180), nonnegative integer
min_episodes, and optional nonnegative min_score (`None` means disabled).

`ScreeningResult`: snapshot_date (nullable UTC timestamp), ordered stage counts,
all ranked eligible display rows, GUID rows removed, future-timestamp rows
excluded, and quality warnings. SourceInfo supplies source context separately.
The two screening implementations return the same fields and meanings. Keep
SQL-specific transformations in the SQL implementation rather than asking the
pure pandas function to process an already screened SQL result.

## 3. Data, environment, and scale

Dataset repository: `https://github.com/USC-DSO-576-PS/dataset_podcast-index`.
Clone it beside this project if absent; private-repository access requires the
user's existing GitHub authorization. Read its README and data overview.

| Source | Path relative to project root | Use |
|---|---|---|
| Default sample | `../dataset_podcast-index/sample/podcasts_sample.csv` | Tracked 6,000-row CSV; pandas development and startup path |
| Optional full snapshot | `../dataset_podcast-index/data/podcastindex_feeds.db` | About 4.7 million feeds; SQLite execution path |

Use Python 3.11+ with Streamlit, pandas, and pytest; `sqlite3` is standard
library. Supply dependency declarations and exact README commands, including
`python -m pip install -r requirements.txt` (or the equivalent for an existing
project environment), `streamlit run app.py`, and `pytest` from the project root.
Resolve source paths against the project location rather than the working
folder. Allow source selection via configuration or environment variables;
default to sample even if SQLite exists. If requested SQLite is absent, fall
back to sample with a visible message; a missing sample or incompatible schema
must produce an actionable error.

The dataset script `download_data.py` downloads an approximately 1.81 GB archive;
follow the dataset README to unpack the approximately 5.06 GB database. Explain
that about 8 GB free disk space is needed and the sample is sufficient. Do not
download the full source automatically or modify the dataset repository.

Inspect SQLite table names and column types rather than assuming its schema.
Required fields: `id`, `title`, `podcastGuid`, `newestItemPubdate`, `language`,
`category1`–`category8`, `episodeCount`, `host`, `popularityScore`, and `explicit`.
Validate unique numeric `id` values for deterministic tie-breaks. Actual missing
values include empty strings and numeric zeros; checking SQL NULL alone is
insufficient. Categories 9 and 10 are unused in the documented snapshot.

Cache sample reads and source metadata by resolved path, file size, and
modification time. Reuse read-only SQLite access only with safe connection
ownership; never share an unsafe connection between sessions. Cache stable SQL
preparation or use a rebuildable, gitignored normalized local SQLite cache if
needed to avoid redoing full-source normalization and GUID sorting on every
interaction. Key derived data by source identity, rule version, and as-of date;
never write to the original snapshot. Cache filtered results only with all
settings and these identity keys. Return only display columns and counts to the
UI; do not copy the raw database into pandas. Measure and report cold preparation
and warm filter latency on the available laptop; identify any unresolved delays.

For later cloud use, replace the local source adapter/executor with a managed
query service or prepared object-store snapshot while preserving the settings
and result contracts. Deployment is outside this local deliverable.

## 4. Exact screening rules

A source row is a crawled RSS/Atom feed, not necessarily a unique show. Apply
these rules in both implementations:

1. **Timestamps.** Parse `newestItemPubdate` as Unix seconds in UTC. Blank,
   missing, nonnumeric, nonpositive, or unrepresentable values are invalid.
   Timestamps whose UTC calendar date is after the supplied as-of UTC date are
   also invalid. Report the number of these future rows in the raw source.
   Capture the as-of date once per evaluation; tests pass it explicitly.
2. **Snapshot and activity.** Before deduplication or user filters,
   `snapshot_date` is the maximum valid timestamp in the complete selected
   source; it is an activity reference, not a verified export date. An active
   feed has a valid timestamp in the inclusive interval
   `[snapshot_date - active_days × 24 hours, snapshot_date]`. If none are valid,
   return no eligible rows, zero post-load stage counts, a null snapshot date,
   and a clear warning.
3. **Language and categories.** Trim and lowercase language, then take the part
   before the first `-` or `_`; English means exactly `en`. Trim and lowercase
   all eight category fields; ignore blanks. A feed matches if any field equals
   the selected normalized category. Build the category selector from the
   sorted distinct nonblank categories in the complete source.
4. **Numbers.** Parse episode counts and discovery scores numerically. Blank,
   missing, nonnumeric, or negative values are missing; preserve stored zero.
   Missing episode counts act as zero for the minimum screen and deduplication
   tie-break but display as missing. Missing discovery scores act as zero only
   for an enabled minimum-score screen; display them as missing and sort them
   after numeric scores. Do not impose an assumed maximum discovery score.
5. **GUID reduction.** Trim `podcastGuid`; treat null or whitespace-only values
   as blank and otherwise compare case-sensitively. Before screening filters,
   retain one row per nonblank GUID: latest valid timestamp first (invalid last),
   then largest effective episode count, then smallest numeric `id`. Retain all
   blank-GUID rows. Report raw rows minus retained rows as GUID rows removed.
   This is a screening heuristic, not verified show deduplication: the dataset
   overview warns that unrelated shows can share GUIDs, so this rule can remove
   genuine opportunities. Disclose that risk in the data-quality notes.
6. **Eligibility.** On retained rows, require valid timestamp, activity,
   normalized English, category match, minimum episodes, and an optional
   minimum discovery score. Threshold comparisons are inclusive.
7. **Ranking.** Sort eligible rows by numeric `popularityScore` descending
   (missing last), effective `episodeCount` descending, trimmed `title`
   ascending using case-sensitive Unicode ordering, then numeric `id` ascending.
   Use matching pandas/SQLite text collation. No composite score.

Attrition contract; compute it in the screening implementations, never the UI:

| Display stage | Definition |
|---|---|
| Loaded feeds | All raw source rows, before GUID reduction; equals SourceInfo row count |
| Valid latest-episode timestamp | Retained rows with valid timestamps |
| Active English feeds | Previous stage inside the activity interval and normalized English |
| Category-matching feeds | Previous stage matching any of the eight category fields |
| Eligible feeds | Previous stage meeting episode and enabled score thresholds |

Counts cannot increase; eligible count equals the number of returned table
rows. Show GUID removals separately, not as an extra attrition stage. Future
row counts are raw-source quality diagnostics and can overlap GUID removals.

## 5. Starting view and presentation

Controls: one category (default `science` if present, otherwise first sorted
category); activity 30/90/180 days (default 90); nonnegative integer minimum
episodes (default 20); optional nonnegative discovery-score minimum (disabled
by default, initial numeric value 0). If no categories exist, disable screening
and explain why. English is fixed for this product, not another control.

Show in order:

1. Source mode, raw row count, and UTC activity-reference snapshot date.
2. The five attrition stages above, plus separate data-quality notes.
3. A ranked, sortable table: `title`, matching category, normalized language,
   UTC latest episode date, `episodeCount`, `host`, `popularityScore`, `explicit`.
   Retain `id` internally for checks. A single-category selection displays that
   category once per matching row. Show all eligible rows; client sorting may
   change the displayed order but not eligibility or counts. For no matches,
   preserve counts and controls and show a clear empty-state message.
4. A short explanation of snapshot-relative activity, score ordering, and the
   following visible limitations warning:

> Each result is a podcast feed, not necessarily a unique show. Categories and
> languages are publisher-provided metadata. popularityScore is a discovery
> signal, not listeners, downloads, revenue, rights, ownership, brand safety, or
> acquisition value. Every shortlisted feed requires audience, editorial,
> ownership, rights, financial, and brand-safety review.

Also explain that `host` is the RSS-serving domain, not proof of ownership or
network affiliation; language does not establish creator geography. The score
reflects requests from Podcast Index API clients, not audience measurement.

## 6. Build order and independent acceptance checks

Build contracts and source inspection first; implement pure screening and its
fixture tests; wire the sample page; implement SQLite screening with equivalence
tests; finish README and verification. Keep raw data, archives, credentials, and
large generated files out of Git.

### Fixed fixture with expected results

Use the following complete fixture in both pandas and temporary SQLite tests.
As-of date is `2026-09-01`; settings are `science`, 30 days, 20 episodes, no score
minimum. Dates mean midnight UTC converted to Unix seconds. All unspecified
categories are blank; host and explicit may use constant valid values.

| id | podcastGuid | title | newestItemPubdate | language | category1 | category8 | episodeCount | popularityScore |
|---|---|---|---|---|---|---|---|---|
| 1 | dup | Old | 2026-08-01 | en | science | | 50 | 9 |
| 2 | dup | Alpha | 2026-09-01 | en-US | science | | 20 | 5 |
| 3 | blank | Beta | 2026-08-02 | en_gb | | Science | 20 | 5 |
| 4 | blank | Beta | 2026-08-15 | en | science | | 20 | 5 |
| 5 | zero | Zero | 0 | en | science | | 20 | 5 |
| 6 | future | Future | 2026-09-02 | en | science | | 20 | 5 |
| 7 | french | French | 2026-08-15 | fr | science | | 20 | 5 |
| 8 | business | Business | 2026-08-15 | en | business | | 20 | 5 |
| 9 | short | Short | 2026-08-15 | en | science | | 19 | 5 |

`blank` in this table means an actual empty string, not the literal word.
Expected: snapshot `2026-09-01T00:00:00Z`; stage counts
`9 → 6 → 5 → 4 → 3`; GUID removals `1`; future rows `1`; ranked ids `[2, 3, 4]`.
Id 3 tests both the inclusive 30-day boundary and category8. Enabling minimum
score 6 changes only the final count to zero.

Add focused cases for whitespace normalization, missing numbers and stored zero,
invalid/absent timestamps, all timestamps invalid, same-day nonmidnight dates,
GUID ties by episode count then id, invalid timestamps within a GUID group, and
score/episode ranking differences. Both implementations must agree on all
result fields, missing-value semantics, counts, and row order. Temporary SQLite
tests are mandatory even when the full snapshot is unavailable.

### Completion evidence

- Run `pytest`; report outcomes, including pandas/SQLite equivalence.
- Start the app against the sample with no full database. Exercise all three
  activity windows, two available categories, zero episode threshold, a high
  score threshold, and no-match behavior. Verify defaults, warning visibility,
  and counts against an independent sample calculation.
- Manually compare several displayed records with source timestamps,
  categories, GUIDs, and ranking. Report measured sample responsiveness.
- If the full snapshot is available, verify schema, run a screen, and record
  source identity, snapshot date, settings, stage counts, and cold/warm timings.
  If unavailable, explicitly report full-source integration/performance as
  unverified; fixture equivalence is still required.
- Inspect `git status` and staged changes for unintended data or teammate edits.
- Hand off changed files, exact setup/run/test commands, check results, measured
  limitations, and schema differences. Never claim a check passed if not run.

Before submitting this prompt, the team should give this file and the dataset
repository to a fresh agent and record any important question or guess as a gap
to resolve. A completed prototype or a successful fresh-agent build must not be
claimed solely because this specification has been reviewed.
