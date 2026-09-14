# Auxiliary Data

## Two Possible Audiences

**Audience A:** A Content Acquisition Manager at iHeartMedia must decide which active podcasts to investigate as potential candidates for distribution partnerships.

**Audience B:** A Product Manager at Riverside.fm, an online recording and editing platform, must decide whether to build a multi-language UI localization feature for creator workflows.

The additions below are proposed research designs. They are not datasets already obtained, verified company procedures, or statements made by actual stakeholders.

## Audience A: iHeartMedia

### Missing decision-important information

Podcast Index can help identify active feeds, but it does not show whether their owners are available for a new distribution partnership. The missing input is the podcast owner's reported partnership availability and interest, including whether an existing exclusive agreement would prevent discussions.

This matters because an active podcast may already have distribution commitments or may not want a partnership. The hosting domain does not establish ownership, network affiliation, or contractual availability.

### One promising source and who could collect it

A short partnership-screening questionnaire completed by podcast owners or authorized representatives could supply this information. An iHeartMedia partnerships or acquisition team could collect responses from a limited shortlist identified using Podcast Index. This is a proposed collection method, not a claim that iHeartMedia already uses this questionnaire.

The questionnaire would ask whether the respondent controls distribution decisions, whether an existing agreement restricts new partnerships, and whether they want further discussion. Respondents could select "unknown" or "prefer not to disclose" rather than being forced to provide contract details.

### Likely rows and fields

One row would represent one podcast's screening response on a particular date.

| Proposed field | Purpose |
| --- | --- |
| `feed_url` | Connect the response to the podcast feed. |
| `response_date` | Record when the information was supplied. |
| `authorized_representative` | Record whether the respondent reports authority to discuss distribution. |
| `current_distributor` | Identify a reported existing distributor, if disclosed. |
| `exclusive_distribution` | Record yes, no, unknown, or not disclosed. |
| `agreement_end_date` | Record an end date if applicable and voluntarily disclosed. |
| `partnership_interest` | Record interested, not interested, or needs more information. |

### How to obtain and connect it

For an initial study, the team could propose screening 20 to 30 shortlisted podcasts through their publicly listed business contact channels, subject to organizational access and permission. No outreach has been conducted.

Ask each respondent for the exact RSS feed URL and match it to Podcast Index's `url` field. Check redirects and `originalUrl` when necessary, then retain the matched Podcast Index `id`. Review ambiguous matches manually. Do not match on title alone or assume every feed represents a different show.

### What could fail

Owners may not reply, may misunderstand exclusivity, or may lack authority to speak for a show. Responses may become outdated. A nonresponse must remain unknown; it cannot be classified as available or uninterested. Multiple feeds may describe one show, creating duplicate contacts or counts.

Self-reported availability is only a screening signal. A company would still need to verify rights and agreements before making a partnership decision. This addition also does not establish audience size, commercial value, or content suitability.

### New question made answerable

Among the active podcasts shortlisted from Podcast Index, which respondents report both interest in a partnership and no known exclusive distribution restriction?

That would help prioritize follow-up conversations, rather than justify a final acquisition or partnership decision.

### Small synthetic prototype

If real responses are unavailable, create five clearly fictional screening records with varied interest and exclusivity responses, including unknown values. Use fictional feed records in a separate demonstration table. The prototype could show how a shortlist is filtered and how uncertainty is retained. It would not provide evidence about real podcasts.

## Audience B: Riverside.fm

### Missing decision-important information

The missing input is creators' preferred interface language and the workflow difficulties they associate with using an English interface. A podcast's declared language does not tell us which software language its creator prefers, whether the creator uses Riverside, or whether localization would solve a meaningful problem.

### One promising source and who could collect it

A targeted creator-language survey could provide this information. Riverside's product research team could invite current users and prospective users who create podcasts, including creators from several non-English podcast-language segments.

The survey would ask about interface preferences and specific recording or editing tasks that are difficult to understand. This is a proposed study; access to Riverside customers or internal systems has not been obtained.

### Likely rows and fields

One row would represent one creator's survey response.

| Proposed field | Purpose |
| --- | --- |
| `response_id` | Identify an anonymous response. |
| `response_date` | Record when the response was collected. |
| `feed_url` | Optionally link a podcast created by the respondent to Podcast Index. |
| `riverside_usage` | Distinguish current, former, and prospective users. |
| `preferred_ui_language` | Record the creator's preferred software language. |
| `english_ui_difficulty` | Record reported difficulty on a defined 1-to-5 scale. |
| `workflow_needing_translation` | Identify a task such as recording setup, editing, or export. |
| `localization_importance` | Record how important translation would be to the respondent. |

### How to obtain and connect it

An initial study could recruit a small sample across selected language segments and report the number of respondents in each segment. Recruitment would require Riverside's cooperation or a separate voluntary creator-research effort; neither has occurred.

For respondents who voluntarily supply a feed URL, match it to Podcast Index's `url`, checking redirects and duplicates. Compare the feed's declared `language` and publishing activity with the creator's reported preferences. Keep unmatched responses for survey analysis, but do not present them as linked records.

The unit of analysis remains the creator response. One creator may operate several feeds, and several creators may work on one feed. A separate response-to-feed mapping would be needed if multiple feeds are collected, to avoid inflating respondent counts.

### What could fail

Voluntary respondents may differ from other creators. An English-only questionnaire could exclude the people most affected by language barriers, so translated questions would need checking for consistent meaning. Self-reported difficulty may also reflect confusing product design rather than language alone.

Podcast language must not be treated as country or preferred interface language. Current and prospective users should be analyzed separately. Stated interest cannot establish willingness to pay or prove that localization improves conversion, retention, or revenue.

### New question made answerable

Among surveyed creators, which preferred interface languages are associated with reported workflow difficulties and strong interest in localization?

This could help Riverside decide which language and workflow to investigate with a translated prototype. It would not establish a complete business case without cost estimates and further product testing.

### Small synthetic prototype

If real responses are unavailable, create ten clearly labeled fictional responses covering several podcast and interface languages. Include creators who prefer English despite publishing in another language, plus unmatched feed URLs. Demonstrate summaries of reported difficulty by preferred interface language. These records would test the analysis process only, not demonstrate actual demand.

## What Was Checked and What Remains Open

### Checked against the supplied materials

- The dataset overview, especially section 6, identifies the absence of ownership and distribution information, actual audience metrics, and geographic information.
- The team's Data Fit file explains that iHeartMedia can use publishing metadata for an initial shortlist, while Riverside can use language segments to identify groups worth investigating.
- The overview warns that a feed is not necessarily a unique show. The proposed matching procedures therefore include duplicate and redirect checks.
- The Module 3 handout permits auxiliary data collected by an organization and clearly labeled synthetic examples when real data is unavailable.

These are checks against course and team documents, not an independent database audit or verification of either company's actual workflow. No surveys, interviews, contract checks, or company-system access have been completed. The proposed fields and collection methods are AI-assisted hypotheses for review.

### Open questions

- Would podcast representatives disclose enough information to screen partnership availability, and how would their authority be verified?
- Could Riverside recruit a sufficiently varied group of creators, including people who find English interfaces difficult?
- What response levels would be adequate for each screening or research decision?
- What safeguards and update schedule would each organization require for responses?
- What further evidence would be required before acting: rights and commercial checks for iHeartMedia, and localization costs and product testing for Riverside?

## References

- Course handout: `03-handout.pdf`, sections 3.1 and 3.2.4, supplied with the assignment.
- [Podcast Index dataset overview](https://github.com/USC-DSO-576-PS/dataset_podcast-index/blob/main/data_overview_podcast-index.md), especially sections 5 and 6; reviewed from the supplied copy.
- [Team M7 Data Fit](https://github.com/JoanneY416/DSO576-project/blob/main/data-fit.md); reviewed from the supplied text.

