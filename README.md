# 🎧 MoodTune — Emotion-Based Music Recommender

> An AI-powered web application that detects user emotions in real-time and recommends music accordingly.

---

## 🚀 Overview

MoodTune is an intelligent music recommendation system that uses **facial emotion recognition** to suggest songs based on your mood. It captures live webcam input, analyzes emotions using Deep Learning, and dynamically generates playlists.

---

## ✨ Features

- 🎥 Real-time emotion detection using webcam
- 🧠 AI-powered analysis with DeepFace
- 🎵 Smart music recommendations based on detected mood
- 🔗 Instant YouTube playback links
- 🌐 Clean and responsive web interface

---

## 🏗️ Project Structure

```
moodtune/
├── app.py              # Flask backend (emotion detection)
├── requirements.txt    # Dependencies
├── templates/
│   └── index.html      # Frontend (UI + webcam)
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/emotion-based-music-recommender.git
cd emotion-based-music-recommender
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ DeepFace downloads model weights (~100MB) on first run.

### 3️⃣ Run the application

```bash
python app.py
```

### 4️⃣ Open in browser

```
http://localhost:5000
```

---

## 🧠 How It Works

```
Webcam → Image Capture → DeepFace Analysis → Emotion Detection
        ↓
   Emotion Mapping → Playlist Generation → YouTube Links
```

---

## 🔌 API Endpoints

| Method | Endpoint           | Description                   |
| ------ | ------------------ | ----------------------------- |
| GET    | `/`                | Load web interface            |
| POST   | `/detect`          | Detect emotion from image     |
| GET    | `/playlist/<mood>` | Get songs for a specific mood |

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **AI Model:** DeepFace
- **Computer Vision:** OpenCV
- **Music Source:** YouTube

---

## 🔮 Future Improvements

- 🎧 Spotify API integration
- 📱 Mobile-friendly UI
- 📊 Emotion history tracking
- 🤖 Improved recommendation system

---

## 👨‍💻 Author

**Abhishek Parmar**

---

## 💡 Key Highlights

- Real-time AI + Web integration
- End-to-end full-stack project
- Practical use of Machine Learning
- API design and implementation

---

⭐ _If you found this project interesting, consider giving it a star!_
