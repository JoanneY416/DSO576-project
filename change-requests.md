# Change requests

Our team's log of what we found and what should change, kept in the top folder of our team repo
from Module 9 to Module 13. Pull before you edit it and push soon after.

- For each finding, copy the request template below to the end of this file, give it the next
  number and fill in every field.
- Never delete a request. When it is built, set its status to `built` with the commit; when the
  team decides against it, `declined` with the reason.
- When this file gets long, ask Codex to move the built and declined requests into a dated file
  in `change-requests-archive/` (for example `change-requests-archive/2026-11-02.md`) and leave
  only the open ones here. Numbers continue; never reuse one.

Request template:

```markdown
### CR-NN: short title

- **From:** name, YYYY-MM-DD
- **Part:** the feature, number or function
- **Evidence:** what you did and saw: the input, what you expected, what the tool gave
- **Change:** what should change, in a sentence or two
- **Priority:** high, medium or low
- **Status:** open
```

A filled request (from the class lottery app):

```markdown
### CR-01: chance above 100% with two slots

- **From:** Ana, 2026-10-21
- **Part:** `odds` (the chance of selection by wage level)
- **Evidence:** one person at Level I and one at Level IV, two slots. Both must be selected,
  so each chance is 1. `odds` gave 0.4 and 1.6.
- **Change:** select each person at most once (without replacement), so no chance passes 1.
- **Priority:** high
- **Status:** open
```

## Requests

<!-- Add new requests below this comment, at the end of the file, newest last. -->
```markdown
### CR-01: Add podcast audience and engagement metrics

- **From:** Esther, 2026-10-23
- **Part:** Part 1 — Screening Funnel
- **Evidence:** I selected the Travel category with a 90-day activity window and a minimum of 20 episodes. The app showed 2 eligible feeds out of 6,000 sampled feeds, but the funnel did not provide audience or engagement information to help evaluate their acquisition potential
- **Change:** Add audience size, engagement, and growth metrics for eligible podcasts so managers can better identify promising acquisition opportunities
- **Priority:** medium
- **Status:** open
```

```markdown
### CR-02: Explain why podcast feeds are excluded

- **From:** Esther, 2026-10-23
- **Part:** Parts 1 and 2 — Screening Funnel and Eligible Feeds
- **Evidence:** The app displayed 2 eligible Travel feeds, and my independent Python calculation confirmed the same result. However, the funnel does not show which individual feeds were excluded or why
- **Change:** Add a table of excluded feeds with the specific screening criteria they failed. This would help managers understand the results and decide whether to adjust their filters
- **Priority:** medium
- **Status:** open
```
### CR-03: Preview discovery-score threshold impact

- **From:** Fidelia Gan, 2026-10-25
- **Part:** Minimum discovery-score filter and eligible-feed ranking
- **Evidence:** With science, 90 active days, and at least 20 episodes, the app returned 12 feeds with the score filter disabled, 9 at a minimum score of 2, 3 at 5, and 1 at 9. The control showed no score distribution or preview of how many feeds each threshold would remove
- **Change:** Show the discovery-score distribution for the current candidate pool and preview the remaining feed count before applying a threshold. Explain that the score is an API-request discovery signal and offer observed-value or percentile-based threshold choices instead of an unconstrained precision input alone
- **Priority:** high
- **Status:** open

### CR-04: Add funnel retention rates and an auditable count definition

- **From:** Fidelia Gan, 2026-10-25
- **Part:** Active English feeds number in the screening funnel
- **Evidence:** The app displayed 315 active English feeds. My independent script reproduced 315 after 9 GUID removals and 5,680 valid retained timestamps, but the manager must manually infer that 315 is 5.5% of valid retained feeds and is a sample count measured from the source snapshot rather than today
- **Change:** Add retention percentages between funnel stages and an expandable calculation summary for each count showing its denominator, snapshot, activity interval, and normalization/deduplication assumptions. This should provide aggregate calculation context without presenting the sample count as a population estimate
- **Priority:** medium
- **Status:** open
