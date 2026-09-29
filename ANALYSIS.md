# Methodology, Findings & Limitations

## Scope

93 long-form TED-Ed videos uploaded in the last ~12 months. Two additional videos under
180 seconds were tagged as Shorts and excluded from age-band medians (included in the raw
dataset, flagged via `Is Short`). Data pulled via the YouTube Data API v3 and snapshotted
on 2026-09-28. View counts are a single point-in-time snapshot, not a time series.

## Age-band methodology

Videos are grouped into four age bands based on days since upload: **0–30, 31–90, 91–180,
181+**. Within each band, the median view count of long-form (non-Short) videos becomes
that band's baseline.

```
Performance Ratio = Video's views ÷ Median views of its age band
```

- **Outlier**: ratio ≥ 2.0 (double the typical video of that age)
- **Underperformer**: ratio ≤ 0.5 (half the typical video of that age)

These thresholds are a judgment call, not an industry standard, and can be adjusted in the
workbook without touching the underlying data.

**Known weakness:** the 0–30 day band is wide relative to how quickly early view velocity
changes — a 3-day-old video and a 28-day-old video are compared against the same baseline.
With a larger dataset this band should be split further (e.g. 0–7, 8–30).

## Tagging

| Field | Method | Values |
|---|---|---|
| **Title structure** | Rule-based: starts with a digit → List; contains "?" → Question; else → Statement | Question / Statement / List |
| **Topic category** | Manual judgment against a fixed rule set | Health/Psychology, Science, History/Culture, Society, Arts/Language |
| **Everyday relevance** | Manual judgment: does the topic describe something the average viewer personally experiences (sleep, attention, habits) vs. something external or abstract (ancient civilizations, tariffs)? | Yes / No |
| **Series flag** | Detects "Think Like a Musician" in the title | True / False |

Topic category and everyday relevance are the most subjective parts of this analysis and
are the first place to sanity-check the results.

## Findings

### By topic category (median performance ratio)

| Category | n | Median ratio | Outliers | Underperformers |
|---|---|---|---|---|
| Health/Psychology | 27 | **2.34** | 15 | 0 |
| Society | 10 | 1.01 | 1 | 0 |
| History/Culture | 19 | 1.00 | 2 | 1 |
| Science | 16 | 0.86 | 0 | 3 |
| Arts/Language | 21 | 0.55 | 0 | 9 |

Health/Psychology is the clear standout — more than double the typical video of the same
age, and the only category with zero underperformers.

### By title structure

| Structure | n | Median ratio |
|---|---|---|
| Question | 37 | 1.11 |
| Statement | 51 | 0.96 |
| List | 5 | 0.85 |

The effect is real but small. With only 5 List-titled videos, that group's median is not
statistically reliable.

### By everyday relevance

| Relevance | n | Median ratio |
|---|---|---|
| Yes | 34 | 1.23 |
| No | 59 | 0.86 |

### Think Like a Musician series vs. all other videos

| Group | n | Median ratio |
|---|---|---|
| Series | 9 | 0.27 |
| All other videos | 84 | 1.05 |

This series is worth calling out on its own rather than folding into the general
Arts/Language number, since it's dragging that category's median down sharply.

## Limitations

- **Public view counts only.** No CTR, impressions, traffic-source, or retention data,
  which YouTube Studio would provide and which would materially sharpen these conclusions.
- **Small samples in some groups.** The 0–30 and 31–90 day bands, and the List title
  structure (n=5), should be read as directional, not conclusive.
- **Correlation, not causation.** A topic category correlating with higher performance
  doesn't establish that the topic *caused* the lift — packaging, timing, and algorithmic
  promotion are confounded with topic in this dataset.
- **Manual tags carry judgment.** Topic category and everyday relevance were assigned by
  one person against a written rule set, but are inherently more subjective than the
  rule-based title structure tag.

## Suggested next steps with full analytics access

1. Compare CTR and impressions on the Health/Psychology outliers vs. that category's
   typical performers, to see whether the lift is a packaging effect or a genuine
   demand/retention effect.
2. Check traffic-source split (search vs. suggested vs. browse) on the top 5 outliers.
3. Compare retention curves between the highest- and lowest-ratio videos within the same
   age band.
4. Run an A/B test on title/thumbnail packaging for an upcoming video, using the patterns
   identified here as the hypothesis.
