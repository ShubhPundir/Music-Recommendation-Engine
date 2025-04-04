import requests

ACCESS_TOKEN = "BQCJI3yN6RN5oDa6KnCvbxK2fvoOAw-_fiOiyEHSJR-6Ypf4eJnAspyaEl6FU2k1HZleI5nYC17rweK6e8sx7teEbBeDPor4DU7EqJKFzh4WgdHhQVoleN0xFQALkHLNtaq6SFhwogM"

query = "The Beatles"
url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=5"
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

response = requests.get(url, headers=headers)
songs = response.json()

for track in songs["tracks"]["items"]:
    print(f"{track['name']} by --> {track['artists'][0]['name']}")
