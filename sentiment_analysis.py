from googleapiclient.discovery import build
from textblob import TextBlob
import pandas as pd

api_key = 'your api key'
youtube = build('youtube', 'v3', developerKey=api_key)

videos = pd.read_csv("data/video_stats.csv")
sentiments = []

for _, row in videos.iterrows():
    video_id = row['video_id']
    channel_name = row['channel_name']
    try:
        comments = youtube.commentThreads().list(part='snippet', videoId=video_id, maxResults=50).execute()
        for item in comments['items']:
            text = item['snippet']['topLevelComment']['snippet']['textDisplay']
            polarity = TextBlob(text).sentiment.polarity
            label = 'Positive' if polarity > 0.1 else 'Negative' if polarity < -0.1 else 'Neutral'
            sentiments.append({
                'channel_name': channel_name,
                'video_id': video_id,
                'comment': text,
                'sentiment_score': polarity,
                'sentiment_label': label
            })
    except:
        continue

pd.DataFrame(sentiments).to_csv('data/comments_sentiment.csv', index=False)

