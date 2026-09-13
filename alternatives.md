# Alternatives: Riverside.fm localization and iHeartMedia content acquisition

## 1. Riverside.fm — multi-language creator workflows

### Decision question

Should Riverside.fm localize its creator-facing UI, and which language should be the first priority?

### Podcast Index evidence

This analysis uses Podcast Index feeds as a proxy for active creator supply. A feed was treated as active when its newest episode was published in the 90 days before the database's latest observed episode date, September 9, 2026. Recently launched feeds had an oldest observed episode date in 2025 or 2026. Regional language tags were combined and English was excluded.

| Language | Active launches, 2025 | Active launches, 2026 YTD | Annualized 2026 pace | Pace vs. 2025 |
|---|---:|---:|---:|---:|
| Spanish | 3,848 | 9,510 | 13,774 | 3.58x |
| Portuguese | 1,092 | 2,167 | 3,139 | 2.87x |
| French | 3,552 | 6,667 | 9,657 | 2.72x |
| Italian | 1,418 | 2,604 | 3,772 | 2.66x |
| Japanese | 2,587 | 4,152 | 6,014 | 2.32x |
| German | 5,183 | 6,967 | 10,091 | 1.95x |
| Chinese | 2,916 | 3,859 | 5,589 | 1.92x |

### Recommendation

Test **Spanish** first. It combines the largest pool of active, recently launched non-English feeds with the fastest growth among large language markets. French is a strong second candidate, and Portuguese is a high-growth follow-on candidate. German has meaningful scale but slower relative growth.

The database is a creator-activity signal, not a complete business case: it does not provide creator country, Riverside usage, willingness to pay, or audience size. Its oldest-episode date is not a guaranteed show-launch date.

### Information, people, and steps

**Information:** Podcast Index language trends; Riverside signup, activation, retention, paid-conversion, support-language, and geography data; customer interviews; translation and engineering costs; and legal, billing, privacy, and payment requirements.

**People:** Product management and analytics; localization specialists, translators, and native-language QA; design and user research; engineering and QA; growth, support, and sales; finance and legal/privacy.

**Steps:**

1. Shortlist Spanish, French, and Portuguese.
2. Segment Riverside's funnel by creator language and country.
3. Interview 8-12 creators in each priority language and test translated prototypes.
4. Set success measures: onboarding completion, first recording/export, 30-day retention, paid conversion, and support-contact rate.
5. Run a limited Spanish test for onboarding, core recording/editor controls, captions, and help content.
6. Compare it with an English control cohort, including translation and support costs.
7. Expand only if pre-agreed adoption, retention, and revenue thresholds are met.

**Google searches to validate the process:**

- `Riverside.fm supported languages interface localization captions help center`
- `Spanish speaking podcast creators growth 2025 2026 podcast market`
- `creator software localization onboarding conversion case study Spanish UI`

## 2. iHeartMedia — potential distribution partnerships

### Decision question

Which active podcasts should iHeartMedia investigate as potential distribution partners?

### Initial Podcast Index screen

Use the database to create an investigation queue, not to select partnership winners. A first-pass candidate should have published during the last 30 days, have at least 20 episodes, have no listed duplicate relationship, and show a higher Podcast Index discovery signal.

A successful query of the September 9, 2026 snapshot found 320,095 feeds active in the last 30 days. Applying the initial activity, durability, duplicate, and discovery screen produced 62,230 feeds. The largest category pools were business (7,580), religion (6,508), news (6,302), sports (6,177), society (5,390), and education (4,933).

`popularityScore` must not be treated as listening or downloads. It measures app and developer requests to Podcast Index, so it is useful only as a discovery signal.

### Information, people, and steps

**Information:** Publishing consistency; episode count; audience downloads, listeners, followers, growth, completion, demographics, and geography; ad inventory and CPM history; content quality and category fit; rights ownership, exclusivity, and existing distribution; deal economics; and brand-safety, copyright, and creator-reliability risks.

**People:** Content acquisition and partnerships; analytics; editorial programming and brand safety; ad sales and revenue operations; legal, business affairs, and finance; marketing and audience development; and the creator, producer, agent, or network representative.

**Steps:**

1. Screen for recently active, established shows with the database.
2. Rank the shortlist by strategic category and discovery signal.
3. Request verified audience, revenue, and rights information from creators or representatives.
4. Review recent episodes for quality, brand safety, and rights issues.
5. Model economics, including promotion and revenue-share terms, against alternatives.
6. Negotiate distribution scope, rights, exclusivity, promotion, and revenue share.
7. Start with a pilot or limited-term partnership.
8. Measure incremental reach, ad revenue, retention, and operational burden before renewal or expansion.

**Google searches to validate the process:**

- `iHeartMedia podcast distribution partnership submission requirements`
- `podcast distribution deal due diligence audience downloads revenue share`
- `podcast advertising brand safety content acquisition checklist`

## Source and limits

The database contains podcast feeds, not necessarily unique shows. Feed-level data supports activity and category screening but not final commercial decisions. The data dictionary and known limitations are documented in the Podcast Index dataset's `data_overview_podcast-index.md`.
