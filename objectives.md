# Objectives

## iHeartMedia Content Acquisition Manager

As an iHeartMedia Content Acquisition Manager, I must decide which active podcasts to prioritize for distribution-partnership outreach. The desired outcome is a portfolio of commercially promising shows that publish reliably and meet advertiser brand-safety standards. I would use a high episode count, a recent `newestItemPubdate`, and a faster `updateFrequency` code as initial signals of publishing activity; `explicit = 0` is only a publisher-declared screening signal, not proof that a show is brand-safe. The tradeoff is that more stringent screening reduces the candidate pool and increases due-diligence cost, but reduces reputational and advertiser risk.

The constraints are an acquisition budget, limited staff time for due diligence, and the fact that the Podcast Index dataset contains neither ownership nor contract information. A wrong decision could result in acquiring a show with unreviewed sensitive content, copyright issues, or poor audience performance, wasting budget and potentially harming advertiser confidence and iHeartMedia's reputation. Evidence that could change my decision includes a completed content and rights review, verified first-party audience analytics, or evidence of an exclusive agreement with another network. I would measure success with post-signing advertising-revenue growth, new-listener retention, partnership renewal, and stable post-signing episode output. Revenue, listener retention, rights status, and contract status require company or creator data.

## Riverside.fm Product Manager

As a Riverside.fm Product Manager, I must decide whether to develop multilingual UI localization for creator workflows. The desired outcome is profitable international growth among non-English-speaking creators. The Podcast Index `language` field and recent `newestItemPubdate` values can help identify active non-English-language feeds, while `createdOn` can only show when Podcast Index first saw a feed—not when a show launched or where its creators are located. The tradeoff is between international-localization investment and continued investment in core audio-video recording and editing features.

The constraints are engineering capacity to build and maintain a multilingual architecture, localization and customer-support costs, and the dataset's lack of geography, product usage, conversion, pricing, and revenue data. A wrong decision would divert engineering resources and add long-term operating costs without increasing overseas revenue. Evidence that could change my decision includes product research showing that language is not the primary adoption barrier, or showing that affordability, payment access, or network latency matters more. I would measure success through registrations and first-month retention among localized-language users, paid conversion, and international annual recurring revenue. These measures require Riverside.fm product and financial data.

## Comparison of the Two Audiences

The iHeartMedia audience makes an outward-facing partnership and risk-management decision: which active feeds merit further commercial and compliance review. Riverside.fm makes an internal product-investment decision: whether localization is a worthwhile use of engineering capacity. Both can use feed metadata to identify candidate segments, but neither can use this dataset alone to establish audience size, revenue, ownership, contracts, verified brand safety, user demand, or geographic market size.

## Sourced Facts from the Podcast Index Dataset

- One row represents a podcast feed, not necessarily a unique show.
- `episodeCount`, `newestItemPubdate`, and `updateFrequency` describe episode volume and observed publishing recency or cadence; they can support a screening rule for active feeds.
- `explicit` is self-declared by the publisher and is not audited, so it is not a conclusive brand-safety assessment.
- `language` is publisher-entered, inconsistently formatted, and does not indicate a creator's country or market; the dataset contains no geography.
- `createdOn` records when Podcast Index first saw a feed, not the show's launch date.
- `host` is the domain serving the RSS feed, not evidence of show ownership, network affiliation, or independence.
- The dataset contains no listener, download, revenue, contract, ownership, rights, product-usage, conversion, or retention data.

## AI-Generated Hypotheses to Test

- Feeds with a high episode count, recent publishing activity, and a faster update-frequency code may be lower-risk candidates for further iHeartMedia outreach, but those signals do not prove long-term creator commitment or partnership availability.
- A growing number of recently active non-English-language feeds may indicate a segment worth investigating for Riverside.fm, but it does not prove demand for localized UI or identify the most promising geographic market.
- For Riverside.fm, UI language may be a conversion barrier, but affordability, payment methods, creator workflows, and network performance may be more important barriers.

## Questions Requiring Real Stakeholder Input

- **iHeartMedia business-development and advertising teams:** What is the maximum all-in acquisition and due-diligence budget per show? Which content verticals and brand-safety standards do advertisers currently require? What verified audience, revenue, rights, and exclusivity evidence is required before signing?
- **Riverside.fm engineering, finance, research, and go-to-market teams:** What localization and maintenance capacity is available? Which languages and markets have sufficient willingness to pay? Do user research and funnel data show that UI language, rather than pricing, payments, or latency, is the main barrier? What revenue threshold must each localized market meet to cover localization and support costs?
