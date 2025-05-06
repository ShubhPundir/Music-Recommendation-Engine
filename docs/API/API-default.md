# 🎧 Music Data Fetching API Documentation

This documentation outlines how to use the **MusicBrainz**, **Genius**, and **Last.fm** APIs for fetching music-related data such as metadata, lyrics, and artist information.

---

## 1. 🎼 MusicBrainz API

**Website:** [https://musicbrainz.org/doc/MusicBrainz_API](https://musicbrainz.org/doc/MusicBrainz_API)

### ✅ Overview:
MusicBrainz is an open music encyclopedia that collects music metadata, including artist names, release groups, and recordings.

### 🔐 Access:
- No API key required
- Requires a custom `User-Agent` header:


### 🚦 Rate Limits:
- 1 request per second (anonymous)
- Up to 5 requests per second with valid User-Agent

### 📡 Common Endpoints:
| Endpoint | Description |
|----------|-------------|
| `/ws/2/artist/?query=artist_name` | Search artist by name |
| `/ws/2/release-group/?artist=artist_id` | Get albums and singles |
| `/ws/2/recording/?artist=artist_id` | Get tracks by artist |

---

## 2. 🎤 Genius API

**Website:** [https://docs.genius.com](https://docs.genius.com)

### ✅ Overview:
Genius provides access to a database of lyrics and song metadata.

### 🔐 Access:
- Requires **OAuth2 access token**
- Sign up at [https://genius.com/developers](https://genius.com/developers)
- Add token to header:


### 🚦 Rate Limits:
- ~60 requests per minute (unofficial)
- Avoid HTML scraping (against ToS)

### 📡 Common Endpoints:
| Endpoint | Description |
|----------|-------------|
| `GET /search?q=track_name` | Search songs or artists |
| `GET /songs/:id` | Get song metadata |
| `GET /artists/:id` | Get artist info |

---

## 3. 📻 Last.fm API

**Website:** [https://www.last.fm/api](https://www.last.fm/api)

### ✅ Overview:
Last.fm offers music metadata, tags, artist info, track info, and listener stats.

### 🔐 Access:
- Requires an **API key**
- Register at: [https://www.last.fm/api/account/create](https://www.last.fm/api/account/create)
- Pass key as query param:


### 🚦 Rate Limits:
- 5 requests per second per IP

### 📡 Common Endpoints:
| Endpoint | Description |
|----------|-------------|
| `artist.getInfo&artist=ARTIST_NAME` | Get artist biography |
| `track.getInfo&artist=ARTIST_NAME&track=TRACK_NAME` | Get track details |
| `album.getInfo&artist=ARTIST_NAME&album=ALBUM_NAME` | Get album metadata |
| `track.search&track=TRACK_NAME` | Search for a track |

---

## ✅ Summary Table

| API        | API Key | Auth Required | Free Limit                  | Notable Endpoints                        |
|------------|---------|----------------|-----------------------------|-------------------------------------------|
| MusicBrainz | ❌      | No             | 1 req/sec (5 with User-Agent) | `/ws/2/artist`, `/ws/2/recording`         |
| Genius      | ✅      | Yes (Bearer)   | ~60 req/min (unofficial)     | `/search`, `/songs/:id`                   |
| Last.fm     | ✅      | Yes (API Key)  | 5 req/sec                    | `artist.getInfo`, `track.getInfo`         |
