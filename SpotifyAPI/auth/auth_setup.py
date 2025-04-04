import requests
import base64

# Your Spotify credentials
CLIENT_ID = "ebf259d867e942ffaf863c1c6262e7cd"
CLIENT_SECRET = "69ceba97f4de4056a6d5c3083a96f89f"

# Request Token
url = "https://accounts.spotify.com/api/token"
headers = {
    "Authorization": "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
}
data = {"grant_type": "client_credentials"}

response = requests.post(url, headers=headers, data=data)
token_info = response.json()

ACCESS_TOKEN = token_info["access_token"]
print("Access Token:", ACCESS_TOKEN)
