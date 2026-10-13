# My design analysis

**Individual.** Write in this file and upload it to **Brightspace → Hand In
Work** before Quiz 8 (the time is on `/hw`); your team's `one-shot-prompt.md`
is uploaded separately, by one member. Graded on effort. Three parts:
**Part 1** the vision and **Part 2** your design analysis (homework before the
module's second class, handout 8.3), then **Part 3** your one improvement to
the team's draft (handout 8.8). Full instructions: handout 8.3, 8.8 and
*What to hand in*.

<!--
  How to fill it in:
  1. Replace every line that says "Paste ... here" or "Write ... here",
     including inside the boxes. Keep the headings and these comments.
  2. Parts 2 and 3 must be your own work. Codex can look things up and
     question you, but the answers are yours.
  3. Part 3 must differ from every teammate's improvement. Claim your change
     before you make it: tell or email your teammates which change you are
     taking (handout 8.8).
-->

## Part 1. The vision (handout 8.3)

Your team's `00-vision.md`, pasted.

<!-- Paste your team's 00-vision.md inside the box below, between the two
     lines of four backticks. If your team has not agreed on a vision yet,
     paste the vision you would propose. -->

````text
# Our Vision: Podcast Opportunity Explorer

We envision an auditable, decision-support tool that turns the open podcast
ecosystem into clear, responsible next steps for media teams. Rather than
presenting a directory or an unsupported ranking, the Podcast Opportunity
Explorer helps leaders identify where to investigate: which languages offer
promising creator supply for a localized Riverside experience, and which
podcast feeds deserve deeper iHeartMedia acquisition research.

The product has two focused workspaces. The localization workspace helps
Riverside assess language opportunities using transparent definitions of
activity, coverage, episode history, and category trends. The acquisition
workspace helps iHeartMedia narrow a large catalog into a review queue using
categories, language, recency, episode volume, duplicate exclusion, and
discovery signals. Each result is accompanied by its filters, data coverage,
missingness, duplicate rules, and suggested follow-up.

Our aim is to make scarce research, product, and business-development capacity
go further. The explorer should be inexpensive, reproducible, and explainable:
it reduces millions of crawled feed records to defensible hypotheses and
shortlists while preserving the uncertainty inherent in the data.

We are deliberate about its boundaries. Feed metadata and discovery scores are
screening signals—not proof of customer demand, audience size, revenue,
ownership, rights, brand safety, or partnership interest. Final decisions
remain grounded in governed analytics, verified audience and commercial data,
editorial review, creator conversations, and responsible experimentation.

In short, we want to build a bridge from open ecosystem data to better,
evidence-led business decisions: a tool that makes both its recommendations
and its limitations visible.
````

## Part 2. My design analysis (handout 8.3)

Your own answers to the four design questions of handout 8.2 for your
project, and your open questions.

<!-- Answer on your own, before the module's second class, for the vision in
     Part 1. A few sentences or a short list per question is enough. Use the
     trade-off tables of handout 8.4: for each question, say which option fits
     your project and why, or describe a better one. These answers are what
     your team compares when it agrees on the design (handout 8.5). -->

### 2a. Clear pieces

<!-- What are the pieces of your tool, one job each? For each, one line: what
     it receives and what it returns. Which option of 8.4 question 1 fits, and
     why? -->

I would use **one piece per job (separation of concerns)**. The prototype has
four clear pieces, each with a small contract that can be built and checked
alone:

- **Source loader:** receives the selected source and its paths, validates the
  CSV or SQLite schema, and returns source metadata plus only the feed fields
  needed for screening.
- **Screening logic:** receives feed records and plain filter settings
  (category, active-days window, minimum episodes, and optional discovery-score
  threshold); it returns a `ScreeningResult` with attrition counts, ranked rows,
  snapshot date, and data-quality notes.
- **Streamlit page:** receives widget values and the loader/screening outputs;
  it renders controls, source context, limitations, and the investigation queue
  without defining the business rules again.
- **Tests and setup documentation:** receive the public screening functions and
  run commands; they return repeatable checks and instructions for teammates.

This option is a better fit than one top-to-bottom script because our app must
support both a small CSV sample and a 4.7-million-row SQLite snapshot while
applying identical rules. The separation costs a few more files and clear
agreements about what each piece passes on, but it lets us unit-test the
consequential screening rules on a tiny invented table and change the user
interface without accidentally changing the recommendation queue.

### 2b. Simple connections

<!-- What must each piece never touch (the screen, the files, another piece's
     internals)? Which piece is the only one that opens the data files? Which
     option of 8.4 question 2 fits, and why? -->

I would use the **“each view has a contract”** option. The connections should
be one-way: source loader → screening logic → Streamlit page.

- The **source loader** receives a source choice, paths, and safe SQL filter
  inputs; it returns source metadata and the needed feed columns. It must never
  create widgets, render a chart, or decide which feeds are eligible.
- The **screening module** receives a DataFrame (or an equivalent SQL result)
  and a plain settings object; it returns the ranked display rows, attrition
  counts, snapshot date, and data-quality notes. It must never open CSV or
  SQLite files, read sidebar widgets, use Streamlit session state, or render a
  view.
- The **Streamlit page** receives widget values plus the loader and screening
  outputs; it returns the visible table, counts, explanations, and empty
  states to the user. It must never contain a second copy of normalization,
  deduplication, screening, or ranking rules.

The loader is the only piece that opens data files. Keeping views dependent on
prepared DataFrames/results rather than on the sidebar or source files lets us
test calculations with a tiny invented table, reuse them for both CSV and
SQLite, and cache source reads safely. The cost is that the dashboard must pass
the required rows and settings into each function, but that contract is clearer
and safer than allowing every chart to reach into the data and sidebar itself.

### 2c. Local changes

<!-- What will the user change on screen? What will your team likely change
     later (a setting, a definition, one more view or data source)? Where should
     each live so that it changes in one place? Which option of 8.4 question 3
     fits, and why? -->

For this small, single-page prototype, I would choose **settings typed in the
code with one conditional branch per view**, rather than a TOML plug-in family.
The user changes the category, activity window, minimum episode count, and
optional minimum discovery score on screen. Those values should be collected in
`app.py` and passed together as one plain settings object to the screening
module; they should not be repeated in charts or tables.

The team is more likely to change screening definitions later: accepted English
language labels, the active-feed calculation, duplicate handling, ranking
tie-breakers, source paths, or the visible list of categories. Each definition
should live once in `src/screening.py` (and source paths/schema requirements in
`src/load_data.py`), with tests beside the screening rules. The page should
only display those rules and their results. If a localization workspace or
additional source is added later, it can be a separate page or module with the
same screening contract instead of copying code into the current view.

The TOML-and-class option would be valuable for many independently configured
views or saved setups, but it adds structure that this assignment does not yet
need. Keeping settings centralized in a small Python settings object makes a
definition change a one-place edit while retaining a simple runnable app.

### 2d. Real-world operation

<!-- How big is your data, in rows and megabytes, and where did you find
     that (a file in your dataset repo, or a query you ran)? What is
     prepared once ahead of time, what is loaded when the tool starts, and what
     is computed on each click? What must be in memory? What does the tool keep
     between visits ("nothing" is fine)? Which option of 8.4 question 4 fits,
     and why? -->

I would choose **prepare once; load only the chosen rows; cache results**. Our
full Podcast Index SQLite snapshot contains about **4,728,574 feed rows and 42
fields**, as recorded in the project vision. That is too large to load into a
DataFrame at application start on every run, and the exact database file size
should be recorded after inspecting the local snapshot. The tracked CSV sample
is small enough to load directly and is the default development path.

Ahead of time, we should record the snapshot date and checksum, inspect the
SQLite schema, and prepare or validate the SQL needed for normalization,
deduplication, filtering, counts, and ranking. When the app starts, it loads
only source metadata and the CSV sample when that source is selected. For the
full source, each changed filter setting triggers SQL that performs as much
filtering, deduplication, aggregation, and ranking as practical in SQLite, then
returns only the attrition counts and display rows required by the page.

The app should keep only the small CSV sample or the current filtered result in
memory—not all 4.7 million rows. It can cache source/schema checks and repeated
source reads, but must not cache a result without including the user’s filter
settings in the cache key. Nothing needs to persist between visits beyond the
local source files; reproducible saved outputs can be created deliberately,
rather than silently retaining a user’s previous queue. This design may pause
when filters change, but it is memory-safe and preserves logically equivalent
rules for the CSV and SQLite paths.

### 2e. Open questions

<!-- What do you not know yet that the design depends on, and how would you
     find out (for example, a query on the data, or a question for the team)? -->

Which language variants should count as English—for example, `en`, `en-US`,
`en_gb`, differently capitalized values, or blank values? This decision affects
which feeds enter the investigation queue, so we should profile the actual
`language` field in both the CSV sample and full SQLite snapshot: count each
distinct normalized value, inspect a few representative records, and agree on
one documented normalization rule. That rule should then live once in the
screening module, with unit tests for accepted English variants and for blanks
or unsupported values.

## Part 3. My improvement to the draft prompt (handout 8.8)

One significant change you made to the team's `one-shot-prompt.md`: before,
after, and your argument for why it is better.

**What I improved, in one sentence:** Write it here, naming the section of
`one-shot-prompt.md` it changes.

### 3a. Before

<!-- The sections you changed, as they were in the team's draft
     one-shot-prompt.md before your change. Only those sections, not the
     whole prompt. -->

````text
Paste the text before your change here.
````

### 3b. After

<!-- The same sections of one-shot-prompt.md after your change. -->

````text
Paste the text after your change here.
````

### 3c. Why it is better

<!-- Required: argue that the change makes the prompt better, and defend it.
     Name the rubric criterion it serves (one-shot-prompt-specs.md) and the
     design practice from handout 8.4 it follows (for example: one place for
     each definition, a contract for each piece, load only the rows needed),
     then explain why the prompt is better for it: what a reader or agent
     could misread, guess or get wrong before, and why the new text fixes
     that. How you argue is up to you. Evidence helps (a query on the data, a
     fresh agent that no longer asks or guesses, a use case walked through
     click by click), but a clear, reasoned argument is what is required.
     "It is clearer now" alone is not an argument. -->

Write your argument here.

