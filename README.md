# TED-Ed Channel Performance Analysis

An age-adjusted outlier analysis of 93 long-form TED-Ed videos, built to identify which
topics and title structures earn views beyond what's typical for a video of that age.

**[View the sample interactive dashboard →](https://docs.google.com/spreadsheets/d/1eDVFxWVHSPVqVNrYMklhrTqkPeLRvvajPun5At5r50w/edit?usp=sharing)**

## Why age-adjusted?

Raw view counts favor old videos — a video from 2015 has had over a decade to accumulate
views that a video from last week hasn't had time to earn. Comparing every video's views to
the **median views of other videos uploaded in the same age band** (0–30, 31–90, 91–180,
181+ days) controls for this, so the comparison is about performance, not age.

```
Performance Ratio = Video's views ÷ Median views of its age band
```

A ratio of 1.0 is typical for that age. ≥2.0 is flagged as an **outlier**; ≤0.5 is flagged
as an **underperformer**.

## Key findings

| Finding | Detail |
|---|---|
| **Health/Psychology topics outperform sharply** | Median ratio 2.34 (n=27) — more than double the typical video of the same age, with 15 of 27 flagged as outliers and zero underperformers |
| **Everyday-relevant topics beat abstract ones** | Median ratio 1.23 vs. 0.86 for topics with no personal relevance to the average viewer |
| **The "Think Like a Musician" series underperforms** | Median ratio 0.27 (n=9) — 7 of 9 videos in the series are flagged as underperformers |
| **Question-style titles slightly outperform statements** | Median ratio 1.11 (Question) vs. 0.96 (Statement) vs. 0.85 (List) |

Full breakdown, methodology, and limitations are in [`ANALYSIS.md`](ANALYSIS.md).

## Repo contents

```
.
├── README.md              This file
├── ANALYSIS.md             Full methodology, findings, and limitations
├── collect_data.py         Pulls video metadata via the YouTube Data API
├── requirements.txt        Python dependencies
├── data/
│   ├── ted_ed_videos.csv          Raw collected dataset (title, views, upload date, duration, URL)
│   └── ted_ed_videos_tagged.csv   Full dataset with age-band, ratio, and tag columns added
└── output/
    └── TED-Ed-Dashboard.xlsx      Tagged data, pivot tables, and dashboard charts
```

## How it was built

1. **Collect** — `collect_data.py` pulls the channel's uploads via the YouTube Data API v3
   (video metadata + statistics), keeping the last ~12 months.
2. **Clean** — flag Shorts (≤180s) and exclude them from age-band medians.
3. **Tag** — each video is manually tagged by title structure (Question / Statement /
   List), topic category, and everyday relevance, against a fixed rule set (see
   `ANALYSIS.md`).
4. **Analyze** — group by tag and compute median performance ratio per group, using
   formulas (not hardcoded values) so the workbook recalculates if tags change.
5. **Visualize** — dashboard with KPI summary and four comparison charts.

## Running it yourself

```bash
pip install -r requirements.txt
export YOUTUBE_API_KEY="your_key_here"
python collect_data.py
```

Requires a free [YouTube Data API v3](https://console.cloud.google.com/apis/library/youtube.googleapis.com)
key. Output is written to `data/ted_ed_videos.csv`.

## What I'd do next with full analytics access

- Compare CTR and impressions on the Health/Psychology outliers vs. typical performers,
  to separate a packaging effect from a content-demand effect
- Check traffic-source split (search / suggested / browse) on the top 5 outliers
- Compare retention curves between the highest- and lowest-ratio videos in the same age band
- A/B test a title/thumbnail change on an upcoming video using the patterns found here

## Tech

Python (`requests`, `pandas`), YouTube Data API v3, Google Sheets / Excel (`openpyxl`)
for the dashboard.

---
Built by [Your Name] as a work sample for data/analytics roles.
