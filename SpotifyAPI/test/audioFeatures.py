import requests

track_id = "6rqhFgbbKwnb9MLmUQDhG6"  # Replace with your song's ID
url = f"https://api.spotify.com/v1/audio-features/{track_id}"
ACCESS_TOKEN = "BQCJI3yN6RN5oDa6KnCvbxK2fvoOAw-_fiOiyEHSJR-6Ypf4eJnAspyaEl6FU2k1HZleI5nYC17rweK6e8sx7teEbBeDPor4DU7EqJKFzh4WgdHhQVoleN0xFQALkHLNtaq6SFhwogM"

headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
response = requests.get(url, headers=headers)

audio_features = response.json()
print(audio_features)
