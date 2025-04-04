import requests
from typing import Dict, List, Optional
import base64
from auth.auth_setup import CLIENT_ID, CLIENT_SECRET
import time
import json
from datetime import datetime

class SpotifyClient:
    def __init__(self):
        print("Initializing SpotifyClient...")
        self.base_url = "https://api.spotify.com/v1"
        self.access_token = self._get_access_token()
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        print("SpotifyClient initialized successfully")

    def _get_access_token(self) -> str:
        """Get a fresh access token from Spotify."""
        print("Getting access token...")
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
        }
        data = {"grant_type": "client_credentials"}
        
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("Successfully obtained access token")
            return token
        print(f"Failed to get access token. Status code: {response.status_code}")
        raise Exception("Failed to get access token")

    def search_artist(self, query: str) -> Optional[Dict]:
        """Search for an artist and return their information."""
        print(f"Searching for artist: {query}")
        url = f"{self.base_url}/search"
        params = {
            "q": query,
            "type": "artist",
            "limit": 1
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if data["artists"]["items"]:
                print(f"Found artist: {data['artists']['items'][0]['name']}")
                return data["artists"]["items"][0]
        print(f"Failed to find artist. Status code: {response.status_code}")
        return None

    def get_artist_albums(self, artist_id: str, limit: int = 50) -> List[Dict]:
        """Get all albums by an artist."""
        print(f"Fetching albums for artist ID: {artist_id}")
        url = f"{self.base_url}/artists/{artist_id}/albums"
        params = {
            "limit": limit,
            "include_groups": "album,single,compilation"
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            albums = response.json()["items"]
            print(f"Found {len(albums)} albums")
            return albums
        print(f"Failed to fetch albums. Status code: {response.status_code}")
        return []

    def get_album_tracks(self, album_id: str) -> List[Dict]:
        """Get all tracks from an album."""
        print(f"Fetching tracks for album ID: {album_id}")
        url = f"{self.base_url}/albums/{album_id}/tracks"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            tracks = response.json()["items"]
            print(f"Found {len(tracks)} tracks in album")
            return tracks
        print(f"Failed to fetch tracks. Status code: {response.status_code}")
        return []

    def get_tracks_audio_features(self, track_ids: List[str]) -> Dict[str, Dict]:
        """Get audio features for multiple tracks at once."""
        if not track_ids:
            return {}
            
        # Spotify API allows up to 100 tracks per request
        features = {}
        for i in range(0, len(track_ids), 100):
            batch = track_ids[i:i+100]
            url = f"{self.base_url}/audio-features"
            params = {"ids": ",".join(batch)}
            
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                data = response.json()
                for track_id, feature in zip(batch, data["audio_features"]):
                    if feature:  # Some tracks might not have features
                        features[track_id] = feature
            else:
                print(f"Failed to fetch audio features. Status code: {response.status_code}")
            
            # Add a small delay to avoid rate limiting
            time.sleep(0.1)
        
        return features

    def get_tracks_details(self, track_ids: List[str]) -> Dict[str, Dict]:
        """Get details for multiple tracks at once."""
        if not track_ids:
            return {}
            
        # Spotify API allows up to 50 tracks per request
        details = {}
        for i in range(0, len(track_ids), 50):
            batch = track_ids[i:i+50]
            url = f"{self.base_url}/tracks"
            params = {"ids": ",".join(batch)}
            
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                data = response.json()
                for track_id, track in zip(batch, data["tracks"]):
                    if track:  # Some tracks might not be available
                        details[track_id] = track
            else:
                print(f"Failed to fetch track details. Status code: {response.status_code}")
            
            # Add a small delay to avoid rate limiting
            time.sleep(0.1)
        
        return details

    def get_album_tracks_with_details(self, album_id: str) -> List[Dict]:
        """Get all tracks from an album with detailed information."""
        tracks = self.get_album_tracks(album_id)
        if not tracks:
            return []
            
        # Get all track IDs
        track_ids = [track["id"] for track in tracks]
        
        # Get audio features and track details in batches
        print(f"Getting audio features for {len(track_ids)} tracks...")
        audio_features = self.get_tracks_audio_features(track_ids)
        
        print(f"Getting track details for {len(track_ids)} tracks...")
        track_details = self.get_tracks_details(track_ids)
        
        detailed_tracks = []
        for track in tracks:
            track_id = track["id"]
            if track_id in audio_features and track_id in track_details:
                details = track_details[track_id]
                features = audio_features[track_id]
                
                detailed_tracks.append({
                    "id": track_id,
                    "name": track["name"],
                    "track_number": track["track_number"],
                    "duration_ms": track["duration_ms"],
                    "popularity": details.get("popularity", 0),
                    "explicit": track["explicit"],
                    "external_urls": track["external_urls"],
                    "preview_url": track["preview_url"],
                    "audio_features": {
                        "danceability": features["danceability"],
                        "energy": features["energy"],
                        "key": features["key"],
                        "loudness": features["loudness"],
                        "mode": features["mode"],
                        "speechiness": features["speechiness"],
                        "acousticness": features["acousticness"],
                        "instrumentalness": features["instrumentalness"],
                        "liveness": features["liveness"],
                        "valence": features["valence"],
                        "tempo": features["tempo"]
                    }
                })
            else:
                print(f"Failed to get complete details for track: {track['name']}")
        
        print(f"Successfully processed {len(detailed_tracks)} tracks with complete details")
        return detailed_tracks

    def get_artist_info(self, artist_name: str) -> Dict:
        """Get comprehensive information about an artist including all their songs."""
        print(f"\nStarting to fetch information for artist: {artist_name}")
        artist = self.search_artist(artist_name)
        if not artist:
            return {"error": "Artist not found"}

        artist_id = artist["id"]
        albums = self.get_artist_albums(artist_id)
        
        # Get all tracks from each album
        all_tracks = []
        for album in albums:
            print(f"\nProcessing album: {album['name']}")
            album_tracks = self.get_album_tracks_with_details(album["id"])
            for track in album_tracks:
                track["album"] = {
                    "name": album["name"],
                    "release_date": album["release_date"],
                    "id": album["id"]
                }
                all_tracks.append(track)
            print(f"Completed processing album: {album['name']}")
            
            # Add a small delay between albums to avoid rate limiting
            time.sleep(0.5)

        print(f"\nTotal tracks collected: {len(all_tracks)}")
        return {
            "artist": {
                "name": artist["name"],
                "id": artist_id,
                "genres": artist["genres"],
                "popularity": artist["popularity"],
                "followers": artist["followers"]["total"]
            },
            "albums": [
                {
                    "name": album["name"],
                    "release_date": album["release_date"],
                    "total_tracks": album["total_tracks"],
                    "type": album["album_type"],
                    "id": album["id"]
                }
                for album in albums
            ],
            "tracks": all_tracks
        }

def save_to_json(data: Dict, artist_name: str) -> str:
    """Save the artist data to a JSON file."""
    # Create a filename with timestamp to avoid overwriting
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"spotify_data_{artist_name.lower().replace(' ', '_')}_{timestamp}.json"
    
    # Save the data to JSON file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nData saved to: {filename}")
    return filename

def main():
    try:
        # Create client with automatic token refresh
        client = SpotifyClient()
        
        # Get information for The Beatles
        print("\nStarting main process...")
        artist_name = "The Beatles"
        artist_info = client.get_artist_info(artist_name)
        
        if "error" in artist_info:
            print(f"Error: {artist_info['error']}")
            return
        
        # Save the data to JSON file
        filename = save_to_json(artist_info, artist_name)
        
        # Print summary
        print(f"\nSummary:")
        print(f"Artist: {artist_info['artist']['name']}")
        print(f"Total Albums: {len(artist_info['albums'])}")
        print(f"Total Songs: {len(artist_info['tracks'])}")
        print(f"Data saved to: {filename}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main() 