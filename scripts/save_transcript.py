from youtube_transcript_api import YouTubeTranscriptApi
import sys

try:
    transcript = YouTubeTranscriptApi.get_transcript('Nie3xloSN6A', languages=['th', 'en'])
    text = " ".join([t['text'] for t in transcript])
    with open('transcript.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Transcript saved to transcript.txt")
except Exception as e:
    print(f"Error: {e}")
