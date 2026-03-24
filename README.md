# MoodTune — Emotion-Based Music Recommender
### B.Tech Project | CSE | I.T.S Engineering College, Greater Noida

---

## Project Structure

```
moodtune/
├── app.py              ← Flask backend (DeepFace emotion detection)
├── requirements.txt    ← Python dependencies
├── templates/
│   └── index.html      ← Full frontend (webcam + YouTube links)
└── README.md
```

---

## Setup Instructions

### Step 1 — Install Python dependencies

```bash
pip install -r requirements.txt
```

> **Note:** DeepFace will auto-download its model weights (~100 MB) on first run.

### Step 2 — Run the Flask server

```bash
python app.py
```

You should see:
```
* Running on http://0.0.0.0:5000
```

### Step 3 — Open the app

Open your browser and go to:
```
http://localhost:5000
```

---

## How It Works

### Flow Diagram

```
Webcam (OpenCV) → Base64 Frame → Flask /detect API
       ↓
   DeepFace.analyze()
       ↓
 Emotion + Confidence Scores
       ↓
 Playlist Mapping (emotion → tracks)
       ↓
 YouTube Search URLs → Frontend Display
```

### API Endpoints

| Method | Endpoint           | Description                          |
|--------|--------------------|--------------------------------------|
| GET    | `/`                | Serve the main HTML frontend         |
| POST   | `/detect`          | Accept webcam frame, return emotion  |
| GET    | `/playlist/<mood>` | Return playlist for a given emotion  |

### POST /detect — Request Body

```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQ..."
}
```

### POST /detect — Response

```json
{
  "emotion": "happy",
  "confidence": 87.3,
  "scores": {
    "happy": 87.3,
    "neutral": 7.1,
    "sad": 2.4,
    "angry": 1.5,
    "surprise": 1.0,
    "fear": 0.5,
    "disgust": 0.2
  },
  "playlist": [
    {
      "title": "Happy",
      "artist": "Pharrell Williams",
      "youtube_url": "https://www.youtube.com/results?search_query=Happy+Pharrell+Williams+official+audio"
    }
  ]
}
```

---

## Technology Stack (as per Synopsis)

| Component         | Technology Used                    |
|-------------------|------------------------------------|
| Emotion Detection | DeepFace (FER2013 + OpenCV)        |
| Image Processing  | OpenCV (cv2)                       |
| Backend           | Python + Flask                     |
| Frontend          | HTML5 + CSS3 + JavaScript          |
| Music Integration | YouTube Search API (URL-based)     |
| Webcam Access     | HTML5 `getUserMedia` API           |

---

## Team

| Name              | Enrollment No.  |
|-------------------|-----------------|
| Abhishek Parmar   | 2202220100010   |
| Abhishek Solanki  | 2202220100013   |
| Aditya Kumar      | 2202220100022   |
| Ankit Kushwaha    | 2202220100037   |

**Supervisor:** Prof. Biswa Mohan Sahoo  
**Session:** 2025-26 | BCS 753

---

## Optional: Spotify Integration

To use real Spotify playback instead of YouTube links:

1. Create an app at https://developer.spotify.com
2. Get your `Client ID` and `Client Secret`
3. Install spotipy: `pip install spotipy`
4. Replace the `build_youtube_url()` function in `app.py` with Spotify search calls

```python
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET"
))

def search_spotify(title, artist):
    results = sp.search(q=f"{title} {artist}", type="track", limit=1)
    items = results["tracks"]["items"]
    if items:
        return items[0]["external_urls"]["spotify"]
    return None
```

---

## References

1. Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press.
2. Li, S., Deng, W. (2020). Deep Facial Expression Recognition: A Survey. *IEEE Transactions on Affective Computing*.
3. DeepFace Library — https://github.com/serengil/deepface
4. Spotify Developer API — https://developer.spotify.com
5. OpenCV Documentation — https://opencv.org
