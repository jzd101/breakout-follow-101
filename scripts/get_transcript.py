from youtube_transcript_api import YouTubeTranscriptApi
import sys

try:
    transcript = YouTubeTranscriptApi.get_transcript('Nie3xloSN6A', languages=['th', 'en'])
    text = " ".join([t['text'] for t in transcript])
    print(text)
except Exception as e:
    print(f"Error: {e}")
