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
