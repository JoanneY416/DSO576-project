# Maya Chen and the Podcast Research Shortlist

Yifei Gan | DSO 576 | Individual Case

## 1 The person and the decision

Maya Chen is a hypothetical podcast acquisitions researcher at iHeartMedia. She needs to choose English-language true crime feeds for an initial review. She has limited research time, so she wants to see whether a 30-day or 90-day activity filter gives her a more useful shortlist. This is a research decision, not a decision to buy a podcast.

## 2 Her situation and alternatives

iHeartMedia’s partnership with Global includes licensing, distribution and advertising representation [1]. This shows why Maya needs to check more than a show’s title before considering a partnership. Acast describes Podcast Index as an open database that creators can submit their shows to [2]. It is useful for discovery, but a listing does not prove commercial availability.

Maya could search podcast directories, read publisher websites and listen to recent episodes, then organize the results in a spreadsheet. The App helps her apply the same screening rules to its sample. She still needs those other sources to check ownership, current activity and content quality.

## 3 The app in use

Live App: [Podcast Opportunity Explorer](https://dso576-project-podcast-index.streamlit.app/)

I selected true crime, English (all variants), at least 20 episodes, Any explicit-content preference, and a minimum discovery score of 0. I searched with 30 days and then 90 days, keeping the other settings unchanged. These are case choices, not official iHeartMedia requirements.

The 30-day search returned 3 eligible feeds. The 90-day search returned the same 3 plus KAMEOFV REDDITS. Its latest displayed episode was July 31, 2026, with 27 episodes and a discovery score of 2. The screenshots below show both searches.

### Screenshots of the live app

![Figure 1. With the 30-day activity window, 3 feeds meet the screening rules.](screenshots/yifei-30.png)

Figure 1. With the 30-day activity window, 3 feeds meet the screening rules.

![Figure 2. With the 90-day window, KAMEOFV REDDITS is added, giving 4 eligible feeds.](screenshots/yifei-90.png)

Figure 2. With the 90-day window, KAMEOFV REDDITS is added, giving 4 eligible feeds.

## 4 Reading the result for her decision

**Does the number measure what she needs?** The results help Maya make a research list. They do not show which podcast is the best investment. The App says discovery score is not audience size, revenue or acquisition value, so a score of 9 does not prove a better opportunity than a score of 2.

**Who is included or left out?** The App uses a 6,000-feed course sample, not the full Podcast Index catalog. Each row is a feed, which may not be a unique show. Shows outside the sample or below the 20-episode minimum are excluded. The App also says feeds with blank GUIDs cannot be reliably deduplicated.

**What outside the data matters?** The activity windows end on August 31, 2026, the sample’s reference date. They do not measure activity relative to today. Maya should check current feeds, ownership, available rights and recent content before contacting anyone. Hosting domains and explicit-content flags do not settle those questions.

**What could she wrongly conclude?** She could think the four results are the best currently active true crime acquisition targets. That would confuse sample eligibility with market coverage and commercial suitability. Three results also have primary categories other than true crime. The App matches category fields 1–8, so this does not prove a bug, but the exact matching field is not shown.

## 5 The verdict and change request

I would start by reviewing the three feeds that appear under both activity windows and keep KAMEOFV REDDITS as a backup. Its exclusion from the 30-day search does not prove it has stopped publishing. The App is useful for narrowing this sample, while directories and publisher checks remain necessary for broader discovery and verification.

I choose break because the category match is difficult to check. My change request is to show the matched category and whether it is primary or secondary for each result. The change should work for every category and should not change which feeds qualify. A simple check is that the same four feeds remain in the 90-day result, with their matching category fields visible. This would make the shortlist easier to explain without treating it as an acquisition recommendation.

### Sources

[1] iHeartMedia, November 15, 2023. [iHeartMedia and Global Sign Multi-Year Podcast Partnership Deal in the UK, Ireland and USA](https://investors.iheartmedia.com/news/news-details/2023/iHeartMedia-and-Global-Sign-Multi-Year-Podcast-Partnership--Deal-in-the-UK-Ireland-and-USA-2023-hYxAs7n6ad/default.aspx)

[2] Acast Learning Center, April 17, 2026. [What is Podcast Index](https://learn.acast.com/en/articles/8597256-what-is-podcast-index)
