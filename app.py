from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import cv2
import numpy as np
import base64
from deepface import DeepFace
import urllib.parse

app = Flask(__name__)
CORS(app)

# ── Home Route ──────────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html")


# ── Emotion → Mixed Playlist (English + Bollywood) ──────
EMOTION_PLAYLISTS = {
    "happy": [
        {"title": "Happy", "artist": "Pharrell Williams"},
        {"title": "Blinding Lights", "artist": "The Weeknd"},
        {"title": "Badtameez Dil", "artist": "Arijit Singh"},
        {"title": "Gallan Goodiyan", "artist": "Yashita Sharma"},
        {"title": "Uptown Funk", "artist": "Bruno Mars"},
        {"title": "Kala Chashma", "artist": "Amar Arshi"},
    ],
    "sad": [
        {"title": "Someone Like You", "artist": "Adele"},
        {"title": "Fix You", "artist": "Coldplay"},
        {"title": "Channa Mereya", "artist": "Arijit Singh"},
        {"title": "Agar Tum Saath Ho", "artist": "Alka Yagnik"},
        {"title": "The Night We Met", "artist": "Lord Huron"},
        {"title": "Tum Hi Ho", "artist": "Arijit Singh"},
    ],
    "angry": [
        {"title": "In The End", "artist": "Linkin Park"},
        {"title": "Numb", "artist": "Linkin Park"},
        {"title": "Sadda Haq", "artist": "Mohit Chauhan"},
        {"title": "Zinda", "artist": "Siddharth Mahadevan"},
        {"title": "Apna Time Aayega", "artist": "Ranveer Singh"},
        {"title": "Break Stuff", "artist": "Limp Bizkit"},
    ],
    "surprise": [
        {"title": "Electric Feel", "artist": "MGMT"},
        {"title": "Midnight City", "artist": "M83"},
        {"title": "Ghungroo", "artist": "Arijit Singh"},
        {"title": "Ilahi", "artist": "Arijit Singh"},
        {"title": "Pompeii", "artist": "Bastille"},
        {"title": "Senorita", "artist": "Farhan Akhtar"},
    ],
    "fear": [
        {"title": "Weightless", "artist": "Marconi Union"},
        {"title": "Experience", "artist": "Ludovico Einaudi"},
        {"title": "Kun Faya Kun", "artist": "A.R. Rahman"},
        {"title": "O Re Piya", "artist": "Rahat Fateh Ali Khan"},
        {"title": "Clair de Lune", "artist": "Debussy"},
        {"title": "Raabta", "artist": "Arijit Singh"},
    ],
    "neutral": [
        {"title": "Do I Wanna Know", "artist": "Arctic Monkeys"},
        {"title": "Redbone", "artist": "Childish Gambino"},
        {"title": "Kesariya", "artist": "Arijit Singh"},
        {"title": "Dil Diyan Gallan", "artist": "Atif Aslam"},
        {"title": "Crystalised", "artist": "The XX"},
        {"title": "Tum Se Hi", "artist": "Mohit Chauhan"},
    ],
    "disgust": [
        {"title": "Creep", "artist": "Radiohead"},
        {"title": "Hurt", "artist": "Nine Inch Nails"},
        {"title": "Beete Lamhein", "artist": "KK"},
        {"title": "Alvida", "artist": "KK"},
        {"title": "Mad World", "artist": "Gary Jules"},
        {"title": "Bhula Dena", "artist": "Mustafa Zahid"},
    ],
}

EMOTION_MAP = {
    "happy": "happy",
    "sad": "sad",
    "angry": "angry",
    "surprise": "surprise",
    "fear": "fear",
    "neutral": "neutral",
    "disgust": "disgust",
}


# ── Helper ──────────────────────────────────────────────
def build_youtube_url(title, artist):
    query = urllib.parse.quote_plus(f"{title} {artist} official audio")
    return f"https://www.youtube.com/results?search_query={query}"


# ── Detect Emotion ──────────────────────────────────────
@app.route("/detect", methods=["POST"])
def detect():
    data = request.get_json(force=True)
    image_b64 = data.get("image", "")

    if not image_b64:
        return jsonify({"error": "No image provided"}), 400

    try:
        header, encoded = image_b64.split(",", 1) if "," in image_b64 else ("", image_b64)
        img_bytes = base64.b64decode(encoded)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except Exception as e:
        return jsonify({"error": f"Image decode failed: {str(e)}"}), 400

    try:
        result = DeepFace.analyze(
            img_path=frame,
            actions=["emotion"],
            enforce_detection=False,
            detector_backend="opencv"
        )

        analysis = result[0] if isinstance(result, list) else result

        dominant_raw = str(analysis["dominant_emotion"]).lower()
        scores = {k: float(v) for k, v in analysis["emotion"].items()}

    except Exception as e:
        return jsonify({"error": f"DeepFace error: {str(e)}"}), 500

    dominant = EMOTION_MAP.get(dominant_raw, "neutral")

    # Normalize scores
    total = sum(scores.values()) or 1
    normalised = {k: float((v / total) * 100) for k, v in scores.items()}

    # Playlist
    tracks = EMOTION_PLAYLISTS.get(dominant, EMOTION_PLAYLISTS["neutral"])
    playlist = [
        {
            "title": t["title"],
            "artist": t["artist"],
            "youtube_url": build_youtube_url(t["title"], t["artist"]),
        }
        for t in tracks
    ]

    return jsonify({
        "emotion": dominant,
        "confidence": float(normalised.get(dominant, 0)),
        "scores": normalised,
        "playlist": playlist,
    })


# ── Manual Playlist ─────────────────────────────────────
@app.route("/playlist/<emotion>")
def get_playlist(emotion):
    emotion = emotion.lower()
    tracks = EMOTION_PLAYLISTS.get(emotion, EMOTION_PLAYLISTS["neutral"])

    playlist = [
        {
            "title": t["title"],
            "artist": t["artist"],
            "youtube_url": build_youtube_url(t["title"], t["artist"]),
        }
        for t in tracks
    ]

    return jsonify({"emotion": emotion, "playlist": playlist})


# ── Run Server ──────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
