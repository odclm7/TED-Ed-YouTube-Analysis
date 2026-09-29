"""
Collect video metadata from a YouTube channel's uploads via the YouTube Data API v3.

Pulls title, upload date, view count, duration, and URL for every long-form video and
Short published in roughly the last 12 months, and writes the result to
data/ted_ed_videos.csv.

Requires a free YouTube Data API v3 key:
https://console.cloud.google.com/apis/library/youtube.googleapis.com

Usage:
    export YOUTUBE_API_KEY="your_key_here"
    python collect_data.py
"""

import os
import re
import sys
from datetime import datetime, timedelta, timezone

import pandas as pd
import requests

BASE = "https://www.googleapis.com/youtube/v3"
CHANNEL_HANDLE = "TEDEd"
LOOKBACK_DAYS = 365
SHORT_MAX_SECONDS = 180
OUTPUT_PATH = "data/ted_ed_videos.csv"


def get_uploads_playlist(api_key: str, handle: str) -> str:
    resp = requests.get(
        f"{BASE}/channels",
        params={"part": "contentDetails", "forHandle": handle, "key": api_key},
        timeout=15,
    )
    resp.raise_for_status()
    items = resp.json().get("items", [])
    if not items:
        raise ValueError(f"No channel found for handle '{handle}'")
    return items[0]["contentDetails"]["relatedPlaylists"]["uploads"]


def get_video_ids(api_key: str, playlist_id: str, max_videos: int = 300) -> list[str]:
    ids, token = [], None
    while len(ids) < max_videos:
        resp = requests.get(
            f"{BASE}/playlistItems",
            params={
                "part": "contentDetails",
                "playlistId": playlist_id,
                "maxResults": 50,
                "pageToken": token,
                "key": api_key,
            },
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        ids += [item["contentDetails"]["videoId"] for item in data["items"]]
        token = data.get("nextPageToken")
        if not token:
            break
    return ids


def parse_iso8601_duration(duration: str) -> int:
    """Convert an ISO 8601 duration like 'PT4M13S' to total seconds."""
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration)
    hours, minutes, seconds = (int(g or 0) for g in match.groups())
    return hours * 3600 + minutes * 60 + seconds


def get_video_details(api_key: str, video_ids: list[str]) -> list[dict]:
    rows = []
    collected_at = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i : i + 50]
        resp = requests.get(
            f"{BASE}/videos",
            params={
                "part": "snippet,statistics,contentDetails",
                "id": ",".join(batch),
                "key": api_key,
            },
            timeout=15,
        )
        resp.raise_for_status()
        for video in resp.json()["items"]:
            duration_sec = parse_iso8601_duration(video["contentDetails"]["duration"])
            rows.append(
                {
                    "Title": video["snippet"]["title"],
                    "Upload date": video["snippet"]["publishedAt"][:10],
                    "Views": int(video["statistics"].get("viewCount", 0)),
                    "Duration (sec)": duration_sec,
                    "Is Short": duration_sec <= SHORT_MAX_SECONDS,
                    "URL": f"https://www.youtube.com/watch?v={video['id']}",
                    "Date collected": collected_at,
                }
            )
    return rows


def main() -> None:
    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        sys.exit("Set the YOUTUBE_API_KEY environment variable before running this script.")

    playlist_id = get_uploads_playlist(api_key, CHANNEL_HANDLE)
    video_ids = get_video_ids(api_key, playlist_id)
    rows = get_video_details(api_key, video_ids)

    df = pd.DataFrame(rows)
    df["Upload date"] = pd.to_datetime(df["Upload date"])
    cutoff = datetime.now() - timedelta(days=LOOKBACK_DAYS)
    df = df[df["Upload date"] >= cutoff].sort_values("Upload date", ascending=False)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {len(df)} videos to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
