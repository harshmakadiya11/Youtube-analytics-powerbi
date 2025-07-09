import os
import pandas as pd
from googleapiclient.discovery import build
from datetime import datetime

api_key = 'AIzaSyAAlfPniCr-xspUWYRa0mF_Kvr33jPlRIs'
youtube = build('youtube', 'v3', developerKey=api_key)

channels = {
    "MrBeast": "UCX6OQ3DkcsbYNE6H8uQQuVA",
    "MKBHD": "UCBJycsmduvYEL83R_U4JriQ"
}

os.makedirs("data", exist_ok=True)
channel_stats = []
video_stats = []
subscriber_timeseries = []

today = datetime.today().strftime("%Y-%m-%d")

for name, cid in channels.items():
    res = youtube.channels().list(part='snippet,statistics', id=cid).execute()
    data = res['items'][0]

    stats = data['statistics']
    channel_stats.append({
        "channel_name": name,
        "subscribers": int(stats.get("subscriberCount", 0)),
        "views": int(stats.get("viewCount", 0)),
        "videos": int(stats.get("videoCount", 0)),
        "date": today
    })
    subscriber_timeseries.append({"channel_name": name, "subscribers": int(stats.get("subscriberCount", 0)), "date": today})

    # Video list
    vids = youtube.search().list(part='snippet', channelId=cid, maxResults=20, order='date').execute()
    for item in vids['items']:
        vid_id = item['id'].get('videoId')
        if vid_id:
            stats = youtube.videos().list(part='statistics,snippet', id=vid_id).execute()['items'][0]
            video_stats.append({
                "video_id": vid_id,
                "channel_name": name,
                "title": stats['snippet']['title'],
                "views": int(stats['statistics'].get("viewCount", 0)),
                "likes": int(stats['statistics'].get("likeCount", 0)),
                "published": stats['snippet']['publishedAt']
            })

# Convert to DataFrames
channel_stats_df = pd.DataFrame(channel_stats)
video_stats_df = pd.DataFrame(video_stats)
subscriber_df = pd.DataFrame(subscriber_timeseries)

# Append to subscriber_timeseries.csv if it exists
subscriber_file = "data/subscriber_timeseries.csv"
if os.path.exists(subscriber_file):
    existing = pd.read_csv(subscriber_file)
    combined = pd.concat([existing, subscriber_df])
    combined = combined.drop_duplicates(subset=["channel_name", "date"], keep="last")  # avoid duplicates
    combined.to_csv(subscriber_file, index=False)
else:
    subscriber_df.to_csv(subscriber_file, index=False)

# Overwrite other files
channel_stats_df.to_csv("data/channel_stats.csv", index=False)
video_stats_df.to_csv("data/video_stats.csv", index=False)
