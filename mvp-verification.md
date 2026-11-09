# Current MVP verification

Checked on November 8, 2026 against repository base commit ca2483e, in a fresh clone with a newly created uv environment. No sibling course environment, external data directory, or API key was used.

## Executed commands and results

Run from the team repository root, one command per line:

~~~text
uv sync --locked
uv run python validate_current_mvp.py
uv run pytest -q test_app.py test_mvp_validation.py
uv run python check_standalone.py
~~~

- Locked dependency installation succeeded.
- Independent CSV calculations matched current app calculations for 10 settings, including Sofía's two music screens, Sophie's Health screen, and the True Crime activity-window screens. Comparisons include all funnel counts, the complete ordered feed-ID list, and the snapshot. The hand-worked fixture passed.
- Combined regression test result: 13 passed in 15.26s.
- Bundled required files were present; Streamlit health and root requests both returned HTTP 200.
- The temporary Streamlit server was stopped and its port was confirmed closed.

validation-check-results.json records the CSV and app hashes, settings, counts, and ordered titles. validate_current_mvp.py computes its reference results with CSV and Python loops independently of the app's pandas transformations. It extracts the current calculation function definitions to compare with them without executing the UI.

test_mvp_validation.py supplements the existing root test with date and numeric boundaries, category8, language selection, explicit filtering, missing-value conversion, and an isolated Streamlit AppTest empty-result check.

## Limits

These checks support independent local operation from the bundled repository and selected calculation correctness. They do not establish public deployment parity, video quality, all browser behavior, performance under concurrent users, source accuracy, or whether case judgments are justified.

The oracle confirms input-order-sensitive first-occurrence GUID retention; it does not fix that limitation. The AppTest runs in an isolated process because the legacy root test imports the UI during collection and otherwise contaminates Streamlit runtime state. No app.py rule or product feature was modified for this verification.

The existing validation.md has not been rewritten by this commit. The team should incorporate relevant evidence from this record into the final report and export validation.pdf separately.
