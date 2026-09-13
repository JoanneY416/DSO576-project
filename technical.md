# Podcast Index data acquisition record

Downloaded and validated on 2026-09-13. The downloaded files are stored locally in
`dataset_podcast-index/data/`, which is ignored by Git. They are not stored in this
shared repository.

## Resulting files

| Filename | Format | Approximate size | Opened successfully? |
|---|---|---:|---|
| `podcastindex_feeds.db.tgz` | gzip-compressed tar archive | 1.83 GB (1.70 GiB; 1,826,623,856 bytes) | Yes. `tar` listed one complete member named `podcastindex_feeds.db`. |
| `podcastindex_feeds.db` | SQLite 3 database | 5.09 GB (4.74 GiB; 5,094,928,384 bytes) | Yes. It opened read-only with SQLite, and `PRAGMA quick_check` returned `ok`. |

## Database opening results

- The database contains one table, `podcasts`.
- The table contains 4,728,574 rows and 42 columns.
- The current database has two columns not present in the repository's 40-column
  sample: `podcastId` and `duplicateOf`.

## Problems and differences from the overview

- The provided `download_data.py --check` command failed locally with
  `SSL: CERTIFICATE_VERIFY_FAILED`. The same official URL worked with the system
  `curl` client and a browser user-agent, returning HTTP 200.
- The publisher replaces the file at a fixed URL. This snapshot was last modified
  on 2026-09-12 at 23:24:31 GMT and is newer than the snapshot described in the
  overview.
- The downloaded archive is about 18.9 MB larger and the extracted database about
  36.7 MB larger than the overview's figures. It also has 4,538 more rows and two
  more columns.
- The archive SHA-256 is
  `67228f5c15596ad313120a632eb9c8ab0119231350c7f601ddc75da2af00be6d`, so it
  differs from the older checksum embedded in the download script. The matching
  HTTP content length, successful tar read, successful SQLite queries, and `ok`
  integrity result indicate that this is version drift rather than a truncated or
  corrupt download.
- About 6.4 GiB of disk space remained after retaining both files. Deleting the
  archive later would recover about 1.7 GiB, but it was kept for now.

## Team next steps

1. **Choose the decision before choosing the technology.** Agree on one named
   stakeholder, one decision that person must make, and the small set of metrics
   needed to support it. Document what the dataset cannot answer, especially
   listener counts, downloads, revenue, geography, and episode-level behavior.
2. **Assign responsibilities.** Name an owner for the decision statement, data
   quality checks, SQL analysis, and the eventual interface. One teammate should
   maintain the full local database; everyone else can begin with the sample.
3. **Create a reproducible data audit.** Write version-controlled SQL or Python
   that checks `id` and `url` uniqueness, empty-string and zero sentinels, timestamp
   ranges, repeated `podcastGuid` values, `duplicateOf`, and differences between
   the 40-column sample and 42-column current database. Do not commit raw data.
4. **Prototype with the sample, validate with the full database.** Use
   `sample/podcasts_sample.csv` to develop queries and charts quickly, but calculate
   every final count, rate, ranking, and recommendation from
   `podcastindex_feeds.db`. Filter and aggregate in SQL rather than loading the
   entire database into Python memory.
5. **Save small derived outputs.** Export only compact, reproducible aggregate
   tables needed by the project. Record the source snapshot date, metric
   definitions, filters, row counts, and the command or script that created each
   output.
6. **Build the simplest useful interface.** Start with SQL and Python. Add a local
   Streamlit dashboard only after the metrics are validated. The app should read
   small derived tables rather than the 5.09 GB raw database.
7. **Add cloud services only for a demonstrated need.** If the team needs a shared
   queryable backend, choose either Supabase/PostgreSQL or Google Cloud SQL, not
   both, and load curated tables rather than the raw dump. Use Google Cloud Storage
   only if shared storage for source snapshots is required, and Cloud Run only
   when the Streamlit app is ready to deploy.
8. **Treat Gemini as optional.** Consider it only for a clearly testable text task,
   such as classifying descriptions. Require structured results, compare them with
   a human-labeled test set, preserve the original text, and keep AI-generated
   labels separate from publisher-provided fields.
9. **Use safe Git practices.** Work in short branches, review changes through pull
   requests, stage named files instead of `git add .`, and check staged paths before
   every commit. Never commit `data/`, `downloads/`, credentials, API keys, or
   local environment files.

### Next team checkpoint

The next meeting should end with an approved stakeholder and decision, written
metric definitions, assigned owners, and one sample-based query or chart that can
later be rerun against the full database. Do not select a cloud platform or add
Gemini until those four items are complete.
