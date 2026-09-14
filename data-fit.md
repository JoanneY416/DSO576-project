# Data Fit

## Audience A: iHeartMedia

A Content Acquisition Manager at iHeartMedia must decide which active podcasts to investigate as potential candidates for distribution partnerships.

### What the data observes

Each row represents one podcast RSS or Atom feed that Podcast Index has crawled. 

The dataset contains information about podcast publishing activity, language, category, hosting domain, and episode history. However, it does not contain actual listener or business performance data.

### Useful columns

- `newestItemPubdate`: Shows when the most recent episode found by Podcast Index was published. This can help identify podcasts that are still active.
- `episodeCount`: Shows how many episodes Podcast Index has stored for the feed. This can help identify podcasts with a longer publishing history.
- `updateFrequency`: Provides information about the podcast's publishing cadence.
- `category1` through `category8`: Show the categories associated with the podcast and can help iHeartMedia identify podcasts in relevant content areas.
- `language`: Shows the language declared by the podcast feed.
- `explicit`: Shows whether the podcast feed marks itself as explicit.
- `host`: Shows the domain that hosts the RSS feed. It can provide information about where the feed is hosted, but it does not show who owns the podcast or whether it belongs to a major network.

### What the data supports

The dataset can help iHeartMedia identify podcast feeds that have recently published episodes, have a substantial episode history and match particular categories or languages. These characteristics could be useful for creating an initial list of active podcasts to investigate further.

### What is partly supported

The data can support the first stage of finding potential partnership candidates, but it cannot determine which podcasts are actually good distribution partners. Publishing activity and episode count may indicate that a podcast is active and established, but they do not show its actual audience size or commercial value.

### What is outside the data's scope

The dataset does not contain listener counts, downloads, subscribers, ratings or reviews, revenue, or other direct measures of audience performance. It also does not show podcast ownership, network affiliation, existing distribution partnerships, or whether a creator would be interested in partnering with iHeartMedia.

Therefore, iHeartMedia would need additional audience, business, and ownership information before making a final partnership decision.

### Association vs. causation

The dataset can show associations between podcast characteristics and publishing activity. For example, some categories or hosting platforms may contain more recently active feeds than others. However, the data cannot show that a particular category, host, or other characteristic causes a podcast to be successful or makes it a better distribution partner.


## Audience B: Riverside.fm

A Product Manager at Riverside.fm, an online recording and editing platform, must decide whether to build a multi-language UI localization feature for creator workflows.

### What the data observes

The dataset contains information about the language declared by each podcast feed and information about its publishing history and activity.

### Useful columns

- `language`: It shows the language declared by each podcast feed and can help identify large non-English language segments.
- `newestItemPubdate`: Shows when the most recent episode was published and can help identify language segments with recently active podcast feeds.
- `oldestItemPubdate`: Shows the oldest episode date found by Podcast Index. It can provide an approximate indication of when publishing began.
- `episodeCount`: Provides information about the number of episodes stored for a feed and can help describe publishing history.
- `updateFrequency`: Provides information about publishing cadence.
- `category1` through `category8`: Can provide additional information about the types of podcast content produced in different language segments.

### What the data supports

The dataset can help Riverside compare the size and publishing activity of different language segments. For example, Riverside could examine which non-English languages have many podcast feeds and which languages have many feeds that are still publishing recently.

This could help identify language segments that may be worth investigating further for UI localization.

### What is partly supported

The data can help Riverside identify potentially important non-English creator segments, but it cannot directly determine whether Riverside should build a localized UI for a particular language.

A large or active podcast language segment does not necessarily mean that Riverside has many users who speak that language or that those users want a localized interface.

### What is outside the data's scope

The dataset does not contain Riverside's actual user data, user language preferences, requests for localized features, user feedback, subscriptions, conversion rates, or revenue.

It also contains no geographic information such as country, state, or city. Therefore, a Spanish-language podcast cannot automatically be treated as being from Spain or any other specific market. 

The dataset also does not contain the cost of developing and maintaining localization or evidence showing whether localization would increase Riverside's users, retention, or revenue.

### Association vs. causation

The data can show that certain language segments have more podcast feeds or more recently active feeds than others. However, this does not prove that adding a UI in that language would cause Riverside to gain more users, subscriptions, or revenue. Riverside would need its own user and product data to evaluate that effect.


## Open Questions

For iHeartMedia, additional research would be needed to determine the audience size, ownership, network affiliation, commercial performance, and partnership interest of potential podcast candidates.

For Riverside, additional research would be needed to understand the languages used by its actual customers, demand for localized interfaces, geographic markets, localization costs, and the possible effect of localization on user acquisition and retention.