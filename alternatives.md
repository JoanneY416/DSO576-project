# Riverside.fm: UI localization alternatives

## Decision question

Should Riverside.fm build a multi-language UI localization feature for creator workflows, and if so, which language should be first?

## Evidence from the Podcast Index data

I used the local Podcast Index SQLite database as a proxy for active creator supply.

- **Active today** means a feed published a newest episode during the 90 days before the database's latest observed episode date, September 9, 2026.
- **Recently launched** means its oldest observed episode was published in 2025 or 2026.
- Regional language tags were combined; for example, `pt-BR` was counted as Portuguese. English was excluded.

| Language | Active launches, 2025 | Active launches, 2026 YTD | Annualized 2026 pace | Pace vs. 2025 |
|---|---:|---:|---:|---:|
| Spanish | 3,848 | 9,510 | 13,774 | 3.58x |
| Portuguese | 1,092 | 2,167 | 3,139 | 2.87x |
| French | 3,552 | 6,667 | 9,657 | 2.72x |
| Italian | 1,418 | 2,604 | 3,772 | 2.66x |
| Japanese | 2,587 | 4,152 | 6,014 | 2.32x |
| German | 5,183 | 6,967 | 10,091 | 1.95x |
| Chinese | 2,916 | 3,859 | 5,589 | 1.92x |

## Initial recommendation

Prioritize **Spanish** for the first localization test. It has both the largest active, recently launched non-English creator pool and the fastest growth among the large language markets. French is a strong second candidate because of its large and fast-growing pool; Portuguese is a high-growth follow-on candidate. German has substantial scale but slower relative growth, suggesting a more mature market.

This is a creator-activity signal, not a complete business case. The data contains feeds and language, rather than creator location, Riverside usage, willingness to pay, or audience size. `oldestItemPubdate` is also an observed earliest episode date, not a guaranteed launch date.

## Information to use

- Podcast Index trends in recently launched and currently active feeds by language.
- Riverside's signup, activation, retention, paid-conversion, support-language, and creator-geography data.
- Customer interviews and usability testing with creators in the priority language markets.
- Estimated revenue opportunity, translation and vendor costs, engineering complexity, QA needs, and ongoing translation maintenance.
- Country-specific billing, legal, privacy, and payment requirements.

## People to involve

- Product manager and product analyst
- Localization lead, translators, and native-language QA testers
- Product design and user research
- Engineering and QA
- Growth marketing, customer support, and sales
- Finance and legal/privacy partners

## Proposed steps

1. Use the data above to shortlist Spanish, French, and Portuguese.
2. Segment Riverside's own funnel by creator language and country to quantify demand and friction.
3. Interview 8-12 creators in each priority language and test translated workflow prototypes.
4. Agree on success metrics: onboarding completion, first recording, first export, 30-day retention, paid conversion, and support-contact rate.
5. Run a limited Spanish experiment covering onboarding, core recording/editor controls, captions, and help-center content.
6. Compare the localized cohort with a comparable English-control cohort, including translation and support costs.
7. Expand only if the experiment clears pre-agreed adoption, retention, and revenue thresholds; otherwise address the largest workflow friction or test the next language.

## Searches to validate the approach

- `Riverside.fm supported languages interface localization captions help center`
- `Spanish speaking podcast creators growth 2025 2026 podcast market`
- `creator software localization onboarding conversion case study Spanish UI`

