import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open("YouTubeAnalytics")

# Upload each dataset to corresponding worksheet
def update_sheet(sheet_name, file):
    ws = sheet.worksheet(sheet_name)
    df = pd.read_csv(file)
    ws.clear()
    ws.update([df.columns.values.tolist()] + df.values.tolist())

update_sheet("ChannelStats", "data/channel_stats.csv")
update_sheet("VideoStats", "data/video_stats.csv")
update_sheet("Comments", "data/comments_sentiment.csv")
update_sheet("Forecast", "data/forecasted_subs.csv")

print("All data pushed to Google Sheets ✅")